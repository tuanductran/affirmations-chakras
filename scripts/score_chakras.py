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
import json
import sys
from pathlib import Path
from typing import TypedDict


class ScoreRow(TypedDict):
    khoa: str
    ten: str
    so_cau: int
    diem_trung_binh: float
    phan_tram: float
    muc_goi_y: str


CHAKRAS = {
    "root": "Gốc rễ",
    "sacral": "Xương cùng",
    "solar_plexus": "Đám rối mặt trời",
    "heart": "Tim",
    "throat": "Cổ họng",
    "third_eye": "Con mắt thứ ba",
    "crown": "Vương miện",
}

LEVELS = (
    (0, "cần được nâng đỡ"),
    (25, "đang được khám phá"),
    (50, "khá được nâng đỡ"),
    (75, "đang vững vàng"),
)


def level_for(percent: float) -> str:
    for lower_bound, label in reversed(LEVELS):
        if lower_bound <= percent <= 100:
            return label
    return "chưa đủ dữ liệu"


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
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"Điểm của {key} phải là số nguyên từ 0 đến 4.")
            if value < 0 or value > 4:
                raise ValueError(f"Điểm của {key} phải nằm trong khoảng 0 đến 4.")
            clean.append(value)
        result[key] = clean
    return result


def score(raw: dict[str, list[int]]) -> list[ScoreRow]:
    rows: list[ScoreRow] = []
    for key, values in raw.items():
        average = sum(values) / len(values)
        percent = round(average / 4 * 100, 1)
        rows.append(
            {
                "khoa": key,
                "ten": CHAKRAS[key],
                "so_cau": len(values),
                "diem_trung_binh": round(average, 2),
                "phan_tram": percent,
                "muc_goi_y": level_for(percent),
            }
        )
    return sorted(rows, key=lambda row: (row["phan_tram"], row["khoa"]))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tính điểm tự phản tỉnh cho bảy chủ đề luân xa, không dùng để chẩn đoán."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--json", help="Dữ liệu JSON, ví dụ: '{\"root\":[2,3,1]}'")
    source.add_argument("--file", type=Path, help="Tệp JSON chứa điểm số")
    source.add_argument("--mau", action="store_true", help="In mẫu JSON trống")
    parser.add_argument("--dinh-dang", choices=("van-ban", "json"), default="van-ban")
    args = parser.parse_args()

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
        if args.json is not None:
            raw = json.loads(args.json)
        else:
            raw = json.loads(args.file.read_text(encoding="utf-8"))
        rows = score(validate_scores(raw))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2

    if args.dinh_dang == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    print("KẾT QUẢ TỰ PHẢN TỈNH — không phải chẩn đoán")
    print("Thứ tự dưới đây đi từ điểm thấp đến điểm cao để gợi ý chủ đề nên khám phá trước.\n")
    for row in rows:
        print(
            f"- {row['ten']}: {row['phan_tram']}% "
            f"(trung bình {row['diem_trung_binh']}/4; {row['muc_goi_y']})"
        )
    if rows:
        print(f"\nChủ đề có điểm thấp nhất để bắt đầu: {rows[0]['ten']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
