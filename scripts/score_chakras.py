#!/usr/bin/env python3
"""Tính điểm tự báo cáo cho bảy chủ đề luân xa.

Điểm 0–4 cho mỗi câu:
0 = hoàn toàn không đúng lúc này
1 = ít đúng
2 = đúng một phần
3 = khá đúng
4 = rất đúng

Đây là công cụ tự phản tỉnh, không phải công cụ chẩn đoán.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import TypedDict


class ScoreRow(TypedDict):
    khoa: str
    ten: str
    so_cau: int
    diem_trung_binh: float


CHAKRAS = {
    "root": "Gốc rễ",
    "sacral": "Xương cùng",
    "solar_plexus": "Đám rối mặt trời",
    "heart": "Tim",
    "throat": "Cổ họng",
    "third_eye": "Con mắt thứ ba",
    "crown": "Vương miện",
}

CSV_ID_COLUMN = "ma_nguoi_tham_gia"
CSV_SCORE_COLUMNS = tuple(f"{chakra}_{question}" for chakra in CHAKRAS for question in range(1, 6))
CSV_COLUMNS = (CSV_ID_COLUMN, *CSV_SCORE_COLUMNS)


class ParticipantScores(TypedDict):
    ma_nguoi_tham_gia: str
    scores: dict[str, list[int]]


class ParticipantResult(TypedDict):
    ma_nguoi_tham_gia: str
    ket_qua: list[ScoreRow]


class GroupRow(TypedDict):
    khoa: str
    ten: str
    so_nguoi: int
    diem_trung_binh: float


def validate_scores(raw: object) -> dict[str, list[int]]:
    if not isinstance(raw, dict):
        raise ValueError("Dữ liệu phải là một đối tượng JSON theo từng luân xa.")
    if not raw:
        raise ValueError("Phải cung cấp điểm cho ít nhất một luân xa.")
    result: dict[str, list[int]] = {}
    for key, values in raw.items():
        if key not in CHAKRAS:
            raise ValueError(f"Tên luân xa không hợp lệ: {key}")
        if not isinstance(values, list) or not values:
            raise ValueError(f"Điểm của {key} phải là một danh sách không rỗng.")
        clean: list[int] = []
        for value in values:
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"Điểm của {key} phải là số nguyên từ 0 đến 4.")
            if value < 0 or value > 4:
                raise ValueError(f"Điểm của {key} phải nằm trong khoảng 0 đến 4.")
            clean.append(value)
        if clean:
            result[key] = clean
    if not result:
        raise ValueError("Phải cung cấp ít nhất một câu trả lời.")
    return result


def validate_csv_scores(raw: str) -> list[ParticipantScores]:
    raw = raw.removeprefix("\ufeff")
    try:
        dialect = csv.Sniffer().sniff(raw, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(io.StringIO(raw), dialect=dialect))
    if not rows:
        raise ValueError("Tệp CSV đang trống.")
    header = rows[0]
    if len(header) != len(set(header)):
        raise ValueError("Tệp CSV có tên cột bị lặp.")
    if set(header) != set(CSV_COLUMNS):
        missing = sorted(set(CSV_COLUMNS) - set(header))
        unknown = sorted(set(header) - set(CSV_COLUMNS))
        details = []
        if missing:
            details.append(f"thiếu cột: {', '.join(missing)}")
        if unknown:
            details.append(f"cột không nhận diện: {', '.join(unknown)}")
        raise ValueError(f"Cấu trúc CSV không hợp lệ ({'; '.join(details)}).")

    participants: list[ParticipantScores] = []
    seen_ids: set[str] = set()
    for line_number, values in enumerate(rows[1:], start=2):
        if not any(value.strip() for value in values):
            continue
        if len(values) != len(header):
            raise ValueError(f"Dòng {line_number} phải có đúng {len(header)} cột.")
        row = dict(zip(header, values, strict=True))
        if not any(row[column].strip() for column in CSV_SCORE_COLUMNS):
            continue
        participant_id = row[CSV_ID_COLUMN].strip()
        if not participant_id:
            raise ValueError(f"Dòng {line_number} thiếu mã người tham gia.")
        if len(participant_id) > 64 or not participant_id.isprintable():
            raise ValueError(
                f"Dòng {line_number}: mã người tham gia phải có tối đa 64 ký tự in được."
            )
        if participant_id in seen_ids:
            raise ValueError(f"Dòng {line_number}: mã người tham gia bị lặp.")
        seen_ids.add(participant_id)

        raw_scores: dict[str, list[int]] = {}
        for chakra in CHAKRAS:
            values_for_chakra: list[int] = []
            for question in range(1, 6):
                value = row[f"{chakra}_{question}"].strip()
                if not value:
                    continue
                try:
                    values_for_chakra.append(int(value))
                except ValueError as exc:
                    raise ValueError(
                        f"Dòng {line_number}, {chakra}_{question}: "
                        "điểm phải là số nguyên từ 0 đến 4 hoặc để trống."
                    ) from exc
            if values_for_chakra:
                raw_scores[chakra] = values_for_chakra
        participants.append(
            {
                "ma_nguoi_tham_gia": participant_id,
                "scores": validate_scores(raw_scores),
            }
        )

    if not participants:
        raise ValueError("Tệp CSV chưa có người tham gia với câu trả lời.")
    return participants


def score(raw: dict[str, list[int]]) -> list[ScoreRow]:
    rows: list[ScoreRow] = []
    for key, values in raw.items():
        average = sum(values) / len(values)
        rows.append(
            {
                "khoa": key,
                "ten": CHAKRAS[key],
                "so_cau": len(values),
                "diem_trung_binh": round(average, 2),
            }
        )
    return rows


def score_participants(
    participants: list[ParticipantScores],
) -> tuple[list[ParticipantResult], list[GroupRow]]:
    individual_results: list[ParticipantResult] = []
    group_scores: dict[str, list[float]] = {key: [] for key in CHAKRAS}
    for participant in participants:
        results = score(participant["scores"])
        individual_results.append(
            {"ma_nguoi_tham_gia": participant["ma_nguoi_tham_gia"], "ket_qua": results}
        )
        for key, values in participant["scores"].items():
            group_scores[key].append(sum(values) / len(values))

    group_summary: list[GroupRow] = []
    for key, values in group_scores.items():
        if values:
            group_summary.append(
                {
                    "khoa": key,
                    "ten": CHAKRAS[key],
                    "so_nguoi": len(values),
                    "diem_trung_binh": round(sum(values) / len(values), 2),
                }
            )
    return individual_results, group_summary


def csv_template() -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    writer.writerow(("P01", *("" for _ in CSV_SCORE_COLUMNS)))
    writer.writerow(("P02", *("" for _ in CSV_SCORE_COLUMNS)))
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tính điểm tự phản tỉnh cho bảy chủ đề luân xa, không dùng để chẩn đoán."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--json", help="Dữ liệu JSON, ví dụ: '{\"root\":[2,3,1]}'")
    source.add_argument("--file", type=Path, help="Tệp JSON một người hoặc CSV nhiều người")
    source.add_argument("--mau", action="store_true", help="In mẫu JSON trống")
    source.add_argument("--mau-csv", action="store_true", help="In mẫu CSV cho nhiều người")
    parser.add_argument("--dinh-dang", choices=("van-ban", "json"), default="van-ban")
    args = parser.parse_args()

    if args.mau_csv:
        print(csv_template(), end="")
        return 0

    if args.mau:
        print(
            json.dumps(
                {key: [None, None, None, None, None] for key in CHAKRAS},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    try:
        if args.file is not None and args.file.suffix.lower() == ".csv":
            participants = validate_csv_scores(args.file.read_text(encoding="utf-8-sig"))
            individual_results, group_summary = score_participants(participants)
            if args.dinh_dang == "json":
                print(
                    json.dumps(
                        {
                            "ca_nhan": individual_results,
                            "tong_hop_nhom": group_summary,
                            "luu_y": (
                                "Điểm tự báo cáo chỉ gợi ý chủ đề phản tỉnh; "
                                "bộ câu hỏi chưa được kiểm định tâm trắc."
                            ),
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                return 0
            print("KẾT QUẢ TỰ PHẢN TỈNH THEO MÃ NGƯỜI THAM GIA")
            print("Dùng mã thay tên; không dùng kết quả để chẩn đoán hoặc xếp hạng.\n")
            for participant in individual_results:
                print(f"{participant['ma_nguoi_tham_gia']}:")
                for row in participant["ket_qua"]:
                    print(
                        f"- {row['ten']}: {row['diem_trung_binh']}/4 "
                        f"({row['so_cau']}/5 câu đã trả lời)"
                    )
            print("\nTỔNG HỢP NHÓM (trung bình tự báo cáo; N là số người có câu trả lời)")
            for row in group_summary:
                print(f"- {row['ten']}: {row['diem_trung_binh']}/4 (N={row['so_nguoi']})")
            print(
                "\nĐiểm chỉ gợi ý chủ đề để tự phản tỉnh tại thời điểm trả lời; "
                "không có ngưỡng đánh giá đã được kiểm định."
            )
            return 0

        if args.json is not None:
            raw = json.loads(args.json)
        else:
            raw = json.loads(args.file.read_text(encoding="utf-8"))
        rows = score(validate_scores(raw))
    except (OSError, csv.Error, json.JSONDecodeError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2

    if args.dinh_dang == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    print("KẾT QUẢ TỰ PHẢN TỈNH — không phải chẩn đoán")
    print("Điểm trung bình tự báo cáo (0–4); không có ngưỡng đánh giá đã được kiểm định.\n")
    for row in rows:
        print(f"- {row['ten']}: {row['diem_trung_binh']}/4 ({row['so_cau']} câu đã trả lời)")
    print(
        "\nBạn có thể chọn chủ đề phù hợp với nhu cầu của mình, không nhất thiết là điểm thấp nhất."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
