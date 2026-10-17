#!/usr/bin/env python3
"""Tạo khung lộ trình 365 ngày theo chu kỳ bảy luân xa."""

from __future__ import annotations

import argparse
from pathlib import Path

CHAKRAS = (
    "Gốc rễ",
    "Xương cùng",
    "Đám rối mặt trời",
    "Tim",
    "Cổ họng",
    "Con mắt thứ ba",
    "Vương miện",
)

TEMPLATE = """## Ngày {day}: {chakra}

- Câu khẳng định:
- Câu hỏi tự phản tỉnh:
- Hành động nhỏ trong 5–15 phút:
- Mức được nâng đỡ (0–4):
- Ghi nhận:

"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Tạo khung lộ trình 365 ngày cho bảy luân xa.")
    parser.add_argument("-o", "--output", type=Path, default=Path("lo-trinh-365-ngay.md"))
    args = parser.parse_args()

    parts = [
        "# Lộ trình 365 ngày theo bảy luân xa\n\n",
        "Đây là khung tự phản tỉnh, không phải chương trình điều trị. Chọn nội dung phù hợp và nghỉ khi cần.\n\n",
    ]
    for day in range(1, 366):
        chakra = "Tổng kết năm" if day == 365 else CHAKRAS[(day - 1) % len(CHAKRAS)]
        parts.append(TEMPLATE.format(day=day, chakra=chakra))
    args.output.write_text("".join(parts), encoding="utf-8")
    print(f"Đã tạo {args.output} với 365 ngày.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
