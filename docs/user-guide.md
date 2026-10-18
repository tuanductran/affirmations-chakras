# Hướng dẫn người dùng

## Chọn cách bắt đầu

1. Đọc [nguyên tắc và giới hạn](../SKILL.md).
2. Chọn một mô-đun trong [bảy tài liệu luân xa](../references/).
3. Chọn 3–5 câu hỏi trong ngân hàng tương ứng, một câu khẳng định và một hành động nhỏ.
4. Bỏ qua hoặc điều chỉnh bất kỳ nội dung nào không phù hợp.

Luân xa được dùng như khung biểu tượng để tự phản tỉnh, không phải cấu trúc y khoa hay chẩn đoán.
Không cần theo một niềm tin, hình dung màu sắc hoặc chia sẻ trải nghiệm riêng tư.

## Dùng công cụ chấm điểm

Cài [uv](https://docs.astral.sh/uv/) và đồng bộ môi trường:

```sh
uv sync --locked --all-groups
```

Tạo mẫu JSON cho một người:

```sh
uv run score-chakras --mau
```

Truyền dữ liệu JSON trực tiếp hoặc dùng `--file` với tệp JSON. Mỗi điểm đã trả lời là số nguyên 0–4;
`null` được bỏ qua. Đầu ra là trung bình thô trên thang 0–4 và số câu đã trả lời.

Để tổ chức câu trả lời nhóm, tạo mẫu CSV:

```sh
uv run score-chakras --mau-csv > quiz.local.csv
uv run score-chakras --file quiz.local.csv
```

Mỗi hàng là một người, mỗi cột điểm có tên theo dạng `<ma_luan_xa>_<so_cau>`, từ 1 đến 5. Nhập điểm
0–4; để trống câu không muốn trả lời. Hàng không có câu trả lời nào sẽ được bỏ qua. Có thể xem dữ
liệu minh họa tại [`examples/group-quiz-responses.csv`](../examples/group-quiz-responses.csv).

## Hiểu kết quả và bảo vệ riêng tư

Điểm là tự báo cáo cho một thời điểm, không có ngưỡng tốt/xấu và không xếp hạng. Điểm nhóm là trung
bình câu trả lời của những người đã trả lời chủ đề đó; `N` là số người được tính. Không suy luận
tình trạng sức khỏe hoặc đặc điểm ổn định của một người từ điểm.

Trong khảo sát nhóm, dùng mã thay tên, không đưa email hoặc dữ kiện nhận dạng vào CSV. Mã thay tên
không bảo đảm ẩn danh nếu có thể ghép với danh sách khác. Chỉ chia sẻ tệp và kết quả với người phù
hợp, lưu ở nơi an toàn và xóa khi không còn cần. Công cụ chỉ xử lý tệp cục bộ, không tự gửi dữ liệu.

## Mẫu thực hành

Sao chép [`templates/reflection-session.md`](../templates/reflection-session.md) để ghi một phiên tự
phản tỉnh. Ví dụ đã điền nằm ở
[`examples/reflection-session.md`](../examples/reflection-session.md). Không bắt buộc trả lời câu
hỏi hoặc hoàn thành bài tập; dừng nếu thấy khó chịu.

Nếu đang gặp nguy hiểm hoặc khủng hoảng, ưu tiên tìm hỗ trợ từ người tin cậy, chuyên gia phù hợp
hoặc dịch vụ khẩn cấp tại nơi bạn sống; không dùng quiz để quyết định chăm sóc.
