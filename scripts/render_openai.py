#!/usr/bin/env python3
"""Render infographic prompts via OpenAI Images API (gpt-image-2).

This script is the ONE exception to the harness rule "no in-repo image
rendering". Everything else in the repo still stops at prompt packs and
QA handoff; this script bridges the prompt pack to real files under
`_workspace/<slug>/05_renders/`.

Reads prompts directly from `03_prompts/master-image-prompt.md`,
`03_prompts/panel-prompts.md`, and `03_prompts/series-prompts.md`. Never
invents prompts or writes files outside `05_renders/`.

Usage:
    python scripts/render_openai.py \
        --slug mythos-fable-webtoon \
        --track editorial-poster \
        --mode oneshot

    python scripts/render_openai.py \
        --slug mythos-fable-webtoon \
        --track vertical-webtoon-page \
        --mode fallback

    python scripts/render_openai.py \
        --slug mythos-fable-webtoon \
        --track both --mode all

    python scripts/render_openai.py \
        --slug database-index-learning-comic \
        --track adult-learning-comic --mode series
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import sys
import time
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# ---------- .env loading (no external dep) ----------

def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


# ---------- Prompt extraction ----------

TRACK_EDITORIAL = "editorial-poster"
TRACK_WEBTOON = "vertical-webtoon-page"
TRACK_LEARNING = "adult-learning-comic"

# Filename mapping: (block_or_panel_id) -> output filename (without .ext).
EDITORIAL_SLOTS = [
    "block_00",
    "block_01",
    "block_02",
    "block_03",
    "block_04",
    "block_05",
]

WEBTOON_SLOTS = [
    "page_header",
    "panel_01",
    "panel_02",
    "panel_03",
    "panel_04",
    "footer_strip",
]

ONESHOT_FILENAME = {
    TRACK_EDITORIAL: "final-poster",
    TRACK_WEBTOON: "final-webtoon",
}


@dataclass
class PromptSpec:
    slot_id: str  # e.g. "block_00" or "panel_02" or "oneshot"
    prompt: str
    negative: str  # merged into main prompt as negative clause; API has no separate field


@dataclass
class RenderJob:
    track: str
    spec: PromptSpec
    out_path: Path
    reference_paths: list[Path]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_code_block_after(header_regex: str, body: str) -> str | None:
    """Find first ```text ... ``` fenced block after the given header regex."""
    header_match = re.search(header_regex, body)
    if not header_match:
        return None
    tail = body[header_match.end():]
    fence = re.search(r"```(?:text)?\n(.*?)\n```", tail, re.DOTALL)
    return fence.group(1).strip() if fence else None


def extract_oneshot(prompts_dir: Path, track: str) -> PromptSpec:
    body = _read(prompts_dir / "master-image-prompt.md")
    if track == TRACK_EDITORIAL:
        prompt_header = r"##\s+Master Prompt\s*\(editorial-poster\)"
        neg_header = r"##\s+Negative Prompt\s*(?!\(vertical)"
        # There are TWO "Negative Prompt" sections. First one (unlabeled) is editorial.
    elif track == TRACK_WEBTOON:
        prompt_header = r"##\s+Master Prompt\s*\(vertical-webtoon-page\)"
        neg_header = r"##\s+Negative Prompt\s*\(vertical-webtoon-page\)"
    else:
        raise SystemExit(f"unknown track: {track}")

    prompt_text = _extract_code_block_after(prompt_header, body)
    if not prompt_text:
        raise SystemExit(
            f"oneshot prompt not found for track {track} in master-image-prompt.md"
        )
    negative_text = _extract_code_block_after(neg_header, body) or ""
    return PromptSpec(slot_id="oneshot", prompt=prompt_text, negative=negative_text)


def extract_fallback(prompts_dir: Path, track: str) -> list[PromptSpec]:
    body = _read(prompts_dir / "panel-prompts.md")
    if track == TRACK_EDITORIAL:
        slots = EDITORIAL_SLOTS
    elif track == TRACK_WEBTOON:
        slots = WEBTOON_SLOTS
    else:
        raise SystemExit(f"unknown track: {track}")

    specs: list[PromptSpec] = []
    for slot_id in slots:
        # Section headers look like "### block_00 (..." or "### panel_01 (..."
        # or "### page_header (..." or "### footer_strip (...".
        header_regex = rf"###\s+{re.escape(slot_id)}\b"
        m = re.search(header_regex, body)
        if not m:
            print(f"[warn] slot section not found in panel-prompts.md: {slot_id}", file=sys.stderr)
            continue
        # Slice from this header to the next "### " header or end of file.
        start = m.end()
        next_hdr = re.search(r"\n###\s+", body[start:])
        section = body[start : start + next_hdr.start()] if next_hdr else body[start:]

        prompt_text = _extract_code_block_after(r"-\s*prompt:", section)
        if not prompt_text:
            print(f"[warn] no prompt code block in slot: {slot_id}", file=sys.stderr)
            continue
        negative_text = _extract_code_block_after(r"-\s*negative:", section) or ""
        specs.append(PromptSpec(slot_id=slot_id, prompt=prompt_text, negative=negative_text))

    return specs


def extract_series(prompts_dir: Path) -> list[PromptSpec]:
    body = _read(prompts_dir / "series-prompts.md")
    shared = _extract_code_block_after(r"##\s+Shared Prompt Policy", body)
    if not shared:
        raise SystemExit("shared prompt policy not found in series-prompts.md")
    shared_negative = (
        _extract_code_block_after(r"##\s+Shared Negative Prompt", body) or ""
    )

    matches = list(
        re.finditer(r"^###\s+(character_sheet|page_\d{2})\b", body, re.MULTILINE)
    )
    if not matches:
        raise SystemExit("no character_sheet or page_XX slots found in series-prompts.md")

    specs: list[PromptSpec] = []
    for index, match in enumerate(matches):
        slot_id = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        section = body[start:end]
        slot_prompt = _extract_code_block_after(r"-\s*prompt:", section)
        if not slot_prompt:
            raise SystemExit(f"no prompt code block in series slot: {slot_id}")
        slot_negative = _extract_code_block_after(r"-\s*negative:", section) or ""
        merged_negative = "\n".join(
            part for part in (shared_negative.strip(), slot_negative.strip()) if part
        )
        specs.append(
            PromptSpec(
                slot_id=slot_id,
                prompt=(
                    f"{shared.strip()}\n\n"
                    f"SLOT-SPECIFIC INSTRUCTIONS ({slot_id}):\n{slot_prompt.strip()}"
                ),
                negative=merged_negative,
            )
        )

    if specs[0].slot_id != "character_sheet":
        raise SystemExit("character_sheet must be the first slot in series-prompts.md")
    return specs


# ---------- OpenAI Images API ----------

def render_one(
    spec: PromptSpec,
    out_path: Path,
    *,
    model: str,
    size: str,
    quality: str,
    fmt: str,
    timeout: int,
    max_retries: int,
    reference_paths: list[Path],
) -> None:
    try:
        from openai import OpenAI
    except ImportError as e:
        raise SystemExit(
            "openai package not installed. run: pip install 'openai>=1.40.0'"
        ) from e

    client_kwargs = {"timeout": timeout}
    org = os.environ.get("OPENAI_ORG_ID") or None
    proj = os.environ.get("OPENAI_PROJECT_ID") or None
    if org:
        client_kwargs["organization"] = org
    if proj:
        client_kwargs["project"] = proj
    client = OpenAI(**client_kwargs)

    # gpt-image-2 has no dedicated negative-prompt field; merge into prompt tail.
    merged = spec.prompt.strip()
    if spec.negative.strip():
        merged = (
            merged
            + "\n\nAvoid the following in the image (treat as negative constraints): "
            + spec.negative.strip()
        )

    attempt = 0
    while True:
        attempt += 1
        try:
            operation = "edit" if reference_paths else "generate"
            print(
                f"[render] slot={spec.slot_id} operation={operation} "
                f"attempt={attempt} size={size} quality={quality}"
            )
            with ExitStack() as stack:
                if reference_paths:
                    image_files = [
                        stack.enter_context(path.open("rb")) for path in reference_paths
                    ]
                    image_input = image_files[0] if len(image_files) == 1 else image_files
                    resp = client.images.edit(
                        model=model,
                        image=image_input,
                        prompt=merged,
                        size=size,
                        quality=quality,
                        output_format=fmt,
                        n=1,
                    )
                else:
                    resp = client.images.generate(
                        model=model,
                        prompt=merged,
                        size=size,
                        quality=quality,
                        output_format=fmt,
                        n=1,
                    )
            b64 = resp.data[0].b64_json
            if not b64:
                raise RuntimeError("empty b64_json in response")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(base64.b64decode(b64))
            print(f"[ok] wrote {out_path}")
            return
        except Exception as e:
            if attempt > max_retries:
                raise
            wait = 2 ** (attempt - 1)
            print(f"[retry] slot={spec.slot_id} error={e!r} sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)


# ---------- CLI ----------

def _resolve_repo_root(script_path: Path) -> Path:
    return script_path.resolve().parent.parent


def _out_name(track: str, slot_id: str, fmt: str) -> str:
    if track == TRACK_LEARNING:
        if slot_id == "character_sheet":
            return f"character-sheet.{fmt}"
        if re.fullmatch(r"page_\d{2}", slot_id):
            return f"{slot_id.replace('_', '-')}.{fmt}"
        raise SystemExit(f"unknown learning comic slot: {slot_id}")
    if slot_id == "oneshot":
        base = ONESHOT_FILENAME[track]
    else:
        base = slot_id
    return f"{base}.{fmt}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="workspace slug under _workspace/")
    parser.add_argument(
        "--track",
        required=True,
        choices=[TRACK_EDITORIAL, TRACK_WEBTOON, TRACK_LEARNING, "both"],
        help="which prompt track to render",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["oneshot", "fallback", "series", "all"],
        help=(
            "oneshot=master prompt only, fallback=per-slot prompts, "
            "series=character sheet plus page prompts, all=all applicable prompts"
        ),
    )
    parser.add_argument(
        "--only",
        default=None,
        help="comma-separated slot ids to render (e.g. block_00,panel_01). fallback/all only.",
    )
    parser.add_argument("--dry-run", action="store_true", help="do not call API, just list plan")
    parser.add_argument("--model", default=None, help="override OPENAI_IMAGE_MODEL")
    parser.add_argument("--size", default=None, help="override OPENAI_IMAGE_SIZE")
    parser.add_argument("--quality", default=None, help="override OPENAI_IMAGE_QUALITY")
    parser.add_argument("--format", dest="fmt", default=None, help="override OPENAI_IMAGE_FORMAT")
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help=(
            "optional image reference path; repeat for multiple references. "
            "Learning-comic pages also use the generated character sheet automatically."
        ),
    )
    args = parser.parse_args(argv)

    repo_root = _resolve_repo_root(Path(__file__))
    load_dotenv(repo_root / ".env")

    if not args.dry_run and not os.environ.get("OPENAI_API_KEY"):
        print("[fatal] OPENAI_API_KEY not set (add it to .env)", file=sys.stderr)
        return 2

    workspace = repo_root / "_workspace" / args.slug
    if not workspace.is_dir():
        print(f"[fatal] workspace not found: {workspace}", file=sys.stderr)
        return 2
    prompts_dir = workspace / "03_prompts"
    renders_dir = workspace / "05_renders"

    model = args.model or os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
    size = args.size or os.environ.get("OPENAI_IMAGE_SIZE", "1536x2048")
    quality = args.quality or os.environ.get("OPENAI_IMAGE_QUALITY", "high")
    fmt = args.fmt or os.environ.get("OPENAI_IMAGE_FORMAT", "png")
    try:
        timeout = int(os.environ.get("OPENAI_TIMEOUT_SECONDS", "180"))
    except ValueError:
        timeout = 180
    try:
        max_retries = int(os.environ.get("OPENAI_MAX_RETRIES", "2"))
    except ValueError:
        max_retries = 2

    only_set: set[str] | None = None
    if args.only:
        only_set = {s.strip() for s in args.only.split(",") if s.strip()}

    if args.track == TRACK_LEARNING and args.mode not in ("series", "all"):
        print(
            "[fatal] adult-learning-comic requires --mode series or --mode all",
            file=sys.stderr,
        )
        return 2
    if args.track != TRACK_LEARNING and args.mode == "series":
        print(
            "[fatal] --mode series is only valid with --track adult-learning-comic",
            file=sys.stderr,
        )
        return 2

    external_references = [Path(value).expanduser().resolve() for value in args.reference]
    missing_references = [path for path in external_references if not path.is_file()]
    if missing_references:
        for path in missing_references:
            print(f"[fatal] reference image not found: {path}", file=sys.stderr)
        return 2

    tracks = (
        [TRACK_EDITORIAL, TRACK_WEBTOON]
        if args.track == "both"
        else [args.track]
    )

    plan: list[RenderJob] = []
    for track in tracks:
        if track == TRACK_LEARNING:
            specs = extract_series(prompts_dir)
            spec_by_id = {spec.slot_id: spec for spec in specs}
            selected = [
                spec for spec in specs if only_set is None or spec.slot_id in only_set
            ]
            selected_pages = [spec for spec in selected if spec.slot_id.startswith("page_")]
            character_spec = spec_by_id.get("character_sheet")
            if character_spec is None:
                raise SystemExit("character_sheet slot is required for adult-learning-comic")
            character_out = renders_dir / _out_name(
                track, character_spec.slot_id, fmt
            )

            needs_character_job = any(
                spec.slot_id == "character_sheet" for spec in selected
            ) or (bool(selected_pages) and not character_out.is_file())
            if needs_character_job:
                plan.append(
                    RenderJob(
                        track=track,
                        spec=character_spec,
                        out_path=character_out,
                        reference_paths=list(external_references),
                    )
                )

            for spec in selected_pages:
                references = [character_out, *external_references]
                plan.append(
                    RenderJob(
                        track=track,
                        spec=spec,
                        out_path=renders_dir / _out_name(track, spec.slot_id, fmt),
                        reference_paths=references,
                    )
                )
            continue

        if args.mode in ("oneshot", "all"):
            spec = extract_oneshot(prompts_dir, track)
            out = renders_dir / _out_name(track, spec.slot_id, fmt)
            if only_set is None or "oneshot" in only_set or ONESHOT_FILENAME[track] in only_set:
                plan.append(
                    RenderJob(track, spec, out, list(external_references))
                )
        if args.mode in ("fallback", "all"):
            for spec in extract_fallback(prompts_dir, track):
                out = renders_dir / _out_name(track, spec.slot_id, fmt)
                if only_set is None or spec.slot_id in only_set:
                    plan.append(
                        RenderJob(track, spec, out, list(external_references))
                    )

    if not plan:
        print("[warn] plan is empty. check --track/--mode/--only.", file=sys.stderr)
        return 1

    print(f"[plan] {len(plan)} render(s) — model={model} size={size} quality={quality} fmt={fmt}")
    for job in plan:
        refs = ", ".join(str(path) for path in job.reference_paths) or "none"
        print(
            f"  - [{job.track}] {job.spec.slot_id} -> "
            f"{job.out_path.relative_to(repo_root)} references={refs}"
        )

    if args.dry_run:
        print("[dry-run] not calling API.")
        return 0

    failures: list[str] = []
    for job in plan:
        missing_runtime_references = [
            path for path in job.reference_paths if not path.is_file()
        ]
        if missing_runtime_references:
            missing_list = ", ".join(str(path) for path in missing_runtime_references)
            print(
                f"[skip] {job.track}/{job.spec.slot_id}: "
                f"missing reference dependency: {missing_list}",
                file=sys.stderr,
            )
            failures.append(f"{job.track}/{job.spec.slot_id}")
            continue
        try:
            render_one(
                job.spec,
                job.out_path,
                model=model,
                size=size,
                quality=quality,
                fmt=fmt,
                timeout=timeout,
                max_retries=max_retries,
                reference_paths=job.reference_paths,
            )
        except Exception as e:
            print(
                f"[fail] {job.track}/{job.spec.slot_id}: {e!r}",
                file=sys.stderr,
            )
            failures.append(f"{job.track}/{job.spec.slot_id}")

    if failures:
        print(f"[done] with failures: {failures}", file=sys.stderr)
        return 1
    print("[done] all renders succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
