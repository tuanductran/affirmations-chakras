# Hướng dẫn cho công cụ AI

## Phạm vi và ngôn ngữ

- Đọc `SKILL.md` trước khi chỉnh sửa nội dung để tuân thủ mục đích, quy trình và giới hạn an toàn
  của repository.
- Viết tài liệu hướng đến người dùng bằng tiếng Việt tự nhiên, rõ ràng và không phán xét. Giữ nguyên
  tên file và mã định danh hiện có.
- Tôn trọng cách tổ chức hiện tại: nội dung dùng chung trong `references/`, mỗi mô-đun luân xa trong
  một file tham chiếu, câu hỏi trong `question-banks/`, mã thực thi trong `scripts/`, kiểm thử trong
  `tests/`.
- Giữ các liên kết tương đối giữa tài liệu và cập nhật liên kết khi đổi tên hoặc di chuyển file.
- Làm theo `CONTRIBUTING.md` khi chuẩn bị thay đổi; báo cáo lỗ hổng theo `SECURITY.md`, không đăng
  chi tiết khai thác công khai.

## An toàn và độ chính xác

- Trình bày luân xa như một khung biểu tượng để tự phản tỉnh, không phải giải phẫu, cơ chế sinh học
  đã được xác nhận, công cụ chẩn đoán hay phương pháp điều trị.
- Không tuyên bố câu khẳng định, điểm số, thiền hoặc thực hành luân xa chữa bệnh, bảo đảm kết quả
  hay thay thế chăm sóc y tế/sức khỏe tâm thần.
- Gọi điểm số là tự báo cáo tại một thời điểm hoặc gợi ý chủ đề thực hành; không gọi điểm thấp là
  luân xa “tắc”, “hỏng” hay “mất cân bằng”.
- Giữ quyền lựa chọn của người dùng. Không ép hình dung màu sắc, niềm tin, tha thứ, hồi tưởng sang
  chấn hoặc tiếp tục bài tập gây khó chịu.
- Với nội dung về khủng hoảng, tự hại, bạo lực, sang chấn hoặc triệu chứng y khoa, ưu tiên an toàn
  và hỗ trợ phù hợp; không tâm linh hóa hay trò chơi hóa nguy cơ.
- Không thêm tuyên bố sức khỏe hoặc nghiên cứu mới nếu không có nguồn đáng tin cậy, liên kết kiểm
  chứng được và mô tả đúng giới hạn của bằng chứng. Cập nhật danh mục trong
  `references/foundations-and-evidence.md` khi thêm nguồn.

## Quy tắc biên tập

- Mỗi ngân hàng câu hỏi hiện có 15 câu tự phản tỉnh và 5 câu tự đánh giá. Nếu thay đổi số lượng hoặc
  cấu trúc, cập nhật kiểm thử có liên quan và nêu rõ thay đổi chủ đích.
- Giữ câu hỏi và câu khẳng định cụ thể, có tính lựa chọn, không phán xét và không đòi hỏi người dùng
  tiết lộ trải nghiệm nhạy cảm.
- Không thêm phụ thuộc lúc chạy nếu thư viện chuẩn đáp ứng được yêu cầu; các công cụ lint, định dạng
  và kiểm thử chỉ được đặt trong nhóm phụ thuộc phát triển. Bảo toàn giao diện dòng lệnh hiện có và
  thông báo lỗi rõ ràng.
- Quản lý phiên bản Python tối thiểu bằng `requires-python` trong `pyproject.toml` và các lệnh CLI;
  chỉ ghim phụ thuộc phát triển trong `uv.lock`, không ghim phiên bản Python mặc định. Không thêm
  hoặc commit môi trường `.venv`.
- Khi đổi phụ thuộc, cập nhật lock bằng `uv lock`; xác minh đồng bộ với
  `uv sync --locked --all-groups`.
- Giữ mã Python đạt `uv run --locked ruff check .` và `uv run --locked ruff format --check .`.
- Giữ tài liệu đạt
  `uv run --locked mdformat --check --number --wrap 100 README.md AGENTS.md CONTRIBUTING.md SECURITY.md SKILL.md question-banks references`
  và
  `uv run --locked pymarkdown --enable-extensions front-matter -d MD013 scan -r . --respect-gitignore`.
- Giữ kiểm tra kiểu đạt `uv run --locked ty check scripts tests`, độ bao phủ đạt ít nhất 85% bằng
  `uv run --locked pytest --cov=scripts --cov-report=term-missing --cov-fail-under=85`, và phụ thuộc
  không có lỗ hổng đã biết bằng `uv run --locked pip-audit`.
- Chỉ sửa những phần cần thiết cho yêu cầu; không xóa nội dung hoặc thay đổi lịch sử Git khi chưa
  được yêu cầu cụ thể.

## Kiểm tra thay đổi

- Chạy kiểm thử với `uv run --locked pytest` khi thay đổi mã, cấu trúc ngân hàng câu hỏi hoặc các
  liên kết được kiểm tra; cấu hình pytest mặc định cũng yêu cầu coverage scripts tối thiểu 85%.
- Trước khi hoàn tất thay đổi Python hoặc Markdown, chạy kiểm thử/coverage, Ruff, kiểm tra kiểu,
  kiểm toán phụ thuộc, Markdown lint/format và `uv build`.
- Khi chỉnh script, kiểm tra cả cách dùng phù hợp và định dạng đầu ra liên quan; không commit tệp
  kết quả sinh ra hoặc dữ liệu riêng tư.
- Nếu không chạy được một kiểm tra, báo rõ lệnh và nguyên nhân thay vì khẳng định kiểm tra đã đạt.
