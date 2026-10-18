# Hướng dẫn nhà phát triển

## Cấu trúc dự án

- `scripts/`: hai CLI Python dùng thư viện chuẩn.
- `tests/`: kiểm tra nội dung, liên kết, dữ liệu đầu vào và hành vi CLI.
- `question-banks/`: ngân hàng câu hỏi theo từng chủ đề.
- `references/`: hướng dẫn mô-đun, thực hành, an toàn và nguồn tham khảo.
- `docs/`: hướng dẫn cho người dùng, nhà phát triển và người kiểm thử.
- `templates/`: tài liệu trống để người dùng sao chép.
- `examples/`: dữ liệu giả và ví dụ đã điền.
- `.agents/skills/`: quy trình biên tập nội dung và bảo trì Python/Markdown.

## Thiết lập

Yêu cầu Python tối thiểu được khai báo trong `pyproject.toml`; CI hiện kiểm tra Python 3.10, 3.12 và
3.15. Dùng `uv` để đồng bộ môi trường tái lập:

```sh
uv sync --locked --all-groups
```

Không cài công cụ phát triển thành dependency lúc chạy. Không thêm thư viện ngoài khi thư viện chuẩn
đã đáp ứng yêu cầu.

## Nguyên tắc thay đổi

- Giữ giao diện CLI hiện có và báo lỗi đầu vào rõ ràng.
- Giữ nội dung sức khỏe thận trọng; cập nhật `references/foundations-and-evidence.md` khi bổ sung
  tuyên bố thực chứng.
- Không thêm dữ liệu người thật vào `examples/`; dùng mã giả và câu trả lời tổng hợp.
- Giữ liên kết tương đối giữa Markdown hợp lệ; khi thêm tài liệu mới, cập nhật `docs/README.md` và
  `README.md` nếu đó là điểm vào chính.
- Mẫu CSV phải khớp tiêu đề do `score-chakras --mau-csv` tạo.
- Thử nghiệm trình tạo tệp trong thư mục tạm để không ghi đè dữ liệu người dùng.

## Quy trình đóng góp

Đọc [`CONTRIBUTING.md`](../CONTRIBUTING.md), thực hiện kiểm tra trong
[hướng dẫn kiểm thử](testing.md), rồi xem lại `git diff` để bảo đảm không thêm `.venv`, dữ liệu
riêng tư hoặc tệp kết quả sinh tự động.
