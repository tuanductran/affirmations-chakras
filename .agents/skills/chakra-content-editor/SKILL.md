---
name: chakra-content-editor
description: "Use when authoring or reviewing this repository's Vietnamese chakra affirmations, reflection prompts, or wellness guidance; use for chakra content edits even when the request only says to improve wording or add a module."
license: MIT
---

# Biên tập nội dung luân xa

## Quy trình

1. Đọc `SKILL.md` ở gốc repository và `references/foundations-and-evidence.md`.
2. Với một mô-đun cụ thể, đọc tài liệu trong `references/` và ngân hàng tương ứng trong
   `question-banks/` trước khi sửa.
3. Giữ nội dung tiếng Việt tự nhiên, cụ thể, không phán xét và có quyền lựa chọn. Không buộc người
   đọc chia sẻ trải nghiệm nhạy cảm, hình dung màu sắc, theo một niềm tin hay tiếp tục bài tập gây
   khó chịu.
4. Trình bày luân xa như khung biểu tượng có cách diễn giải khác nhau giữa các truyền thống; không
   khẳng định luân xa là cấu trúc giải phẫu, cơ chế y sinh, chẩn đoán hay phương pháp điều trị.
5. Viết câu khẳng định có thể tin được, thiên về quá trình và gắn với lựa chọn hoặc hành động nhỏ.
   Tránh lời hứa chữa lành/chữa bệnh, bảo đảm kết quả, phủ nhận nguy hiểm, áp đặt tha thứ hoặc nói
   rằng suy nghĩ quyết định bệnh tật, an toàn hay sự sung túc.
6. Khi nêu thông tin thực chứng, tra nguồn đáng tin cậy, kiểm tra nguồn gốc và giới hạn của nghiên
   cứu; cập nhật `references/foundations-and-evidence.md`. Không sao chép câu chữ từ nguồn; diễn đạt
   lại ngắn gọn và dẫn nguồn.
7. Mỗi ngân hàng hiện có 15 câu tự phản tỉnh và 5 câu tự đánh giá. Nếu đổi số lượng, cập nhật kiểm
   thử và mọi mô tả số lượng có liên quan.

## Kiểm tra

```sh
uv run --locked pytest
uv run --locked mdformat --check --number --wrap 100 README.md AGENTS.md CONTRIBUTING.md SECURITY.md SKILL.md question-banks references .agents/skills
uv run --locked pymarkdown --enable-extensions front-matter -d MD013 scan -r . --respect-gitignore
```

Nếu sửa mã hoặc nguồn phụ thuộc, làm theo `CONTRIBUTING.md` và chạy các kiểm tra Python đầy đủ.
