from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
from markdown_it import MarkdownIt

from scripts.generate_365_day_plan import main as generate_plan_main
from scripts.score_chakras import level_for, score, validate_scores
from scripts.score_chakras import main as score_main

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


def markdown_link_errors(root: Path) -> list[str]:
    parser = MarkdownIt("commonmark")
    ignored = {".git", ".venv", "build", "dist", "node_modules"}
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in sorted(root.rglob("*.md")):
        if ignored.intersection(source.relative_to(root).parts):
            continue

        tokens = parser.parse(source.read_text(encoding="utf-8"))
        for token in tokens:
            if token.type != "inline":
                continue
            for child in token.children or []:
                if child.type != "link_open":
                    continue
                href = child.attrGet("href")
                if not isinstance(href, str) or not href:
                    continue
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc:
                    continue

                target = (source.parent / unquote(parsed.path)).resolve()
                try:
                    target.relative_to(root.resolve())
                except ValueError:
                    errors.append(f"{source.relative_to(root)}: link escapes repository: {href}")
                    continue
                if not target.exists():
                    errors.append(f"{source.relative_to(root)}: missing target: {href}")
                    continue
                if parsed.fragment and target.is_file() and target.suffix.lower() == ".md":
                    fragment = unquote(parsed.fragment)
                    if target not in anchor_cache:
                        anchor_cache[target] = anchors_for_markdown(target, parser)
                    if fragment not in anchor_cache[target]:
                        errors.append(f"{source.relative_to(root)}: missing heading anchor: {href}")

    return errors


def anchors_for_markdown(path: Path, parser: MarkdownIt) -> set[str]:
    tokens = parser.parse(path.read_text(encoding="utf-8"))
    anchors: set[str] = set()
    slug_counts: dict[str, int] = defaultdict(int)
    for index, token in enumerate(tokens[:-1]):
        if token.type != "heading_open" or tokens[index + 1].type != "inline":
            continue
        inline = tokens[index + 1]
        heading_text = "".join(
            child.content
            for child in inline.children or []
            if child.type in {"text", "code_inline"}
        )
        slug = re.sub(r"[^\w -]", "", heading_text.casefold())
        slug = re.sub(r"\s+", "-", slug).strip("-")
        duplicate = slug_counts[slug]
        slug_counts[slug] += 1
        anchors.add(f"{slug}-{duplicate}" if duplicate else slug)
    return anchors


def test_markdown_local_links_and_anchors() -> None:
    assert markdown_link_errors(ROOT) == []


def test_markdown_link_checker_reports_missing_files_and_anchors(tmp_path: Path) -> None:
    (tmp_path / "index.md").write_text(
        "[valid](target.md#section) [missing](absent.md) [bad anchor](target.md#absent)\n\n"
        "```markdown\n[ignored](not-a-link.md)\n```\n",
        encoding="utf-8",
    )
    (tmp_path / "target.md").write_text("# Section\n", encoding="utf-8")
    errors = markdown_link_errors(tmp_path)
    assert len(errors) == 2
    assert any("missing target" in error for error in errors)
    assert any("missing heading anchor" in error for error in errors)


def test_skill_metadata_and_references() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\n")
    metadata = skill.split("---", 2)[1]
    name = re.search(r"^name:\s*(.+)$", metadata, re.MULTILINE)
    description = re.search(r'^description:\s*"(.+)"$', metadata, re.MULTILINE)
    assert name is not None
    assert description is not None
    assert name.group(1) == ROOT.name
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1))
    assert len(name.group(1)) <= 64
    assert 0 < len(description.group(1)) <= 1024
    assert "license: MIT" in metadata
    for slug in SLUGS:
        reference = ROOT / "references" / f"{slug}.md"
        bank = ROOT / "question-banks" / f"{slug}-question-bank.md"
        assert reference.exists()
        assert bank.exists()
        assert f"../question-banks/{slug}-question-bank.md" in reference.read_text(encoding="utf-8")


def test_agent_skills_follow_specification() -> None:
    skill_files = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
    assert {path.parent.name for path in skill_files} == {
        "chakra-content-editor",
        "python-markdown-maintenance",
    }
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        metadata = text.split("---", 2)[1]
        name = re.search(r"^name:\s*(.+)$", metadata, re.MULTILINE)
        description = re.search(r'^description:\s*"(.+)"$', metadata, re.MULTILINE)
        assert name is not None
        assert description is not None
        assert name.group(1) == path.parent.name
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1))
        assert len(name.group(1)) <= 64
        assert 0 < len(description.group(1)) <= 1024
        assert "license: MIT" in metadata
        assert len(text.splitlines()) <= 500


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


def test_score_cli_template_json_and_text(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["score-chakras", "--mau"])
    assert score_main() == 0
    template = json.loads(capsys.readouterr().out)
    assert set(template) == {
        "root",
        "sacral",
        "solar_plexus",
        "heart",
        "throat",
        "third_eye",
        "crown",
    }
    assert all(values == [None] * 5 for values in template.values())

    monkeypatch.setattr(
        sys,
        "argv",
        ["score-chakras", "--json", '{"root":[0,2,4]}', "--dinh-dang", "json"],
    )
    assert score_main() == 0
    assert json.loads(capsys.readouterr().out)[0]["phan_tram"] == 50.0

    monkeypatch.setattr(sys, "argv", ["score-chakras", "--json", '{"root":[0,2,4]}'])
    assert score_main() == 0
    text = capsys.readouterr().out
    assert "KẾT QUẢ TỰ PHẢN TỈNH" in text
    assert "Chủ đề có điểm thấp nhất để bắt đầu: Gốc rễ." in text


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


def test_score_cli_file_and_error_paths(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    score_file = tmp_path / "scores.json"
    score_file.write_text('{"heart":[4,3,2]}', encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["score-chakras", "--file", str(score_file), "--dinh-dang", "json"],
    )
    assert score_main() == 0
    assert json.loads(capsys.readouterr().out)[0]["khoa"] == "heart"

    monkeypatch.setattr(sys, "argv", ["score-chakras", "--json", "not-json"])
    assert score_main() == 2
    assert capsys.readouterr().err.startswith("Lỗi:")

    monkeypatch.setattr(sys, "argv", ["score-chakras", "--file", str(tmp_path / "missing.json")])
    assert score_main() == 2
    assert capsys.readouterr().err.startswith("Lỗi:")


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
        {},
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


@pytest.mark.parametrize("percent", [-0.1, 100.1])
def test_level_for_out_of_range_percent(percent: float) -> None:
    assert level_for(percent) == "chưa đủ dữ liệu"


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


def test_generator_main_writes_plan(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    output = tmp_path / "plan.md"
    monkeypatch.setattr(sys, "argv", ["generate-chakra-plan", "--output", str(output)])
    assert generate_plan_main() == 0
    assert "với 365 ngày" in capsys.readouterr().out
    assert len(re.findall(r"^## Ngày ", output.read_text(encoding="utf-8"), re.MULTILINE)) == 365


def test_generator_main_reports_write_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    output = tmp_path / "missing" / "plan.md"
    monkeypatch.setattr(sys, "argv", ["generate-chakra-plan", "--output", str(output)])
    with pytest.raises(SystemExit) as error:
        generate_plan_main()
    assert error.value.code == 2
    assert "Không thể ghi tệp" in capsys.readouterr().err
