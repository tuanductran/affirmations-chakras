# Đóng góp

Cảm ơn bạn đã quan tâm đóng góp. Mọi thay đổi nên giữ nội dung chính xác, dễ kiểm chứng và tôn trọng
quyền lựa chọn của người đọc.

## Bắt đầu

- Cài [uv](https://docs.astral.sh/uv/getting-started/installation/) và Python 3.10 trở lên.
- Đồng bộ môi trường phát triển bằng `uv sync --all-groups`.
- Tạo nhánh riêng từ `main`; mở pull request với mô tả mục đích, thay đổi và các kiểm tra đã chạy.

## Nguyên tắc nội dung

- Trình bày luân xa như khung biểu tượng để tự phản tỉnh, không phải cấu trúc y khoa hay công cụ
  chẩn đoán.
- Không hứa hẹn chữa bệnh, bảo đảm kết quả hoặc thay thế chăm sóc y tế/sức khỏe tâm thần.
- Dùng ngôn ngữ tiếng Việt tự nhiên, không phán xét; tôn trọng khả năng bỏ qua hoặc điều chỉnh bài
  tập của người đọc.
- Khi bổ sung thông tin về sức khỏe, tâm lý hoặc nguồn gốc truyền thống, dẫn nguồn đáng tin cậy và
  ghi rõ giới hạn của bằng chứng trong `references/foundations-and-evidence.md`.
- Nếu đổi câu hỏi, giữ nội dung tương ứng trong tài liệu tham chiếu và cập nhật kiểm thử số lượng.

## Kiểm tra trước khi gửi

Chạy các kiểm tra tương ứng với thay đổi. Bộ lệnh đầy đủ được dùng trong CI:

```sh
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked ty check scripts tests
uv run --locked mdformat --check --number --wrap 100 README.md AGENTS.md CONTRIBUTING.md SECURITY.md SKILL.md question-banks references .agents/skills
uv run --locked pymarkdown --enable-extensions front-matter -d MD013 scan -r . --respect-gitignore
uv run --locked pip-audit --skip-editable
uv lock --check
uv build
```

Nếu sửa phụ thuộc, cập nhật `uv.lock` bằng `uv lock` và xác minh `uv sync --locked --all-groups`.
Không commit `.venv`, dữ liệu cá nhân, bí mật hoặc tệp đầu ra được tạo tự động. Khi không thể chạy
một kiểm tra, ghi rõ kiểm tra nào chưa chạy và lý do trong pull request.
