"""Smoke tests for a freshly scaffolded skill repository."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BaselineTest(unittest.TestCase):
    def run_tool(self, script: str, *args: str) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), "--root", str(ROOT), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_strict_audit(self) -> None:
        self.run_tool("audit_skills.py", "--strict")

    def test_catalog_is_current(self) -> None:
        self.run_tool("generate_skill_catalog.py", "--check")

    def test_description_over_150_chars_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "soia-dev-test-description"
            skill.mkdir(parents=True)
            description = "x" * 151
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: soia-dev-test-description\n"
                f"description: {description}\n"
                "version: 0.1.0\n"
                "created_at: 2026-08-04 14:05:00\n"
                "updated_at: 2026-08-04 14:05:00\n"
                "created_by: test-model\n"
                "updated_by: test-model\n"
                "---\n\n"
                "# Test\n\n"
                "## 客户可读说明\n\n"
                "### 私密信息与中间数据\n\n无。\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "audit_skills.py"), "--root", str(root), "--strict"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("maximum is 150", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
