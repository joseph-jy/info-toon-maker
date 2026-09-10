"""Check the repo's shared Claude/Codex instruction copies without calling APIs."""

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
# These two Codex entry points deliberately delegate instead of copying the body.
DELEGATING_SKILLS = {"report-to-infographic-toon", "one-page-comic-toon"}


def files_by_name(directory: Path, pattern: str) -> dict[str, Path]:
    return {path.stem: path for path in directory.glob(pattern)}


def skills_by_name(directory: Path) -> dict[str, Path]:
    return {path.parent.name: path for path in directory.glob("*/SKILL.md")}


class CrossToolSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claude_agents = files_by_name(REPO_ROOT / ".claude/agents", "*.md")
        cls.codex_agents = files_by_name(REPO_ROOT / ".codex/agents", "*.toml")
        cls.claude_skills = skills_by_name(REPO_ROOT / ".claude/skills")
        cls.codex_skills = skills_by_name(REPO_ROOT / ".agents/skills")

    def test_agent_counterparts_exist(self):
        self.assertTrue(self.claude_agents, "No canonical agents found")
        self.assertEqual(set(self.claude_agents), set(self.codex_agents))

    def test_agent_instruction_bodies_match(self):
        for name in sorted(self.claude_agents.keys() & self.codex_agents.keys()):
            with self.subTest(agent=name):
                claude = self.claude_agents[name].read_text(encoding="utf-8")
                self.assertTrue(claude.startswith("---\n"), "Expected YAML frontmatter")
                _, separator, body = claude.partition("\n---\n")
                self.assertTrue(separator, "Missing frontmatter closing delimiter")
                codex = self.codex_agents[name].read_text(encoding="utf-8")
                # Compare source text in the repo's plain multiline-string format.
                # Platform-specific metadata (e.g. Claude's model) is not mirrored.
                match = re.search(r'^developer_instructions\s*=\s*"""\n(.*?)"""', codex, re.M | re.S)
                self.assertIsNotNone(match, "Expected multiline developer_instructions")
                self.assertEqual(body.strip(), match.group(1).strip(),
                                 f"Sync .claude/agents/{name}.md and .codex/agents/{name}.toml")

    def test_skill_counterparts_exist(self):
        self.assertTrue(self.claude_skills, "No canonical skills found")
        self.assertEqual(set(self.claude_skills), set(self.codex_skills))
        self.assertTrue(DELEGATING_SKILLS <= self.codex_skills.keys())

    def test_mirrored_skill_definitions_match(self):
        shared = self.claude_skills.keys() & self.codex_skills.keys()
        for name in sorted(shared - DELEGATING_SKILLS):
            with self.subTest(skill=name):
                self.assertEqual(
                    self.claude_skills[name].read_text(encoding="utf-8").strip(),
                    self.codex_skills[name].read_text(encoding="utf-8").strip(),
                    f"Sync .claude/skills/{name}/SKILL.md and .agents/skills/{name}/SKILL.md",
                )

    def test_delegating_skills_link_to_existing_canonical_workflows(self):
        for name in sorted(DELEGATING_SKILLS):
            with self.subTest(skill=name):
                canonical = REPO_ROOT / ".claude/skills" / name / "SKILL.md"
                self.assertTrue(canonical.is_file(), f"Missing canonical workflow: {canonical}")
                wrapper = self.codex_skills[name].read_text(encoding="utf-8")
                self.assertIn(f"`{canonical.relative_to(REPO_ROOT).as_posix()}`", wrapper)


if __name__ == "__main__":
    unittest.main()
