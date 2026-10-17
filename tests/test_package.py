from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.score_chakras import level_for, score, validate_scores

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


def test_score_script_reads_file(tmp_path: Path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text('{"heart":[4,3,2]}', encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "score_chakras.py"),
            "--file",
            str(scores_file),
            "--dinh-dang",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result[0]["khoa"] == "heart"
    assert result[0]["phan_tram"] == 75.0


def test_score_script_rejects_fractional_values() -> None:
    script = ROOT / "scripts" / "score_chakras.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--json", '{"root":[2.5]}'],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "số nguyên" in completed.stderr


@pytest.mark.parametrize(
    ("percent", "expected"),
    [
        (0, "cần được nâng đỡ"),
        (24.9, "cần được nâng đỡ"),
        (25, "đang được khám phá"),
        (49.9, "đang được khám phá"),
        (50, "khá được nâng đỡ"),
        (74.9, "khá được nâng đỡ"),
        (75, "đang vững vàng"),
        (100, "đang vững vàng"),
    ],
)
def test_level_for_covers_continuous_score_ranges(percent: float, expected: str) -> None:
    assert level_for(percent) == expected


@pytest.mark.parametrize(
    "raw",
    [
        [],
        {"unknown": [1]},
        {"root": []},
        {"root": [True]},
        {"root": [2.5]},
        {"root": [-1]},
        {"root": [5]},
    ],
)
def test_validate_scores_rejects_invalid_input(raw: object) -> None:
    with pytest.raises(ValueError):
        validate_scores(raw)


def test_score_classifies_valid_fractional_percentage() -> None:
    result = score({"root": [3, 3, 3, 3, 3, 3, 2]})
    assert result[0]["phan_tram"] == 71.4
    assert result[0]["muc_goi_y"] == "khá được nâng đỡ"


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
    assert "## Ngày 1: Gốc rễ" in text
    assert "## Ngày 364: Vương miện" in text
    assert "## Ngày 365: Tổng kết năm" in text


def test_365_day_generator_reports_output_errors(tmp_path: Path) -> None:
    output = tmp_path / "missing" / "plan.md"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_365_day_plan.py"),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "Không thể ghi tệp" in completed.stderr
