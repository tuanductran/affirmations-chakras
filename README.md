# Hệ thống câu khẳng định theo 7 luân xa

Repository này cung cấp một **kỹ năng hướng dẫn tự phản tỉnh bằng tiếng Việt**, sử dụng bảy luân xa như các chủ đề biểu tượng: an toàn, cảm xúc, tự tin, lòng trắc ẩn, giao tiếp, sáng suốt và ý nghĩa. Nội dung gồm câu khẳng định, câu hỏi gợi mở, bài thực hành nhẹ nhàng và các công cụ Python nhỏ.

Đây không phải công cụ chẩn đoán hay điều trị. Các điểm số chỉ phản ánh tự đánh giá tại một thời điểm; không mô tả luân xa hoặc tình trạng sức khỏe. Không dùng nội dung để thay thế chăm sóc y tế hoặc sức khỏe tâm thần. Xem [nền tảng, phạm vi và bằng chứng](references/foundations-and-evidence.md) và [quy tắc an toàn](references/practices.md#quy-tắc-an-toàn) trước khi sử dụng.

## Bắt đầu

1. Đọc [`SKILL.md`](SKILL.md) để biết mục đích, nguyên tắc an toàn và quy trình sử dụng.
2. Chọn một trong bảy mô-đun tham chiếu: [Gốc rễ](references/root-chakra.md), [Xương cùng](references/sacral-chakra.md), [Đám rối mặt trời](references/solar-plexus-chakra.md), [Tim](references/heart-chakra.md), [Cổ họng](references/throat-chakra.md), [Con mắt thứ ba](references/third-eye-chakra.md) hoặc [Vương miện](references/crown-chakra.md).
3. Chọn 3–5 câu trong ngân hàng câu hỏi của mô-đun, một câu khẳng định và một hành động nhỏ. Bỏ qua hoặc điều chỉnh bất cứ nội dung nào không phù hợp.

## Nội dung repository

- `SKILL.md` — hướng dẫn chính cho kỹ năng và liên kết đến tài liệu chi tiết.
- `references/` — bảy mô-đun luân xa cùng tài liệu về nền tảng, an toàn, thực hành và lộ trình 365 ngày.
- `question-banks/` — mỗi luân xa có 15 câu hỏi tự phản tỉnh và 5 câu tự đánh giá.
- `scripts/score_chakras.py` — tính điểm tự báo cáo từ 0–4; xuất văn bản hoặc JSON.
- `scripts/generate_365_day_plan.py` — tạo khung nhật ký thực hành 365 ngày.
- `tests/` — kiểm tra metadata, liên kết, số lượng câu hỏi và hai script.
- `AGENTS.md` — quy tắc dành cho công cụ AI khi đọc hoặc sửa repository.

## Công cụ

Cần Python 3.10 trở lên; các script chỉ dùng thư viện chuẩn.

Tạo mẫu dữ liệu chấm điểm:

```sh
python scripts/score_chakras.py --mau
```

Tính điểm và nhận kết quả JSON:

```sh
python scripts/score_chakras.py \
  --json '{"root":[0,2,4]}' \
  --dinh-dang json
```

Tạo khung thực hành 365 ngày:

```sh
python scripts/generate_365_day_plan.py --output lo-trinh-365-ngay.md
```

Chạy kiểm thử (cần `pytest`):

```sh
python -m pytest -q
```

## Nguồn tham khảo

Các nguồn và giới hạn bằng chứng được ghi trong [references/foundations-and-evidence.md](references/foundations-and-evidence.md). Tài liệu này phân biệt khung luân xa mang tính truyền thống/biểu tượng với nghiên cứu tâm lý về tự khẳng định và hướng dẫn về thiền; không diễn giải các nghiên cứu đó thành bằng chứng rằng luân xa là cấu trúc y khoa.

## Giấy phép

Repository được phát hành theo giấy phép [MIT](LICENSE).
