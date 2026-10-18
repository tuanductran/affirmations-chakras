# Hệ thống câu khẳng định theo 7 luân xa

Repository này cung cấp một **kỹ năng hướng dẫn tự phản tỉnh bằng tiếng Việt**, sử dụng bảy luân xa
như các chủ đề biểu tượng: an toàn, cảm xúc, tự tin, lòng trắc ẩn, giao tiếp, sáng suốt và ý nghĩa.
Nội dung gồm câu khẳng định, câu hỏi gợi mở, bài thực hành nhẹ nhàng và các công cụ Python nhỏ.

Đây không phải công cụ chẩn đoán hay điều trị. Các điểm số chỉ phản ánh tự đánh giá tại một thời
điểm; không mô tả luân xa hoặc tình trạng sức khỏe. Không dùng nội dung để thay thế chăm sóc y tế
hoặc sức khỏe tâm thần. Xem
[nền tảng, phạm vi và bằng chứng](references/foundations-and-evidence.md) và
[quy tắc an toàn](references/practices.md#quy-t%E1%BA%AFc-an-to%C3%A0n) trước khi sử dụng.

## Bắt đầu

1. Đọc [`SKILL.md`](SKILL.md) để biết mục đích, nguyên tắc an toàn và quy trình sử dụng.
2. Chọn một trong bảy mô-đun tham chiếu: [Gốc rễ](references/root-chakra.md),
   [Xương cùng](references/sacral-chakra.md), [Đám rối mặt trời](references/solar-plexus-chakra.md),
   [Tim](references/heart-chakra.md), [Cổ họng](references/throat-chakra.md),
   [Con mắt thứ ba](references/third-eye-chakra.md) hoặc [Vương miện](references/crown-chakra.md).
3. Chọn 3–5 câu trong ngân hàng câu hỏi của mô-đun, một câu khẳng định và một hành động nhỏ. Bỏ qua
   hoặc điều chỉnh bất cứ nội dung nào không phù hợp.

Đọc thêm [thực hành câu khẳng định nâng cao](references/affirmation-practice.md) khi muốn dùng hình
dung, điều chỉnh cảm xúc, nhịp đọc hoặc nghi thức theo cách an toàn và có thể dừng bất cứ lúc nào.

Xem [tài liệu dự án](docs/README.md) để chọn hướng dẫn người dùng, nhà phát triển hoặc kiểm thử; các
mẫu điền sẵn nằm trong [`templates/`](templates/) và dữ liệu minh họa tổng hợp nằm trong
[`examples/`](examples/).

## Nội dung repository

- `SKILL.md` — hướng dẫn chính cho kỹ năng và liên kết đến tài liệu chi tiết.
- `references/` — bảy mô-đun luân xa cùng tài liệu về nền tảng, an toàn, thực hành và lộ trình 365
  ngày; có thêm tài liệu thực hành câu khẳng định nâng cao.
- `question-banks/` — mỗi luân xa có 15 câu hỏi tự phản tỉnh và 5 câu tự đánh giá.
- `scripts/score_chakras.py` — chấm tự báo cáo một người bằng JSON hoặc nhiều người bằng CSV.
- `scripts/generate_365_day_plan.py` — tạo khung nhật ký thực hành 365 ngày.
- `tests/` — kiểm tra metadata, liên kết, số lượng câu hỏi và hai script.
- `docs/` — hướng dẫn cho người dùng, nhà phát triển và người kiểm thử.
- `templates/` — mẫu phiên tự phản tỉnh và tự rà soát tuần.
- `examples/` — dữ liệu điểm JSON/CSV giả và ví dụ phiên đã điền.
- `AGENTS.md` — quy tắc dành cho công cụ AI khi đọc hoặc sửa repository.
- `.agents/skills/` — các quy trình chuyên biệt theo
  [định dạng Agent Skills](https://agentskills.io/specification) cho tác vụ biên tập nội dung và bảo
  trì Python/Markdown.
  [Codex phát hiện skills repository ở vị trí này](https://developers.openai.com/codex/skills/); các
  agent khác có thể cần cấu hình hoặc dùng vị trí riêng.
- `CONTRIBUTING.md` — hướng dẫn đóng góp và kiểm tra trước khi tạo pull request.
- `SECURITY.md` — phạm vi hỗ trợ và cách báo cáo lỗ hổng riêng tư.

## Cài đặt và sử dụng với uv

Cài [uv](https://docs.astral.sh/uv/getting-started/installation/) nếu máy chưa có. uv tự chọn Python
tương thích với yêu cầu `>=3.10` trong `pyproject.toml`, tải Python nếu cần và tạo môi trường cô lập
`.venv`. CI kiểm thử Python 3.10, 3.12 và bản ổn định mới nhất 3.15.

```sh
uv python install 3.15
uv sync --all-groups
```

Hai lệnh CLI được cài trong môi trường dự án:

```sh
uv run score-chakras --mau
uv run generate-chakra-plan --output lo-trinh-365-ngay.md
```

Chấm điểm trực tiếp và nhận kết quả JSON:

```sh
uv run score-chakras \
  --json '{"root":[0,2,4]}' \
  --dinh-dang json
```

Hoặc đọc dữ liệu từ file JSON bằng `--file scores.json`. Mỗi câu đã trả lời phải là số nguyên từ 0
đến 4; giá trị `null` được bỏ qua. Kết quả là điểm trung bình thô trên thang 0–4 và số câu đã trả
lời, không có ngưỡng hoặc xếp hạng. Bộ câu hỏi này là công cụ tự phản tỉnh, chưa được kiểm định như
thang đo tâm lý hay đánh giá sức khỏe.

Có thể sao chép `score_example.json` thành `score.json`, chỉnh sửa điểm rồi chạy
`--file score.json`. Tệp `score.json` bị Git bỏ qua và không được commit; chỉ commit tệp mẫu
`score_example.json`.

### Dùng quiz với nhiều người

Tạo mẫu CSV rồi mở bằng ứng dụng bảng tính:

```sh
uv run score-chakras --mau-csv > quiz.local.csv
```

Mỗi dòng là một người; dùng mã thay tên như `P01`, không nhập tên, email hoặc thông tin có thể nhận
dạng người trả lời. Các cột `root_1` đến `crown_5` khớp với 5 câu tự đánh giá trong từng ngân hàng
câu hỏi. Dựa trên 7 ngày gần đây, nhập điểm 0–4; để trống câu không muốn trả lời. Các dòng chưa có
câu trả lời nào được tự động bỏ qua. Sau đó chạy:

```sh
uv run score-chakras --file quiz.local.csv
```

Kết quả gồm điểm riêng theo mã và trung bình nhóm cho từng chủ đề; `N` cho biết số người đã trả lời
ít nhất một câu thuộc chủ đề đó. Công cụ không xếp hạng người tham gia, không lưu hoặc gửi dữ liệu
đi nơi khác. Mã thay tên không bảo đảm ẩn danh nếu có thể liên kết với danh sách khác; chỉ chia sẻ
kết quả với người phù hợp, giữ tệp CSV an toàn và xóa khi không còn cần.

## Kiểm tra mã và Markdown

```sh
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

`mdformat` định dạng Markdown; `pymarkdownlnt` kiểm tra quy tắc Markdown (bỏ qua quy tắc độ dài dòng
MD013 để không làm hỏng câu tiếng Việt và liên kết dài). Pytest-cov đo độ bao phủ mã, `ty` kiểm tra
kiểu dữ liệu và `pip-audit` rà lỗ hổng trong các phụ thuộc. Kiểm thử rà các liên kết và heading nội
bộ bên cạnh nội dung, CLI và trình tạo lịch. `uv.lock` ghim phụ thuộc phát triển để máy local và
GitHub Actions dùng cùng bộ công cụ. CI chạy kiểm thử, coverage, lint, kiểm tra kiểu, rà bảo mật,
Markdown và đóng gói trên các phiên bản Python trong ma trận.

## Nguồn tham khảo

Các nguồn và giới hạn bằng chứng được ghi trong
[references/foundations-and-evidence.md](references/foundations-and-evidence.md). Tài liệu này phân
biệt khung luân xa mang tính truyền thống/biểu tượng với nghiên cứu tâm lý về tự khẳng định và hướng
dẫn về thiền; không diễn giải các nghiên cứu đó thành bằng chứng rằng luân xa là cấu trúc y khoa.

## Giấy phép

Repository được phát hành theo giấy phép [MIT](LICENSE).

## Đóng góp và bảo mật

Xem [hướng dẫn đóng góp](CONTRIBUTING.md) trước khi tạo pull request. Nếu phát hiện vấn đề bảo mật,
hãy làm theo [chính sách bảo mật](SECURITY.md) và không đăng chi tiết khai thác công khai.
