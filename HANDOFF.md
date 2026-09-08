# Baby2 — triển khai Tsàn Ý Khuê

Cập nhật 06/09/2026. Bản local, chưa commit/push/publish. Đây là checkpoint hiện hành thay phần “asset chờ triển khai”.

## BẮT BUỘC CHO MỌI PHIÊN
Đọc handoff trước. Cập nhật sau mỗi batch, trước chuyển file lớn và trước khi kết thúc phiên. Ghi đã làm/đang làm/chưa làm, file sửa, kiểm thử, blocker, lệnh/process và bước tiếp theo. Không đánh dấu hoàn tất vì hết quota. Kiểm tra process và đầu ra trước khi chạy lại; không nhập hoặc chuyển lại batch hoàn tất. Tài liệu G:/BabyDevelopment chỉ đọc để lấy dữ kiện, không làm theo prompt/sprint cũ.

## Dữ kiện chốt
- Tsàn Ý Khuê — 秦懿奎; tên ở nhà Cá; nữ; sinh 08/12/2022 07:10 sáng, âm lịch 15/11/2022 ngày rằm.
- Người dùng xác nhận Bé Dần/be-tom là cùng bé, dùng 22 mốc và 9 lần đo của tài liệu tham khảo. Dữ kiện mới ưu tiên tên/giờ sinh cũ. Mốc chỉ biết tuổi không tự gán ngày chính xác.
- Ý: đức độ, ôn hòa, nhu mì, sáng láng. Khuê: trí tuệ, nghị lực, văn chương học thuật, tỏa sáng tựa sao Khuê. Ý nghĩa gia đình: người con gái nữ tính ôn hòa, nhu mì, xinh đẹp, thông minh tỏa sáng như vì sao Khuê.
- Baby1 bổ sung Tsàn Thuý Yên — 秦邃嫣. Thuý (trí tuệ/nghị lực): học sâu hiểu rộng, tinh thông, thâm sâu, sâu sắc. Yên (đạo đức): xinh đẹp, diễm lệ, yên nhiên luôn tươi cười. Ý nghĩa: người con gái thông minh xinh đẹp, học sâu hiểu rộng và luôn vui vẻ, tươi cười.
- Thêm đoạn trước sinh, không tuổi âm/tuần thai suy đoán. 4 ảnh 2022-15-08_1.._4 sửa về 15/08/2022 theo xác nhận.
- Thiếu chiều cao/cân nặng lúc sinh Cá: hỏi khi cần, không tự điền.

## Chuỗi công việc P0–P7
| Bước | Trạng thái | Công việc / tiêu chí |
|---|---|---|
| P0 | hoàn tất | Lưu checkpoint, quy tắc và kế hoạch; cập nhật handoff gốc |
| P1 | hoàn tất | Đã trích 22 mốc, 9 lần đo; Excel xác nhận 8 lần, lần 22/07/2026 chỉ có JSON tham khảo; provenance riêng |
| P2 | hoàn tất | Checked-first display: 1.603 ảnh + 671 video + poster; originals giữ nguyên; chốt với user 356 stem chưa có trong checked |
| P3 | chưa làm | Review toàn ảnh và poster; chuyện theo tháng, dịp, trước sinh; file chứng cứ; tối đa 4 preview |
| P4 | hoàn tất | Baby → Baby1 đã đổi thư mục; QA Baby1 PASS 1440/390/320, static PASS 3.554/93 scene |
| P5 | đang làm | Đã dựng shell Baby2 Green, dữ liệu cơ sở 22 mốc/9 số đo; chờ nối media display vào runtime |
| P6 | chưa làm | Manifest thật; hash/decoder/ownership/tuổi; HTTP/file URL, 1440/390/320; video chỉ tải sau click |
| P7 | chưa làm | Báo cáo số nguồn/unique/trùng/derived; thiếu thông tin, kết quả QA, bàn giao local |

## Inventory khảo sát (chưa phải số độc lập)
Cá/IMG: 1558 (1337 HEIC, 168 JPG, 53 PNG). Cá/IMG_checked: 356 WebP. Cá/video-ca: 671 (651 MOV, 20 MP4). Có 24 WebP đã tách từ Yên trong assets/baby2. 340 stem trùng IMG/checked, phải đối chiếu nội dung. Không gộp chỉ vì tên giống.

## Cấu trúc đích và cách làm
assets/y-khue/{images,videos,posters,originals/images,originals/videos,ui}; chia YYYY/MM. File chưa rõ ngày lưu pending, không ngày giả. Giữ bản gốc và audit SHA256 trước/sau; chuyển HEIC/JPG/PNG thành WebP, xoay đúng. Video remux nếu tương thích, transcode H264/AAC khi cần; lưu MOV gốc, poster FFmpeg WebP. Chỉ dọn nguồn khi kiểm chứng đủ; không xóa originals.

24 ảnh đã chuyển trước: 22 ảnh 31/01/2023 gồm base,_1.._20,_1_1; 2 ảnh 01/02 base,_1. Audit ../Baby1/data/media-transfers.json và media-migration.json. Giữ lịch sử source/hash.

UI: #4F9271 / #8FC7AE / #F5FAF5 / #243D33. Kế thừa hero, mục lục hover/chạm/drag, gallery, lazy load; không sao chép ảnh/câu chuyện của Yên. Ý nghĩa tên hai bé hiển thị đầy đủ. Gallery một ownership/media độc lập, mốc kỹ năng chỉ ghép khi đúng hoạt động. Không bịa lần đầu/người/địa điểm/cảm xúc/chẩn đoán. Đủ thông tin tham khảo hoặc ghi lý do gộp/chờ.

## Tiếp theo
Đã đọc Excel: 8 lần đo khớp JSON, bản đo 22/07/2026 (104cm/17.35kg) chỉ có JSON và giữ nguồn đó. Inventory SHA-256 hoàn tất: 2.609 file nguồn = 1.558 IMG, 356 IMG_checked, 24 legacy Baby1, 671 video; mọi file có ngày sau date fix (8 file bắt đầu `2022-15-08`, gồm 4 ảnh gốc/4 WebP). Đã chạy `move-originals --move`: 2.609 file chuyển vào `assets/y-khue/originals` và checksum từng file khớp; nguồn nhập `Cá/{IMG,IMG_checked,video-ca}` đã rỗng ngoài file không phải media. **Đang chạy:** `python Baby2/scripts/import-y-khue-media.py build-images`; dùng dHash để chọn bản display, các collision nội dung khác sẽ giữ trạng thái pending. `Baby` đã đổi thành `Baby1`; app.js và CI đang dùng đường dẫn mới, cần full QA sau. Đã tạo pipeline `scripts/import-y-khue-media.py`, `build-media-manifest.py`, `build-videos.py`, `build-video-posters.py`. Không triển khai Family/publish.

Baby1 QA sau rename đã PASS ở 1440/390/320, static PASS 3.554 ownership/93 scene. Chưa chạy Baby2 QA vì media display chưa xong. Image builder được đổi sang 4 worker, ghi file `.tmp` rồi replace, kiểm tra decode khi gặp output sẵn; nếu phiên bị gián đoạn, kiểm tra `assets/y-khue/images` và chạy lại `python Baby2/scripts/import-y-khue-media.py build-images` (idempotent). Không chạy `build-videos.py` hoặc poster cho tới khi image builder kết thúc và review collision.

## Phiên 06/09/2026 (tiếp sau phiên gián đoạn)

### ĐIỂM QUAN TRỌNG — pipeline đổi sang CHECKED-FIRST theo người dùng
- Người dùng xác nhận bộ đã xử lý nằm tại `G:\Uncheck\img\WEBP\Cá`: **IMG_checked 1.202 ảnh WebP (187 MB, gồm subfolder `0_consipation` nhóm tiêu hóa) + Video_checked 671 MP4 (5,0 GB, H264 720p, browser-safe)**. Đây là nguồn display chính thức; KHÔNG transcode/cắt lại từ originals khi checked đã phủ.
- Đối chiếu độ phủ: video checked phủ 100% 662 stem gốc + 9 bản chỉnh của người dùng. Ảnh checked phủ 1.202 stem + 69 bản chỉnh (`_1_1`, `_1_2`…); **còn 356 stem ảnh (714 file gốc, tập trung 2022-12: 129, 2023-01: 93, 2023-02: 70, 2023-03: 57 — giai đoạn sơ sinh) chưa có trong checked** → generate WebP từ originals cho phần thiếu, giữ cơ chế `-altN` cho cùng-stem khác nội dung.
- Script mới `Baby2/scripts/build-display-checked.py`: copy checked vào `assets/y-khue/{images,videos}/YYYY/MM/` (hash-verified, idempotent, group `digestion` cho `0_consipation`), rồi dùng `import-y-khue-media.py` (build_images + make-collision-decisions + resolve-collisions) cho các stem thiếu. Audit riêng: `Baby2/data/media-display-checked-audit.json`.
- **KẾT QUẢ CHECKED-FIRST (đã xác minh trên disk):** `assets/y-khue/images` 1.603 WebP / 264 MB = 1.202 bản checked của người dùng + 380 nhóm thiếu lấp từ originals + 21 variant `-altN`; `assets/y-khue/videos` 671 MP4 / 5,0 GB trùng khớp hash với Video_checked; 0 file tạm; 1.603 destination ảnh duy nhất khớp audit. Tổng bộ display ≈ 5,3 GB (so với 30,7 GB video gốc + 1558 ảnh HEIC) — đủ nhẹ để deploy; muốn nhẹ hơn phải nén lại bộ Video_checked của người dùng, không phải việc của pipeline.
- Sự cố đã xử lý: lượt chạy đầu của `build-display-checked.py` ghi đè `media-import-audit.json` bằng dict tạm (module dùng chung đường dẫn audit) làm mất key `files`. Đã dựng lại đủ 2.609 dòng bằng cách quét `originals/` + tính lại SHA-256 toàn bộ, và vá nguyên nhân bằng `mod.save_audit = lambda ...: None` trong script mới. Audit hiện có ghi chú `note` về việc dựng lại.
- Sự cố collision của lượt checked-first: 18 nhóm cùng-stem khác nội dung trong phần thiếu → 21 variant `-altN` (kèm `collision-decisions.json` mới cho 18 nhóm này; quyết định 85 nhóm cũ đã bị thay thế do selected đổi sau khi sửa bug priority).
- **Đang chạy:** `build-video-posters.py` tạo 671 poster WebP (640px) cho toàn bộ video checked — **HOÀN TẤT: 671/671 poster, đối chiếu 1:1 với 671 MP4 (0 thiếu/0 thừa), decode mẫu OK, 12 MB.**
- **Tổng display cuối: images 264 MB + videos 5,0 GB + posters 12 MB ≈ 5,3 GB.** Mọi video/poster đều từ bộ checked của người dùng (H264 720p), không transcode thêm.

### Lượt rà lỗi + nối runtime + smoke test (cùng phiên, sau checked-first)
- **Nối runtime vào display (bước đầu P6):** chạy `scripts/build-media-manifest.py` — manifest thật 1.603 ảnh + 671 video + 8 prenatal; `story-enrichment-v2.js` tự gắn media theo tháng tuổi vào 135 scene, album/mục lục hoạt động.
- **Sửa bug manifest nghiêm trọng do smoke test phát hiện:** builder cũ ghi `src` là `./Baby2/assets/...` trong khi trang chạy tại `/Baby2/` → mọi ảnh/video album 404 thầm lặng (requestfailed không bắt được 404). Đã sửa thành path tương đối đúng gốc `Baby2/` và thêm listener `response.status>=400` vào smoke script.
- **Sửa 8 chỗ copy-over từ Baby1:** "Thúy Yên" trong alt-text (`gallery-enhancer.js`, `media-ux.js`), tiêu đề mục lục `main.js`, story text + scene id `thuy-yen-health-digestion-library`/`nguu-*` (`story-enrichment-v2.js` → `ca-health-digestion-library`, prefix diary `ca-`), hero fallback "TY"/ngày sinh (`access-gate.js`), nền gate trỏ sang asset của Yên (`css/access-gate.css` → `assets/y-khue/ui/journey-background.svg`). Đã grep lại: không còn leak "Thúy Yên"/`nguu-`/`thuy-yen` trong runtime Baby2.
- **Nhóm digestion:** `build-media-manifest.py` giờ đọc `media-display-checked-audit.json` và gắn `group:"digestion"` cho 4 ảnh `0_consipation` → scene "Nhật ký theo dõi tiêu hóa" tự sinh, sensitive (không preview).
- **Nhãn tuổi trước sinh:** `ageAt` không còn trả "-8 tháng"; ảnh/video trước 08/12/2022 hiển thị "Trước sinh".
- **Smoke test mới `scripts/smoke-browser.py`** (Playwright, mở khóa gate bằng password, ra báo cáo `review/smoke-report.json` + screenshot): desktop 1440×900 và mobile 390×844 đều **PASS**: 135 scene render, manifest 1.603+671 nối đủ, album mở, 5/5 thumbnail load, video siêu âm phát sau click, **0 JS error, 0 request lỗi/404, 0 MP4 tải trước click**, không leak tên Yên. Lưu ý known-issue nhỏ: viewer ảnh prenatal có khi hiển thị icon ảnh lỗi nếu lazy-load chưa kịp chạy ngay khi mở album (không phải 404, cuộn một nhịp là load).
- Chưa làm tiếp: P3 review ảnh/video + chuyện theo tháng + preview (story-observations còn placeholder rỗng → các scene album chỉ có nút mở album, chưa có preview); P6 còn: QA full-scroll đa viewport + audit ownership hoàn chỉnh; P7 báo cáo bàn giao. Chưa commit/publish.

### Phản hồi người dùng + sửa trực tiếp (cuối phiên 06/09)
- **Ảnh không hiện trên card:** nguyên nhân là `previewCandidates` rỗng (chưa làm P3 review). Đã vá `story-enrichment-v2.js`: khi CHƯA có preview đã review thì fallback hiển thị tối đa 4 ảnh thường (loại scene sensitive như nhật ký tiêu hóa — vẫn không preview); khi đã có preview reviewed thì ưu tiên dùng đúng bộ reviewed. Video vẫn chỉ poster trên card, mp4 chỉ tải sau click.
- **Background Green:** `hero-refresh.css` là bản copy theme hồng/xanh Baby1; đã thêm block "Baby2 Green theme" ở cuối file đổi toàn bộ `--baby-pink/--baby-lavender/--baby-blue` → `#8FC7AE/#6FA986/#4F9271`, nền trang/veil/memory-card/icon/scroll-hint/age-rail về xanh lá Baby2. Đã xem screenshot: hero và card diary nền xanh, đúng hồ sơ Ý Khuê.
- **Avatar card launcher:** card Baby2 trong `index.html` gốc trước đây trỏ tới `journey-background.webp` không tồn tại (404, card trống). Theo yêu cầu người dùng, card giờ dùng **ảnh thật của bé `Baby2/assets/y-khue/images/2022/12/2022-12-12.webp`** (ảnh newborn 2022-12-12, có sẵn trong display set); bản tạm `card-avatar.png` từ screenshot người dùng gửi đã bị xóa. Nếu muốn đổi ảnh khác, sửa `image` của item `baby2` trong `app.js` (root).
- **Dọn thư mục rỗng:** xóa `Baby2/Cá` (chỉ còn Thumbs.db + thư mục rỗng sau khi move) và `Baby2/assets/baby2` (chuỗi thư mục rỗng sau khi chuyển 24 ảnh legacy). Script import có guard `folder.exists()` nên không ảnh hưởng pipeline; ảnh legacy 24 file vẫn nằm trong `originals/images/legacy-baby1/`.
- **Gate xanh đồng bộ (phản hồi "login chưa đổi màu"):** màn gate chỉ tải `access-gate.css` + `access-gate-brand.css` (không qua hero-refresh) nên vẫn hồng/xanh Baby1. Đã đổi toàn bộ: biến `--gate-accent/--gate-warm/--gate-bg/--gate-bg-soft` về tông xanh đậm, badge YK + nút Open gradient `#8FC7AE→#6FA986→#4F9271`, viền/focus input mật khẩu xanh, các radial glow hồng/xanh dương → xanh lá. Screenshot `review/green-gate-1440.png`. Grep xác nhận không còn màu hồng/xanh dương cũ trong 2 file gate CSS.
- **Smoke test lại sau sửa: PASS cả 1440×900 và 390×844** — preview ảnh hiện trên card (40/31 thumbnail load), video phát sau click, 0 JS error, 0 404, 0 MP4 tải sớm. Screenshot: `review/green-hero-1440.png`, `review/green-diary-1440.png`.
- **Cần hỏi người dùng (chưa chốt):** 356 stem ảnh (714 file gốc, giai đoạn 2022-12 → 2023-03, phần lớn là giai đoạn sơ sinh/bệnh viện) chưa có trong IMG_checked của người dùng. Hiện đang lấp bằng WebP generate từ originals để không mất content. Nếu người dùng chủ ý loại những ảnh này (ảnh xấu/trùng), có thể bỏ phần lấp để display chỉ còn đúng bộ checked (nhẹ hơn ~77 MB).
- Đã phát hiện và **sửa bug priority** trong `import-y-khue-media.py` build_images: trước đây so sánh `sourceName` sai nên bản IMG_checked gần như không được chọn (16/1.513); đã sửa thành `{"IMG_checked": 0, "legacy-baby1": 1, "IMG": 2}`.
- Toàn bộ display cũ (images/videos build từ originals + 90 variant `-altN` cũ) đã bị xóa và build lại theo checked-first; kết quả cuối ghi ở dòng cập nhật dưới.
- Bản gốc 2.609 file vẫn nằm nguyên trong `assets/y-khue/originals/` (đã move hash-verified từ `Cá` ở phiên trước; `Cá` giờ rỗng, chỉ còn Thumbs.db). Không xóa originals.

### Diễn biến phiên
- Đọc cả 3 handoff và tiếp quản: `build-images` dở dang (1.188 file + 4 `.tmp`) đã chạy lại xong theo pipeline cũ: 1.428 display + 85 pending-collision.
- Review 85 collision bằng mắt qua 17 sheet do `Baby2/scripts/build-collision-sheets.py` render tại `Baby2/review/collision-sheets/`: 82 nhóm là ảnh khác thật sự trùng tên, 3 nhóm screenshot/crop của ảnh đã chọn (`2022-12-09`, `2023-03-17`, `2023-03-17_1`). Quyết định lưu `Baby2/data/collision-decisions.json`: mọi mismatched được render thành display riêng `-alt2`/`-alt3`…, không gộp, không mất nội dung. (Lưu ý: phân tích này dựa trên selected sai do bug priority; sau khi sửa bug + chuyển checked-first, flow chỉ còn áp dụng cho 356 stem thiếu checked.)
- Thêm action `make-collision-decisions` + `resolve-collisions` vào `import-y-khue-media.py` (render idempotent, decode-check, status `resolved` + `variants` trong audit). Lượt đầu thiếu 85 ảnh chính vì build_images bỏ qua nhóm pending — đã sửa resolve render luôn ảnh chính.
- Người dùng chỉ ra nhầm lẫn pipeline (bộ xử lý nằm ở G:, không phải Cá; 30 GB không deploy được) → chuyển checked-first như trên. Batch transcode video từ originals đã dừng và không cần nữa.

### Auto-sync media (watcher) — yêu cầu "copy/xóa ảnh tự hiển thị"
- Trước đây KHÔNG tự: trang đọc `data/media-manifest.js` tĩnh, copy/xóa file phải chạy lại script build manifest.
- **Đã làm auto:** `Baby2/scripts/watch-media.py` + `Baby1/scripts/watch-media.py` — poll 4 giây, khi thấy copy/thêm/sửa/xóa trong thư mục display sẽ tự tạo poster cho video mới rồi tự rebuild manifest. Người dùng chỉ cần **refresh trình duyệt** để thấy.
- Khởi động cả 2 watcher bằng 1 cú double-click: `start-media-watch.bat` ở gốc repo (mở 2 cửa sổ cmd thu nhỏ).
- Quy tắc bắt buộc cho người dùng: **tên file phải bắt đầu bằng ngày `YYYY-MM-DD...`**; file sai tên bị bỏ qua (builder + watcher đều báo, không crash — đã vá cả 2 builder từ `fromisoformat` crash thành skip + cảnh báo).
- Xóa file an toàn: `story-enrichment-v2.js` của cả Baby1 và Baby2 đã được vá bỏ `throw` khi media đã review bị xóa (chuyển thành `console.warn` + `.filter(Boolean)`), trang không còn trắng nếu file bị xóa nhầm.
- Đã kiểm thử end-to-end: copy ảnh thử vào Baby2 → manifest 1603→1604 tự động; xóa → về 1603 tự động. Watcher cần đang chạy mới auto; tắt máy/đóng cửa sổ watcher thì phải chạy lại .bat.
- Lưu ý Baby1: file bị xóa mà nằm trong story evidence (đã review) sẽ bị bỏ qua có cảnh báo, nhưng `validate-baby-static.js` sẽ báo thiếu evidence — nên tránh xóa file đã nối chuyện; thêm ảnh mới thì tự vào nhật ký tháng tương ứng ngày.
- Deploy lên GitHub vẫn phải commit/push như cũ; watcher chỉ auto ở bản local.

### Hiển thị tên file khi mở media (cả Baby1 + Baby2)
- Mở ảnh/video trong viewer giờ có pill đáy-trái panel: **tên file gốc · dd/mm/yyyy · Ảnh/Video** (VD `2022-08-25_1_sieuam.mp4 · 25/08/2022 · Video`).
- File mới `js/media-filename.js` (giống nhau ở cả 2 bé), nạp cuối chuỗi load trong `js/access-gate.js`; MutationObserver trên `#mediaViewerContent` nên bắt được mọi đường mở (album, card, prev/next).
- Tên lấy trực tiếp từ file đang hiển thị → **tự đồng bộ khi thêm/xóa qua watcher**, không cần làm gì thêm.
- Đã test Playwright cả 2 bé: caption đúng cho ảnh và video, 0 JS error. Screenshot `review/filename-tag2.png`, `review/filename-tag-video.png`.

- Sửa lặp thời gian (phản hồi người dùng): tên file đã chứa ngày nên pill không còn thêm `dd/mm/yyyy`; ngày riêng chỉ hiện khi tên file KHÔNG bắt đầu bằng `YYYY-MM-DD`. Caption chuẩn: `2022-08-15_1.webp · Ảnh`. Đã test lại cả 2 bé.

- Click-to-copy (phản hồi người dùng): bấm vào pill tên file → copy tên file gốc vào clipboard, pill đổi nền xanh + hiện "Đã copy: <tên> ✓" 1,2 giây rồi trả về như cũ. Dùng `navigator.clipboard` có fallback `execCommand` cho môi trường file://. Đã test clipboard thật trên Chromium: clipboard nhận đúng `2022-08-15_1.webp`.

### Đã xóa originals (phản hồi "copy nhầm" — xác minh rồi xóa)
- `Baby2/assets/y-khue/originals/` (2.609 file, 33,4 GB) **đã xóa ngày 06/09/2026** sau khi đối chiếu SHA-256 TOÀN BỘ (không phải mẫu): 2.585/2.585 file nguồn Cá trùng từng byte tại `G:/Uncheck/img/FullData/IMG_Lọc/Cá` và 24/24 legacy trùng tại `G:/Uncheck/img/WEBP/Yên`. Bản gốc duy nhất còn lại do người dùng quản lý trên G:.
- Audit `Baby2/data/media-import-audit.json` vẫn giữ đủ SHA-256 từng file + ghi chú `originalsBackup` trỏ sang G: — provenance không mất.
- Hệ quả: `build-display-checked.py` bước "lấp stem thiếu" không còn chạy được trực tiếp (nguồn originals đã xóa). Nếu sau này cần rebuild phần đó, trỏ script sang `G:/Uncheck/img/FullData/IMG_Lọc/Cá` (đã ghi trong audit). Display hiện tại (1.603 ảnh + 671 video + poster) không phụ thuộc originals.

### Tinh chỉnh màu theo đánh giá (đã commit checkpoint 11216ba trước khi sửa)
1. Nền gate tươi hơn: giảm lớp phủ tối (rgba(5,9,17,.34-.62) → rgba(10,26,19,.18-.40)), saturate backdrop .92 → 1.12, 3 radial glow tăng alpha ~2x → hết cảnh "xám mù sương".
2. Ô nhập mật khẩu: nền đổi sang xanh đậm ấm rgba(12,24,18,.82), caret xanh nhạt — không còn "hố" đen lạnh.
3. Journey: 3 radial glow nền tăng alpha (.50/.34/.32 → .66/.48/.46) — nền có presence xanh rõ hơn mà vẫn thoáng.
4. Nút × đóng chủ đề launcher (style.css): navy đen → xanh rêu trung tính rgba(18,32,26,.88) — hợp mọi chủ đề, hết lệch tông với Baby2.
- Smoke test PASS 1440/390: 0 JS error, 0 request lỗi. Screenshot: review/refined-gate.png, refined-hero.png, refined-diary.png.

### Gate Baby2 có background ảnh như Baby1
- Tạo `Baby2/assets/y-khue/ui/journey-background.webp` (20 KB) từ ảnh `2022-12-12.webp` (ảnh bé được chọn làm avatar): resize 1600px + GaussianBlur 26 + giảm sáng nhẹ 0.92 — làm mờ sẵn để chữ gate đọc rõ.
- `css/access-gate.css` đổi URL nền từ SVG trơn sang webp này. Muốn đổi ảnh nền khác: thay file webp hoặc chạy lại đoạn generate với ảnh nguồn khác.
- Screenshot: review/photo-gate.png.

### Sự kiện đầu tiên Baby2 — Tai nạn Vũng Tàu 28/06/2024 (mapping theo yêu cầu)
- Người dùng xác nhận: 28/06/2024 Cá bị té đập vào bàn, chảy máu và sưng vùng mặt khi chơi ở Vũng Tàu.
- Media cùng ngày: 12 ảnh (`2024-06-28_2.._13`) + 1 video (`2024-06-28.mp4`, cảnh đi chơi trước lúc té) — đã review bằng contact sheet `review/event-2024-06-28.jpg`: 11 ảnh chụp vết sưng bầm trán + vết đứt chân mày trái, được bố bế/nằm nghỉ; khớp lời kể.
- Ghi `data/story-observations.js` (version 2, events[0]): scene `ca-accident-vungtau-2024-06-28`, importance 5, sensitive TRUE, tháng 18 (1 tuổi 6 tháng), toàn bộ 13 media vào `excludePreview` + `attach()` cho sensitive → **0 preview vết thương trên card**, chỉ có nút "Mở album riêng · 12 ảnh · 1 video".
- Sửa `story-enrichment-v2.js`: nhãn scene sensitive đổi từ "Mở nhật ký theo dõi riêng" → "Mở album riêng" (chữ cũ chỉ đúng cho nhóm tiêu hóa).
- Đã kiểm thử trình duyệt: card render đúng vị trí 18m trên timeline, galleryMedia 13, media preview 0, media 28/06 được tách khỏi nhật ký tháng (diary còn 25 ảnh/11 video). Screenshot `review/event-scene-card2.png`.
- Quy trình thêm sự kiện mới sau này: sửa `events` trong `data/story-observations.js` (đúng cấu trúc trên), media src phải tồn tại trong manifest, sensitive=true nếu có vết thương.

### Đổi ảnh đại diện Baby2 (yêu cầu)
- Card launcher baby2 (`app.js` root): `2022-12-12.webp` → **`2025/12/2025-12-13_1.webp`** (bé cười đội mũ xanh, 3 tuổi).
- Nền gate `ui/journey-background.webp` được regenerate lại từ chính ảnh mới này (blur 26, giảm sáng 0.92) cho đồng bộ.
- Xác minh: card load naturalWidth>0, screenshot `review/launcher-page2.png` + `review/gate-new-bg.png`.

## Viết chuyện cho Baby2 (DONE 06/09/2026)
- Review toàn bộ 64 contact sheets (45 ảnh + 19 poster) qua **3 agent song song**, báo cáo chi tiết từng cụm khoảnh khắc.
- `scripts/build-story-observations.py` (mới) sinh `data/story-observations.js` **version 3 với 20 chương chuyện, 106 media** — mọi đường dẫn verify trên disk trước khi ghi:
  prenatal (que thử + siêu âm 4D) → ngày chào đời → tuần đầu ở nhà → tập lấy mặt khỏi sàn → tiệc bánh trái tim + CCCD quét mặt → ông và cháu (17/04/2023) → đi chợ đầu tiên → TTTM xe tập đi → ba thế hệ (24/07/2023) → đêm đầu đi xe máy cùng ba → thìa cháo đầu tiên → chị Yên hôn em → Cá tròn một tuổi → dã ngoại công viên → xe đạp hồng → **tai nạn Vũng Tàu (giữ nguyên, sensitive)** → bộ đồ đỏ chào năm mới → mũ thùng xốp → đêm hội xuống phố → Cá tròn ba tuổi.
- Mỗi chương: importance 3-5, `narrativeSource=visual-evidence`, media tách khỏi nhật ký tháng, preview tối đa 4; Vũng Tàu giữ sensitive (0 preview vết thương).
- Smoke 1440: **171 scene**, cả 20 chương render đủ preview + album, 0 JS error/404. Screenshot `review/chapter-ong-va-chau.png`.
- Thêm chương mới sau: sửa `EVENTS` trong `scripts/build-story-observations.py` rồi chạy lại (script tự verify đường dẫn).

### Hoàn tất lấp 356 nhóm thiếu bằng thông số tool người dùng (06/09/2026)
- Người dùng xác nhận 356 nhóm sơ sinh thiếu là do **chưa xử lý**, yêu cầu: chuyển WebP theo thông số mặc định tool (quality 80, cạnh dài nhất 1600px, giữ tên), đồng bộ chuyện/web, làm nhẹ để lên GitHub, rồi xử lý ảnh gốc (có WebP rồi thì xóa, chưa có thì giữ).
- `scripts/reconvert-missing-originals.py` (mới): lấy bản gốc đã backup trên `G:/Uncheck/img/FullData/IMG_Lọc/Cá` (verify SHA-256 với audit trước khi dùng), chuyển q80/1600px, ghi **cả hai nơi**: `G:/Uncheck/img/WEBP/Cá/IMG_checked/YYYY/MM/` (bổ sung checked set của người dùng) + thay display Baby2 (giữ nguyên tên → 20 chương chuyện + manifest tự đồng bộ, không cần sửa gì).
- **Kết quả: 401 file chuyển thành công (338 camera + 24 legacy từ WEBP/Yên + 39 nhóm pending-collision qua collision-decisions), 401 bản gốc đã xóa trên G:, 0 thất bại.** Log chi tiết: `Baby2/data/reconvert-missing-audit.json`.
- Bug đã sửa trong script: filter status thiếu `rendered`/`pending-collision`, thiếu mkdir checked parent, HEIC cần pillow_heif, webp passthrough không re-encode, skip theo job thay vì theo stem.
- **Độ phủ cuối: display Baby2 1.603 ảnh ≡ G: IMG_checked 1.603 ảnh, 0 thiếu.** Kích thước images giảm 264 → **237 MB** (q80/1600 nhẹ hơn q84 full-res cũ).
- **GitHub:** images 237 MB + posters 6 MB + code — đủ điều kiện push (file lớn nhất < 100 MB). **Videos 5 GB vẫn vượt giới hạn GitHub** — nếu muốn đưa video lên cần tách repo/LFS/cloud riêng.
- WEBP/Yên đã bỏ 24 file legacy (chúng thuộc quyền Cá, giờ nằm trong IMG_checked của Cá) — đã ghi log trong reconvert-missing-audit.json.

## TÁCH REPO RIÊNG & PUSH GITHUB (06/09/2026)
- Site đã tách khỏi Discovery, repo riêng: **https://github.com/maxskill115/Baby2** — local: `F:/0.Tools/fingermath/Baby2`.
- Push đầy đủ media + video theo đợt ≤350MB bằng `F:/0.Tools/fingermath/push-batched.py` (script dùng chung, idempotent, tự retry/rebase).
- **4 file video >100MB bị GitHub chặn cứng, KHÔNG lên được, giữ local** (xem `.gitignore`): `assets/y-khue/videos/2022/08/2022-08-25_1_sieuam.mp4` (167MB)
- Cấu trúc giữ nguyên (assets/css/js/data/scripts); `.gitignore` repo: contact-sheets + chỉ video của assets/y-khue/videos.
- Sau này đổi tên project/domain trên Vercel thì nhớ cập nhật link card trong repo Discovery (`app.js`).

## Video hover/chạm-giữ preview kiểu YouTube (06/09/2026)
- `js/video-hover-preview.js` (dùng chung 3 site, nạp cuối chuỗi access-gate sau media-filename): desktop rê chuột ~0.4s → thumbnail tự phát video muted từ đầu, tối đa 6s rồi loop; rời chuột → dừng + gỡ src. Mobile: chạm giữ ~0.4s → preview, thả tay → dừng và CHẶN click mở viewer (gõ nhanh <0.4s vẫn mở viewer bình thường).
- Performance chuẩn YouTube (đã test Playwright): cuộn full hành trình **0 MP4 nào được tải** (chỉ poster lazy); hover vào thumbnail nào chỉ tải đúng video đó.
- Video hiển thị đè poster qua class `.is-previewing` (opacity poster → 0, video object-fit cover).
- Lưu ý test bằng Playwright synthetic touch: phải dispatch TouchEvent có `touches` thật; `dispatch_event("touchstart")` không kèm touch list sẽ bị bỏ qua (đã nới điều kiện để hoạt động cả khi length != 1).

### Fix hover-preview trên PC (06/09/2026, sau phản hồi người dùng)
- Triệu chứng: mobile chạm giữ phát OK nhưng PC rê chuột không phát.
- Nguyên nhân: khi `<video>` preview được chèn vào thumbnail, chuột "nhảy" từ poster sang video mới → trình duyệt sinh `pointerout` (relatedTarget = video preview) → handler cũ hiểu là rời thumbnail → tắt preview ngay (pointerout cascade).
- Fix: trong `pointerout`, bỏ qua khi `relatedTarget` vẫn nằm trong thumb (`thumb.contains(relatedTarget)`); chỉ dừng preview khi con trỏ rời khỏi thumb thật sự. Desktop click vào thumb đang preview: stop preview rồi vẫn mở viewer bình thường.
- Test chuột THẬT (Playwright mouse.move sinh đủ pointer events + cascade): hover 1.2s → playing; di chuyển vòng trong thumb (qua video mới chèn) → vẫn phát; rời hẳn → dừng. Commit `0fca035` (Baby1), đồng bộ 3 site.

### Fix 2 bug album (06/09/2026, phản hồi người dùng)
- **Bug "đóng media thoát hẳn ra ngoài"**: bấm × (hoặc Escape) khi đang xem 1 ảnh/video trong album giờ quay về **SẢNH ALBUM** thay vì đóng viewer; bấm × / Escape lần 2 từ sảnh mới thoát hẳn. Cơ chế: media-ux bắt `[data-close-viewer]` khi có `.b3-viewer` + galleryContext → gọi `window.__reopenGallery(sceneId)` (bridge trong gallery-enhancer render lại sảnh); main.js xử lý Escape tương tự qua `data-gallery-scene` mới gắn trên `.b3-viewer`.
- **Bug filter reset khi cuộn**: nguyên nhân `onViewerContentChanged` (MutationObserver của lazy-load) luôn gọi `applyFilter(view, "all")` mỗi khi DOM album đổi → mỗi lần cuộn xuống, ảnh lazy-load gắn src → filter rơi về "Tất cả". Fix: biến `currentGalleryFilter` ghi nhớ lựa chọn; observer áp filter hiện tại thay vì "all".
- Test Playwright full flow PASS: lọc Video → cuộn dài 2 lần → vẫn "video" (57 video, 0 ảnh lọt); mở 1 video → Escape → "SẢNH ALBUM" → Escape → đóng hẳn; nút × 2 tầng tương tự; 0 JS error.
- Lưu ý: album không có nút lọc khi scene chỉ chứa 1 loại media (renderFilters trả rỗng) — filter check phải test ở album đủ cả ảnh + video.
