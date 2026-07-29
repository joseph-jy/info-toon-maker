#!/usr/bin/env python3
"""Report how often each cast profile has been cast, derived from run packages.

Why derived instead of stored: `usage.appeared_in[]` in cast/*.character.yaml is a
manual bookkeeping field. It has never once been filled in practice, so it cannot be
trusted as the source of truth. This script instead reads every
`_workspace/*/02_storyboard/character-bible.md` and recovers the casting from the run
itself, which cannot drift away from what was actually produced.

Usage:
  python scripts/cast_usage.py                 # table, hottest first
  python scripts/cast_usage.py --eligibility   # who is benched / cold / eligible now
  python scripts/cast_usage.py --cold          # only never-cast profiles
  python scripts/cast_usage.py --json          # machine-readable

The cooldown window counts only runs that actually cast from the library, so it does
not expire just because unrelated runs happened in between.

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
BIBLE_REL = Path("02_storyboard/character-bible.md")
BRIEF_REL = Path("00_input/brief.md")

# Real profile ids are private; only placeholders appear in this tracked file.
# "- Cast library profiles used (`cast/<id>.character.yaml`): `<id-1>` (explainer), ..."
PROFILES_LINE = re.compile(
    r"^-\s*Cast library profiles used[^:]*:\s*(?P<rest>.*)$", re.IGNORECASE
)
# `<id-1>` (explainer)  ->  id + optional role
ID_WITH_ROLE = re.compile(r"`(?P<id>[a-z0-9][a-z0-9-]*)`(?:\s*\((?P<role>[^)]*)\))?")
CREATED_LINE = re.compile(r"^-\s*created:\s*(?P<d>\d{4}-\d{2}-\d{2})", re.IGNORECASE)


@dataclass
class Appearance:
    slug: str
    run_date: date
    role: str


@dataclass
class Profile:
    profile_id: str
    path: Path
    appearances: list[Appearance] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.appearances)

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


def load_profiles(cast_dir: Path) -> dict[str, Profile]:
    profiles: dict[str, Profile] = {}
    if not cast_dir.is_dir():
        return profiles
    for path in sorted(cast_dir.glob(PROFILE_GLOB)):
        if path.name == "EXAMPLE.character.yaml":
            continue
        profile_id = path.name[: -len(".character.yaml")]
        profiles[profile_id] = Profile(profile_id=profile_id, path=path)
    return profiles


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
            profile_id = hit.group("id")
            if profile_id in TEMPLATE_IDS:
                continue
            role = (hit.group("role") or "").strip()
            out.append((profile_id, role))
    return out


def collect(root: Path) -> tuple[dict[str, Profile], list[str], int]:
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
        pairs = parse_casting(bible)
        if not pairs:
            continue
        when = run_date_for(run_dir)
        for profile_id, role in pairs:
            if profile_id in profiles:
                profiles[profile_id].appearances.append(
                    Appearance(slug=run_dir.name, run_date=when, role=role)
                )
            else:
                unknown.append(f"{run_dir.name} -> {profile_id}")
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
        print(f"{p.profile_id:<16} {p.count:>5}  {last_txt:<32} {roles}")
    cold = [p.profile_id for p in ordered if p.count == 0]
    if cold:
        print()
        print(f"never cast ({len(cold)}): {', '.join(cold)}")


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
                "appearances": [
                    {"slug": a.slug, "date": a.run_date.isoformat(), "role": a.role}
                    for a in sorted(p.appearances, key=lambda a: a.run_date)
                ],
            }
            for p in sorted(
                profiles.values(), key=lambda p: (-p.count, p.profile_id)
            )
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
        "--cold", action="store_true", help="print only never-cast profile ids"
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if args.window < 0:
        print("--window must be >= 0", file=sys.stderr)
        return 2

    root = repo_root(Path(__file__))
    profiles, unknown, run_count = collect(root)

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

    print_table(profiles, run_count)
    if unknown:
        print()
        print("[warn] character bibles referenced ids with no cast/ profile:", file=sys.stderr)
        for item in unknown:
            print(f"  - {item}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
