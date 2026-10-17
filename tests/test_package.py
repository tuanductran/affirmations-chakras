from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = (
    "root-chakra",
    "sacral-chakra",
    "solar-plexus-chakra",
    "heart-chakra",
    "throat-chakra",
    "third-eye-chakra",
    "crown-chakra",
)


def test_skill_metadata_and_references() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\n")
    assert "name: affirmations-chakras" in skill
    for slug in SLUGS:
        reference = ROOT / "references" / f"{slug}.md"
        bank = ROOT / "question-banks" / f"{slug}-question-bank.md"
        assert reference.exists()
        assert bank.exists()
        assert f"../question-banks/{slug}-question-bank.md" in reference.read_text(encoding="utf-8")


def test_question_banks_have_expected_counts() -> None:
    for slug in SLUGS:
        text = (ROOT / "question-banks" / f"{slug}-question-bank.md").read_text(encoding="utf-8")
        main, scoring = text.split("## Bộ chấm điểm nhanh", 1)
        assert len(re.findall(r"^\d+\.", main, re.MULTILINE)) == 15
        assert len(re.findall(r"^\d+\.", scoring, re.MULTILINE)) == 5


def test_score_script_json_output() -> None:
    script = ROOT / "scripts" / "score_chakras.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--json",
            json.dumps({"root": [0, 2, 4]}),
            "--dinh-dang",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result[0]["khoa"] == "root"
    assert result[0]["phan_tram"] == 50.0


def test_score_script_rejects_fractional_values() -> None:
    script = ROOT / "scripts" / "score_chakras.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--json", '{"root":[2.5]}'],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "số nguyên" in completed.stderr


def test_console_scripts_are_configured() -> None:
    config = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'score-chakras = "scripts.score_chakras:main"' in config
    assert 'generate-chakra-plan = "scripts.generate_365_day_plan:main"' in config


def test_365_day_generator(tmp_path: Path) -> None:
    script = ROOT / "scripts" / "generate_365_day_plan.py"
    output = tmp_path / "lo-trinh-365-ngay.md"
    subprocess.run([sys.executable, str(script), "--output", str(output)], check=True)
    text = output.read_text(encoding="utf-8")
    assert len(re.findall(r"^## Ngày ", text, re.MULTILINE)) == 365
