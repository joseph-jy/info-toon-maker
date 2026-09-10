"""Offline regressions: python3 -B -m unittest discover -s scripts -p 'test_*.py'."""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import render_openai as renderer


def benchmark_usage(model: str) -> renderer.UsageSummary:
    """Non-sensitive token counters from the 2026-09-10 comparison."""
    legacy = renderer._priced_model_family(model) == "gpt-image-2"
    text_input, image_input, output = (1174 if legacy else 1184), 1452, (5488 if legacy else 1372)
    return renderer.extract_usage_summary(
        {"usage": {
            "input_tokens": text_input + image_input,
            "input_tokens_details": {"text_tokens": text_input, "image_tokens": image_input},
            "output_tokens": output,
            "total_tokens": text_input + image_input + output,
        }},
        model=model, size="1024x1536", quality="high",
    )


class CostTests(unittest.TestCase):
    def test_measured_usage_matches_benchmark_for_aliases_and_snapshots(self):
        models = {
            "gpt-image-2": 0.182126,
            "gpt-image-2-2026-04-21": 0.182126,
            "gpt-image-2.5-flare": 0.058696,
            "gpt-image-2.5-flare-2026-09-08": 0.058696,
            "gpt-image-2.5-sunburst": 0.058696,
            "gpt-image-2.5-sunburst-2026-09-08": 0.058696,
        }
        for model, expected in models.items():
            with self.subTest(model=model):
                usage = benchmark_usage(model)
                cost, note = renderer.estimate_cost_usd(usage, model=model, has_image_references=True)
                self.assertAlmostEqual(cost, expected, places=8)
                self.assertFalse(usage.output_tokens_estimated)
                self.assertEqual(note, "")

    def test_legacy_missing_usage_still_estimates_output_only(self):
        for model in ("gpt-image-2", "gpt-image-2-2026-04-21"):
            with self.subTest(model=model):
                usage = renderer.extract_usage_summary({}, model=model, size="1024x1536", quality="high")
                self.assertEqual(usage.output_tokens, 5488)
                self.assertTrue(usage.output_tokens_estimated)
                cost, note = renderer.estimate_cost_usd(usage, model=model, has_image_references=True)
                self.assertAlmostEqual(cost, 0.16464, places=8)
                self.assertIn("output only", note)
                self.assertIn("estimated from gpt-image-2", note)

    def test_new_models_never_use_legacy_output_estimator(self):
        for model in ("gpt-image-2.5-flare", "gpt-image-2.5-sunburst-2026-09-08"):
            for response in ({}, {"usage": {}}, {"usage": {"input_tokens": 100}}):
                with self.subTest(model=model, response=response):
                    usage = renderer.extract_usage_summary(response, model=model, size="1024x1536", quality="high")
                    self.assertIsNone(usage.output_tokens)
                    self.assertFalse(usage.output_tokens_estimated)
                    cost, note = renderer.estimate_cost_usd(usage, model=model, has_image_references=True)
                    self.assertIsNone(cost)
                    self.assertIn("unknown", note)

    def test_unknown_models_are_not_free_or_assumed_priced(self):
        for model in ("gpt-image-1", "gpt-image-2.5", "gpt-image-2.5-flare-preview"):
            with self.subTest(model=model):
                cost, note = renderer.estimate_cost_usd(
                    benchmark_usage(renderer.DEFAULT_IMAGE_MODEL), model=model, has_image_references=True,
                )
                self.assertIsNone(cost)
                self.assertIn("not configured", note)

    def test_known_zero_is_distinct_from_missing_usage(self):
        usage = renderer.extract_usage_summary(
            {"usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}},
            model=renderer.DEFAULT_IMAGE_MODEL, size="1024x1536", quality="high",
        )
        cost, _ = renderer.estimate_cost_usd(usage, model=renderer.DEFAULT_IMAGE_MODEL, has_image_references=False)
        self.assertEqual(cost, 0.0)
        self.assertEqual(renderer._fmt_usd(cost), "$0.0000")
        self.assertEqual(renderer._fmt_usd(None), "unknown")

    def test_missing_input_detail_is_estimated_and_disclosed(self):
        cases = [
            (renderer.UsageSummary(input_tokens=100, output_tokens=10), False, 0.0008, "text input"),
            (renderer.UsageSummary(input_tokens=100, output_tokens=10), True, 0.0011, "image input"),
            (renderer.UsageSummary(input_tokens=100, text_input_tokens=40, output_tokens=10), True, 0.00098, "60 input tokens"),
            (renderer.UsageSummary(output_tokens=10), True, 0.0003, "output only"),
        ]
        for usage, references, expected, note_fragment in cases:
            with self.subTest(usage=usage, references=references):
                cost, note = renderer.estimate_cost_usd(usage, model=renderer.DEFAULT_IMAGE_MODEL, has_image_references=references)
                self.assertAlmostEqual(cost, expected, places=8)
                self.assertIn(note_fragment, note)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        # Keep generated fixtures inside the repo; never load its actual .env.
        repo_root = Path(__file__).resolve().parents[1]
        self.temp = tempfile.TemporaryDirectory(prefix="render-test-", dir=repo_root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "_workspace" / "fixture"
        prompts = self.workspace / "03_prompts"
        prompts.mkdir(parents=True)
        (prompts / "master-image-prompt.md").write_text(
            "## Master Prompt (vertical-webtoon-page)\n\n```text\nA blue circle.\n```\n",
            encoding="utf-8",
        )

    def result(self, cost):
        return renderer.RenderResult(
            job=renderer.RenderJob(
                renderer.TRACK_WEBTOON, renderer.PromptSpec("oneshot", "A blue circle.", ""),
                self.workspace / "05_renders" / "final-webtoon.png", [],
            ),
            operation="generate",
            usage=benchmark_usage(renderer.DEFAULT_IMAGE_MODEL) if cost is not None else renderer.UsageSummary(),
            estimated_cost_usd=cost,
            cost_note="" if cost is not None else "Output token count was unavailable; cost is unknown.",
        )

    def test_reports_preserve_known_unknown_mixed_and_empty_totals(self):
        cases = [
            ([0.058696, 0.058696], "$0.1174"),
            ([None], "unknown"),
            ([0.058696, None], "unknown"),
            ([], "unknown"),
            ([0.0], "$0.0000"),
        ]
        for costs, formatted_total in cases:
            with self.subTest(costs=costs):
                results = [self.result(cost) for cost in costs]
                path = renderer.write_render_cost_report(
                    self.workspace, self.root, model=renderer.DEFAULT_IMAGE_MODEL,
                    size="1024x1536", quality="high", fmt="png",
                    results=results, failures=[] if costs else ["fixture/oneshot"],
                )
                report = path.read_text(encoding="utf-8")
                self.assertIn(f"- Estimated cost: `{formatted_total}`", report)
                self.assertIn("standard pricing for `gpt-image-2.5-flare`", report)
                self.assertIn("excluding cache discounts", report)
                rows = json.loads(report.split("```json\n", 1)[1].split("\n```", 1)[0])
                self.assertEqual([row["estimated_cost_usd"] for row in rows], costs)
                if formatted_total == "unknown":
                    self.assertIn("Unknown costs are not zero.", report)

    def test_unknown_model_report_does_not_claim_known_price_basis(self):
        path = renderer.write_render_cost_report(
            self.workspace, self.root, model="unpriced-model", size="1024x1536",
            quality="high", fmt="png", results=[self.result(None)], failures=[],
        )
        self.assertIn("- Price basis: unavailable for `unpriced-model`.", path.read_text(encoding="utf-8"))

    def test_cli_model_precedence_and_blank_environment_without_api_calls(self):
        cases = [
            ({}, [], "gpt-image-2.5-flare"),
            ({"OPENAI_IMAGE_MODEL": ""}, [], "gpt-image-2.5-flare"),
            ({"OPENAI_IMAGE_MODEL": "gpt-image-2"}, [], "gpt-image-2"),
            ({"OPENAI_IMAGE_MODEL": "gpt-image-2.5-flare"}, ["--model", "gpt-image-2.5-sunburst"], "gpt-image-2.5-sunburst"),
        ]
        for env, override, expected in cases:
            with self.subTest(env=env, override=override):
                output = io.StringIO()
                with (
                    patch.dict(os.environ, env, clear=True),
                    patch.object(renderer, "_resolve_repo_root", return_value=self.root),
                    patch.object(renderer, "render_one") as render,
                    redirect_stdout(output),
                ):
                    status = renderer.main([
                        "--slug", "fixture", "--track", "vertical-webtoon-page",
                        "--mode", "oneshot", "--size", "1024x1536", "--dry-run", *override,
                    ])
                self.assertEqual(status, 0)
                self.assertIn(f"model={expected} size=1024x1536 quality=high fmt=png", output.getvalue())
                self.assertIn("[dry-run] not calling API.", output.getvalue())
                render.assert_not_called()
                self.assertFalse((self.workspace / "05_renders").exists())


if __name__ == "__main__":
    unittest.main()
