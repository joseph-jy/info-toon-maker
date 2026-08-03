#!/usr/bin/env python3
"""Report how often each cast profile has been cast, derived from run packages.

Why derived instead of stored: `usage.appeared_in[]` in cast/*.character.yaml is a
manual bookkeeping field. It has never once been filled in practice, so it cannot be
trusted as the source of truth. This script instead reads every
`_workspace/*/02_storyboard/character-bible.md` and recovers the casting from the run
itself, which cannot drift away from what was actually produced.

Usage:
  python scripts/cast_usage.py                 # table, hottest first
  python scripts/cast_usage.py --stats         # full appearance statistics
  python scripts/cast_usage.py --eligibility   # who is benched / cold / eligible now
  python scripts/cast_usage.py --cold          # only never-cast profiles
  python scripts/cast_usage.py --json          # machine-readable
  python scripts/cast_usage.py --declared-only # ignore recovered appearances

The cooldown window counts only runs that actually cast from the library, so it does
not expire just because unrelated runs happened in between.

Two detection passes, because bibles are hand-written and drift from the template:
  declared  - the "Cast library profiles used" line under `## Cast Source`. Authoritative.
  recovered - the profile id, or the `name_en` handle it maps to (`<id>.<x>`), appearing
              inside `## Cast Lock` or `## Real-Person Casting`. Older runs skip the Cast
              Source line or write ids without backticks, and an appearance that is
              invisible here would let a just-used face pass the cooldown gate.

The recovered pass deliberately never reads `## Cast Source` or any `Rotation` block:
those cite BENCHED and COLD ids that were *not* cast, so scanning them would count a
profile for the run that excluded it. Korean display names are not matched either -- a
two-syllable name has no word boundary to anchor on. Use `--declared-only` for strict
numbers.

Reads only. Never writes to cast/ or _workspace/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

PROFILE_GLOB = "*.character.yaml"
TEMPLATE_IDS = {"<id>", "dwayne"}  # EXAMPLE.character.yaml and doc placeholders
PLACEHOLDER_ID = re.compile(r"^id-\d+$")  # `<id-1>` in the template line
BIBLE_REL = Path("02_storyboard/character-bible.md")
BRIEF_REL = Path("00_input/brief.md")

# Real profile ids are private; only placeholders appear in this tracked file.
# "- Cast library profiles used (`cast/<id>.character.yaml`): `<id-1>` (explainer), ..."
PROFILES_LINE = re.compile(
    r"^-\s*Cast library profiles used[^:]*:\s*(?P<rest>.*)$", re.IGNORECASE
)
# One comma-separated entry of that line. Backticks are optional: several runs write
# bare ids, and requiring the backticks silently dropped their whole cast.
#   `<id-1>` (explainer)   |   <id-1> (explainer)   |   <id-1>
ID_WITH_ROLE = re.compile(
    r"`?(?P<id>[a-z][a-z0-9]*(?:[-.][a-z0-9]+)+)`?(?:\s*\((?P<role>[^)]*)\))?"
)
CREATED_LINE = re.compile(r"^-\s*created:\s*(?P<d>\d{4}-\d{2}-\d{2})", re.IGNORECASE)

# Recovered pass: only these bible sections describe who is actually in the comic.
SCAN_SECTIONS = ("cast lock", "real-person casting", "real person casting")
SKIP_SUBSECTION = "rotation"
ROLE_WORDS = ("explainer", "learner", "challenger", "mascot", "narrator")
H2 = re.compile(r"^##\s+(?P<title>.+?)\s*$")
H3 = re.compile(r"^###\s+(?P<title>.+?)\s*$")
CAST_ROLE_LINE = re.compile(r"^-\s*Cast role[^:]*:\s*(?P<value>.+)$", re.IGNORECASE)

DECLARED = "declared"
RECOVERED = "recovered"


@dataclass
class Appearance:
    slug: str
    run_date: date
    role: str
    source: str = DECLARED


@dataclass
class Profile:
    profile_id: str
    path: Path
    aliases: set[str] = field(default_factory=set)
    appearances: list[Appearance] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.appearances)

    @property
    def recovered_count(self) -> int:
        return sum(1 for a in self.appearances if a.source == RECOVERED)

    @property
    def first(self) -> Appearance | None:
        if not self.appearances:
            return None
        return min(self.appearances, key=lambda a: (a.run_date, a.slug))

    @property
    def last(self) -> Appearance | None:
        if not self.appearances:
            return None
        return max(self.appearances, key=lambda a: a.run_date)

    @property
    def roles(self) -> list[str]:
        seen: dict[str, None] = {}
        for a in self.appearances:
            if a.role:
                seen.setdefault(a.role, None)
        return list(seen)


def repo_root(script_path: Path) -> Path:
    return script_path.resolve().parent.parent


NAME_EN_LINE = re.compile(r"^name_en:\s*(?P<value>.+?)\s*$")


def profile_aliases(path: Path, profile_id: str) -> set[str]:
    """Match tokens for the recovered pass: the id plus its `name_en` handle.

    Bibles name real cast members by their work handle (`<id>.<x>`) as often as by
    profile id, so the handle has to be a first-class alias. Korean `name:` is skipped
    on purpose -- a two-syllable name has no boundary and would match inside words.
    """
    aliases = {profile_id.lower()}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = NAME_EN_LINE.match(line)
            if m:
                handle = m.group("value").strip().strip("\"'").lower()
                if re.fullmatch(r"[a-z][a-z0-9]*(?:[-.][a-z0-9]+)+", handle):
                    aliases.add(handle)
                break
    except OSError:
        pass
    return aliases


def load_profiles(cast_dir: Path) -> dict[str, Profile]:
    profiles: dict[str, Profile] = {}
    if not cast_dir.is_dir():
        return profiles
    for path in sorted(cast_dir.glob(PROFILE_GLOB)):
        if path.name == "EXAMPLE.character.yaml":
            continue
        profile_id = path.name[: -len(".character.yaml")]
        profiles[profile_id] = Profile(
            profile_id=profile_id,
            path=path,
            aliases=profile_aliases(path, profile_id),
        )
    return profiles


def alias_index(profiles: dict[str, Profile]) -> tuple[re.Pattern[str], dict[str, str]]:
    """One regex over every alias, plus alias -> profile_id.

    The boundary classes exclude `.`, `-` and word chars, which is what keeps
    `cast/images/<id>-01.jpg` and `cast/<id>.character.yaml` from counting as appearances
    while a `(<a>.<x>·<b>.<y>·<c>.<z>)` handle list still resolves to three hits.
    """
    lookup: dict[str, str] = {}
    for profile in profiles.values():
        for alias in profile.aliases:
            lookup[alias] = profile.profile_id
    if not lookup:
        return re.compile(r"(?!x)x"), lookup
    body = "|".join(re.escape(a) for a in sorted(lookup, key=len, reverse=True))
    pattern = re.compile(rf"(?<![a-z0-9._-])(?:{body})(?![a-z0-9._-])")
    return pattern, lookup


def run_date_for(run_dir: Path) -> date:
    """Prefer the brief's declared created: date; fall back to bible mtime."""
    brief = run_dir / BRIEF_REL
    if brief.is_file():
        try:
            for line in brief.read_text(encoding="utf-8").splitlines():
                m = CREATED_LINE.match(line.strip())
                if m:
                    return date.fromisoformat(m.group("d"))
        except (OSError, ValueError):
            pass
    bible = run_dir / BIBLE_REL
    stamp = bible.stat().st_mtime if bible.is_file() else run_dir.stat().st_mtime
    return datetime.fromtimestamp(stamp).date()


def parse_casting(bible: Path) -> list[tuple[str, str]]:
    """Return (profile_id, role) pairs recorded in a character bible."""
    try:
        text = bible.read_text(encoding="utf-8")
    except OSError:
        return []
    out: list[tuple[str, str]] = []
    for line in text.splitlines():
        m = PROFILES_LINE.match(line.strip())
        if not m:
            continue
        rest = m.group("rest")
        if rest.strip().lower().startswith("none"):
            continue
        for hit in ID_WITH_ROLE.finditer(rest):
            profile_id = hit.group("id").lower()
            if profile_id in TEMPLATE_IDS or PLACEHOLDER_ID.match(profile_id):
                continue
            role = short_role(hit.group("role") or "")
            out.append((profile_id, role))
    return out


def short_role(value: str) -> str:
    """Trim a prose role note down to something a table column can hold."""
    role = value.strip().strip("*").split("(")[0].strip(" .-—:")
    role = re.sub(r"\s+", " ", role)
    if len(role) > 28:
        role = role[:27].rstrip() + "…"
    return role


def parse_recovered(bible: Path, profiles: dict[str, Profile]) -> list[tuple[str, str]]:
    """Return (profile_id, role) pairs found inside the cast-describing sections.

    Blocks are delimited by headings; a hit takes the role from that block's
    `- Cast role:` line, or from the heading itself when it names a role slot.
    """
    try:
        lines = bible.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []

    pattern, lookup = alias_index(profiles)
    found: dict[str, tuple[str, int]] = {}  # id -> (role, confidence)
    in_scope = False
    skip_block = False
    block_hits: list[str] = []
    block_role = ""
    block_rank = 0  # 0 no role, 1 from a role-slot heading, 2 from a `Cast role:` line

    def flush() -> None:
        # A `Cast role:` block beats a role-slot heading: a heading like `### Explainer`
        # also covers the members it merely mentions, e.g. a portrait-only cameo.
        for profile_id in block_hits:
            if profile_id not in found or block_rank > found[profile_id][1]:
                found[profile_id] = (block_role, block_rank)

    for raw in lines:
        line = raw.strip()
        h2 = H2.match(line)
        h3 = H3.match(line)
        if h2 or h3:
            flush()
            block_hits, block_role, block_rank = [], "", 0
            title = (h2 or h3).group("title").strip().lower()
            title = title.replace("(optional)", "").strip()
            if h2:
                in_scope = any(title.startswith(s) for s in SCAN_SECTIONS)
                skip_block = False
            else:
                skip_block = SKIP_SUBSECTION in title
                if title in ROLE_WORDS:
                    block_role, block_rank = title, 1
            # `### <name> (<id>.<x>)` names the cast member in the heading itself, so the
            # heading is scanned as part of the block it opens.
            if in_scope and not skip_block:
                for hit in pattern.finditer(title):
                    profile_id = lookup[hit.group(0)]
                    if profile_id not in block_hits:
                        block_hits.append(profile_id)
            continue
        if not in_scope or skip_block:
            continue
        role_line = CAST_ROLE_LINE.match(line)
        if role_line:
            block_role, block_rank = short_role(role_line.group("value")), 2
        for hit in pattern.finditer(line.lower()):
            profile_id = lookup[hit.group(0)]
            if profile_id not in block_hits:
                block_hits.append(profile_id)
    flush()
    return sorted((pid, role) for pid, (role, _) in found.items())


def collect(
    root: Path, declared_only: bool = False
) -> tuple[dict[str, Profile], list[str], int]:
    profiles = load_profiles(root / "cast")
    unknown: list[str] = []
    workspace = root / "_workspace"
    run_count = 0
    if not workspace.is_dir():
        return profiles, unknown, run_count
    for run_dir in sorted(p for p in workspace.iterdir() if p.is_dir()):
        bible = run_dir / BIBLE_REL
        if not bible.is_file():
            continue
        run_count += 1

        cast_in_run: dict[str, tuple[str, str]] = {}  # id -> (role, source)
        for profile_id, role in parse_casting(bible):
            if profile_id in profiles:
                cast_in_run[profile_id] = (role, DECLARED)
            else:
                unknown.append(f"{run_dir.name} -> {profile_id}")
        if not declared_only:
            for profile_id, role in parse_recovered(bible, profiles):
                if profile_id in cast_in_run:
                    # Declared wins, but fill in a role the declared line omitted.
                    known_role, source = cast_in_run[profile_id]
                    if role and not known_role:
                        cast_in_run[profile_id] = (role, source)
                else:
                    cast_in_run[profile_id] = (role, RECOVERED)
        if not cast_in_run:
            continue

        when = run_date_for(run_dir)
        for profile_id, (role, source) in cast_in_run.items():
            profiles[profile_id].appearances.append(
                Appearance(
                    slug=run_dir.name, run_date=when, role=role, source=source
                )
            )
    return profiles, unknown, run_count


def print_table(profiles: dict[str, Profile], run_count: int) -> None:
    ordered = sorted(
        profiles.values(),
        key=lambda p: (-p.count, p.profile_id),
    )
    print(f"cast profiles: {len(profiles)}   runs with a character bible: {run_count}")
    print()
    print(f"{'profile':<16} {'casts':>5}  {'last run':<32} {'roles used'}")
    print("-" * 88)
    for p in ordered:
        last = p.last
        last_txt = f"{last.slug} ({last.run_date})" if last else "-"
        roles = ", ".join(p.roles) if p.roles else "-"
        casts = str(p.count) + ("*" if p.recovered_count else "")
        print(f"{p.profile_id:<16} {casts:>5}  {last_txt:<32} {roles}")
    cold = [p.profile_id for p in ordered if p.count == 0]
    if cold:
        print()
        print(f"never cast ({len(cold)}): {', '.join(cold)}")
    if any(p.recovered_count for p in ordered):
        print()
        print("* includes appearances recovered from Cast Lock / Real-Person Casting")
        print("  (the run's Cast Source line was missing or unparseable) — see --stats")


def co_appearances(profiles: dict[str, Profile]) -> list[tuple[str, str, int]]:
    """Pairs that shared at least one run, most-shared first."""
    by_run: dict[str, set[str]] = {}
    for p in profiles.values():
        for a in p.appearances:
            by_run.setdefault(a.slug, set()).add(p.profile_id)
    pairs: dict[tuple[str, str], int] = {}
    for members in by_run.values():
        ordered = sorted(members)
        for i, left in enumerate(ordered):
            for right in ordered[i + 1 :]:
                pairs[(left, right)] = pairs.get((left, right), 0) + 1
    return [
        (left, right, n)
        for (left, right), n in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0]))
    ]


def print_stats(profiles: dict[str, Profile], run_count: int) -> None:
    library_runs = library_runs_newest_first(profiles)
    total = len(library_runs)
    recency = {slug: i for i, (slug, _) in enumerate(library_runs)}
    castings = sum(p.count for p in profiles.values())
    recovered_runs = sorted(
        {
            a.slug
            for p in profiles.values()
            for a in p.appearances
            if a.source == RECOVERED
        }
    )
    ever = [p for p in profiles.values() if p.count]

    print("CAST APPEARANCE STATS")
    print(f"  runs with a character bible : {run_count}")
    print(f"  runs that cast from cast/   : {total}")
    print(f"  profiles in cast/           : {len(profiles)}")
    pct = f" ({len(ever) * 100 // len(profiles)}%)" if profiles else ""
    print(f"  profiles ever cast          : {len(ever)}/{len(profiles)}{pct}")
    avg = f"  (avg {castings / total:.1f} per run)" if total else ""
    print(f"  total castings              : {castings}{avg}")
    print()

    def stamp(a: Appearance | None) -> str:
        return f"{a.slug} ({a.run_date})" if a else "-"

    rows: list[tuple[str, str, str, str, str, str, str]] = []
    for p in sorted(profiles.values(), key=lambda p: (-p.count, p.profile_id)):
        last = p.last
        ago = recency.get(last.slug) if last else None
        rows.append(
            (
                p.profile_id,
                str(p.count),
                str(p.recovered_count) if p.recovered_count else "",
                f"{p.count * 100 // total}%" if total and p.count else "-",
                "-" if ago is None else str(ago),
                stamp(p.first),
                stamp(last),
            )
        )
    # Roles hold Korean text of unpredictable display width, so that column goes last
    # and is never padded; every other column is sized to its own widest value.
    w_id = max(len("profile"), *(len(r[0]) for r in rows))
    w_first = max(len("first cast"), *(len(r[5]) for r in rows))
    w_last = max(len("last cast"), *(len(r[6]) for r in rows))
    header = (
        f"{'profile':<{w_id}}  {'casts':>5} {'rec':>3} {'share':>5} {'ago':>3}  "
        f"{'first cast':<{w_first}}  {'last cast':<{w_last}}  roles"
    )
    print(header)
    print("-" * len(header))
    for pid, casts, rec, share, ago, first, last in rows:
        profile = profiles[pid]
        roles = ", ".join(profile.roles) if profile.roles else "-"
        print(
            f"{pid:<{w_id}}  {casts:>5} {rec:>3} {share:>5} {ago:>3}  "
            f"{first:<{w_first}}  {last:<{w_last}}  {roles}"
        )
    print()
    print("  rec    of those casts, how many were recovered rather than declared")
    print("  share  of runs that cast from the library")
    print("  ago    library-using runs since that profile's last cast (0 = latest run)")
    print()

    roles: dict[str, int] = {}
    for p in profiles.values():
        for a in p.appearances:
            roles[a.role or "(unrecorded)"] = roles.get(a.role or "(unrecorded)", 0) + 1
    print("ROLE DISTRIBUTION")
    if roles:
        for role, n in sorted(roles.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {n:>3}  {role}")
    else:
        print("  (none)")
    print()

    pairs = co_appearances(profiles)
    print("CO-APPEARANCES (shared runs; watch these for confusable-cast collisions)")
    if pairs:
        for left, right, n in pairs[:12]:
            print(f"  {n:>3}  {left} + {right}")
        if len(pairs) > 12:
            print(f"       ... and {len(pairs) - 12} more pair(s)")
    else:
        print("  (none)")
    print()

    print("RUNS THAT CAST FROM THE LIBRARY (newest first)")
    for slug, when in library_runs:
        members = sorted(
            p.profile_id for p in profiles.values() if any(a.slug == slug for a in p.appearances)
        )
        mark = " [recovered]" if slug in recovered_runs else ""
        print(f"  {when}  {slug}{mark}: {', '.join(members)}")
    if recovered_runs:
        print()
        print(
            "[recovered] the cast was read out of Cast Lock / Real-Person Casting because "
            "the\n            run's Cast Source line is missing or off-template. Fix those "
            "bibles, or\n            run --declared-only to see the strict numbers."
        )


DEFAULT_WINDOW = 3


def library_runs_newest_first(profiles: dict[str, Profile]) -> list[tuple[str, date]]:
    """Distinct runs that cast at least one library profile, newest first."""
    seen: dict[str, date] = {}
    for p in profiles.values():
        for a in p.appearances:
            prior = seen.get(a.slug)
            if prior is None or a.run_date > prior:
                seen[a.slug] = a.run_date
    return sorted(seen.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)


def eligibility(
    profiles: dict[str, Profile], window: int
) -> tuple[list[tuple[str, str]], list[str], list[str], list[tuple[str, date]]]:
    """Split profiles into benched / cold / eligible for the given cooldown window."""
    recent = library_runs_newest_first(profiles)[:window]
    recent_slugs = {slug for slug, _ in recent}

    benched: list[tuple[str, str]] = []
    cold: list[str] = []
    eligible: list[str] = []
    for p in sorted(profiles.values(), key=lambda p: p.profile_id):
        hits = sorted({a.slug for a in p.appearances if a.slug in recent_slugs})
        if hits:
            benched.append((p.profile_id, ", ".join(hits)))
        elif p.count == 0:
            cold.append(p.profile_id)
        else:
            eligible.append(p.profile_id)
    return benched, cold, eligible, recent


def print_eligibility(profiles: dict[str, Profile], window: int) -> None:
    benched, cold, eligible, recent = eligibility(profiles, window)

    print(f"cooldown window: last {window} run(s) that cast from the library")
    if recent:
        for slug, when in recent:
            print(f"  - {slug} ({when})")
    else:
        print("  - none yet; no profile is benched")
    print()

    print(f"BENCHED ({len(benched)}) — do not cast unless you write an override line")
    for profile_id, where in benched or []:
        print(f"  {profile_id:<16} cast in: {where}")
    if not benched:
        print("  (none)")
    print()

    print(f"COLD ({len(cold)}) — never cast; pick at least ONE of these while non-empty")
    print(f"  {', '.join(cold) if cold else '(none)'}")
    print()

    print(f"ELIGIBLE ({len(eligible)}) — cast before, but outside the window")
    print(f"  {', '.join(eligible) if eligible else '(none)'}")
    print()

    if cold:
        print("rule: >=1 pick from COLD, and none from BENCHED without an override line")
    else:
        print("rule: cold list is drained; only the BENCHED constraint applies")


def print_cold(profiles: dict[str, Profile]) -> None:
    cold = sorted(p.profile_id for p in profiles.values() if p.count == 0)
    if not cold:
        print("every profile has been cast at least once.")
        return
    for profile_id in cold:
        print(profile_id)


def as_json(
    profiles: dict[str, Profile], unknown: list[str], run_count: int, window: int
) -> str:
    benched, cold, eligible, recent = eligibility(profiles, window)
    payload = {
        "runs_with_character_bible": run_count,
        "cooldown": {
            "window": window,
            "recent_library_runs": [
                {"slug": slug, "date": when.isoformat()} for slug, when in recent
            ],
            "benched": [{"id": pid, "cast_in": where} for pid, where in benched],
            "cold": cold,
            "eligible": eligible,
        },
        "profiles": [
            {
                "id": p.profile_id,
                "casts": p.count,
                "roles_used": p.roles,
                "last_run": p.last.slug if p.last else None,
                "last_date": p.last.run_date.isoformat() if p.last else None,
                "recovered_casts": p.recovered_count,
                "first_run": p.first.slug if p.first else None,
                "appearances": [
                    {
                        "slug": a.slug,
                        "date": a.run_date.isoformat(),
                        "role": a.role,
                        "source": a.source,
                    }
                    for a in sorted(p.appearances, key=lambda a: a.run_date)
                ],
            }
            for p in sorted(
                profiles.values(), key=lambda p: (-p.count, p.profile_id)
            )
        ],
        "co_appearances": [
            {"pair": [left, right], "shared_runs": n}
            for left, right, n in co_appearances(profiles)
        ],
        "unresolved_ids": unknown,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Report cast profile usage derived from run packages."
    )
    parser.add_argument(
        "--eligibility",
        action="store_true",
        help="show who is benched by cooldown, who is cold, and who is eligible",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_WINDOW,
        help=(
            "cooldown window: how many recent library-using runs bench a profile "
            f"(default {DEFAULT_WINDOW})"
        ),
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="full statistics: counts, share, role mix, co-appearances, run list",
    )
    parser.add_argument(
        "--cold", action="store_true", help="print only never-cast profile ids"
    )
    parser.add_argument(
        "--declared-only",
        action="store_true",
        help=(
            "count only casts declared on a `Cast library profiles used` line; "
            "skip appearances recovered from Cast Lock / Real-Person Casting"
        ),
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if args.window < 0:
        print("--window must be >= 0", file=sys.stderr)
        return 2

    root = repo_root(Path(__file__))
    profiles, unknown, run_count = collect(root, declared_only=args.declared_only)

    if not profiles:
        print("no cast profiles found under cast/.", file=sys.stderr)
        return 1

    if args.json:
        print(as_json(profiles, unknown, run_count, args.window))
        return 0
    if args.cold:
        print_cold(profiles)
        return 0
    if args.eligibility:
        print_eligibility(profiles, args.window)
        return 0
    if args.stats:
        print_stats(profiles, run_count)
        if unknown:
            print()
            print("[warn] bibles referenced ids with no cast/ profile:", file=sys.stderr)
            for item in unknown:
                print(f"  - {item}", file=sys.stderr)
        return 0

    print_table(profiles, run_count)
    if unknown:
        print()
        print("[warn] character bibles referenced ids with no cast/ profile:", file=sys.stderr)
        for item in unknown:
            print(f"  - {item}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
