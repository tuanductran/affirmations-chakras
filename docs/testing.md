# Hướng dẫn kiểm thử

## Kiểm tra cục bộ

Kích hoạt `.venv` hoặc dùng `uv run`; trước tiên đồng bộ dependency đã khóa:

```sh
uv sync --locked --all-groups
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked ty check scripts tests
git ls-files -co --exclude-standard -z -- '*.md' | xargs -0 uv run --locked mdformat --check
uv run --locked pymarkdown scan -r . --respect-gitignore
uv run --locked pip-audit --skip-editable
uv lock --check
uv build
```

Pytest yêu cầu coverage của `scripts/` ít nhất 85%. Workflow CI chạy các kiểm tra Python/Markdown,
kiểm toán dependency và build trên Python 3.10, 3.12, 3.15; kiểm toán dependency và smoke test wheel
chạy trên Python 3.12.

## Các đường đi cần kiểm tra khi thay đổi CLI

- `score-chakras --mau` tạo JSON gồm bảy chủ đề, mỗi chủ đề có năm ô trống.
- `score-chakras --mau-csv` tạo tiêu đề CSV phù hợp với năm câu mỗi chủ đề.
- Chấm một người bằng JSON hoặc tệp JSON; giá trị `null` được bỏ qua.
- Chấm nhiều người từ CSV; dòng chưa trả lời được bỏ qua, mã trùng và điểm không hợp lệ phải báo lỗi
  rõ ràng.
- Kết quả nhóm tính trung bình mỗi người trước rồi lấy trung bình giữa những người có câu trả lời;
  `N` đếm số người được tính cho chủ đề.
- `generate-chakra-plan` tạo đủ 365 ngày trong một thư mục tạm.

Ví dụ đầu vào tổng hợp nằm trong [`examples/`](../examples/). Không đưa thông tin nhận dạng hoặc dữ
liệu nhạy cảm vào fixture, log hoặc ảnh chụp kiểm thử.

Thiết lập mdformat dùng
[`.mdformat.toml`](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html);
PyMarkdown đọc cấu hình từ `[tool.pymarkdown]` trong
[`pyproject.toml`](https://pymarkdown.readthedocs.io/en/latest/advanced_configuration/). Lệnh
mdformat lấy danh sách Markdown từ Git để tránh quét `.venv`, cache và tài liệu của các dependency
khi đi qua toàn bộ thư mục repository.
