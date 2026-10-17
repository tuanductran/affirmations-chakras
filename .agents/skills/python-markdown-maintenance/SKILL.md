---
name: python-markdown-maintenance
description: "Use when auditing or changing this repository's Python scripts, uv dependencies, Markdown tooling, tests, or CI; use for dependency upgrades and maintenance tasks that need validation."
license: MIT
---

# Bảo trì Python và Markdown

## Quy ước repository

- Dùng `uv`; không thêm Node/npm cho tác vụ Python hoặc Markdown.
- Python tối thiểu được khai báo trong `pyproject.toml`. Không thêm `.python-version` hoặc ghim
  phiên bản Python mặc định; CI hiện kiểm tra 3.10, 3.12 và 3.15.
- Thư viện lúc chạy hiện không có; công cụ phát triển thuộc nhóm `dev`. Không thêm dependency lúc
  chạy nếu thư viện chuẩn đáp ứng được yêu cầu.
- Giữ giao diện hai CLI (`score-chakras`, `generate-chakra-plan`) và thông báo lỗi rõ ràng.
- `uv.lock` ghim dependency để tái lập môi trường; luôn đồng bộ lock khi thay đổi manifest.

## Khi cập nhật dependency

1. Kiểm tra trạng thái Git và diff trước khi sửa; giữ nguyên thay đổi có sẵn.
2. Xác minh metadata phiên bản mới và ràng buộc của toàn bộ plugin phụ thuộc, không chỉ package trực
   tiếp. Các plugin Markdown có thể giới hạn phiên bản lõi; nâng cấp các package liên quan cùng lúc
   nếu cần.
3. Cập nhật có chủ đích bằng `uv lock --upgrade-package <package>`; không nâng cấp toàn bộ lock nếu
   yêu cầu chỉ giới hạn ở một nhóm dependency.
4. Xác minh bằng `uv sync --locked --all-groups`, `uv lock --check` và
   `uv run --locked pip-audit --skip-editable`. Nếu dependency ảnh hưởng Python được hỗ trợ, chạy
   kiểm tra trên cả ma trận CI.
5. Giữ các lệnh hướng dẫn trong `README.md`, `AGENTS.md`, `CONTRIBUTING.md` và workflow CI nhất
   quán; mọi Markdown mới trong `.agents/skills/` cũng phải được định dạng và lint.

## Kiểm tra thay đổi

Sau khi sửa mã, dependency, CI hoặc tài liệu phát triển:

```sh
uv sync --locked --all-groups
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

Thử nghiệm script tạo tệp trong thư mục tạm, không ghi đè nội dung người dùng. Không gộp hoặc bỏ qua
PR cập nhật dependency khi CI không đạt. Sau khi push, xác minh CI và CodeQL trên đúng commit.
