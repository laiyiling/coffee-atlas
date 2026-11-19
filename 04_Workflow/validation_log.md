# Coffee_Atlas｜GitHub 匯入與驗證紀錄

最後更新：2026-11-16

## 本次已確認的修正
1. Wiki 首頁曾將整份章節 JSON 誤放在 Hero 統計標籤內，造成首頁顯示大量原始 JSON；已移除錯誤內容，恢復「5 VOL.／11 CHAPTERS／15 SOURCES／APA 7TH」四個標籤。Wiki 主頁資料仍保留於 script 區塊，script 開閉標籤各一組。
2. Wiki 首頁 Hero 主視覺路徑與原始圖片副檔名不一致；已統一改用 Repository 內的 `01_Wiki/assets/coffee_atlas_hero.svg`。
3. HTML 雜誌封面 CSS 背景與內頁圖片曾引用不存在的 PNG／WebP；已改為 `../01_Wiki/assets/coffee_atlas_hero.svg`。
4. 補入並追蹤四個 SVG：coffee_atlas_hero、processing_methods、flavor_wheel、brewing_steps。
5. APA 7 參考文獻 A4 作者順序已修正。
6. 第 02、11 章的文內引用與章節來源 ID 曾不一致；已調整引用與來源 ID。
7. 已比對 11 個章節的 Wiki 正文與五冊 Markdown，現在每章正文都能在一冊 Markdown 中找到且僅找到一次。
8. 公開 Repository 的專案規格已移除學生姓名與學號。

## GitHub 遠端靜態檢查（2026-11-16）
- Wiki 與雜誌的 script 開啟／關閉標籤數量：均為 1／1。
- Wiki Hero 統計標籤不再包含原始 JSON，並新增自動回歸檢查。
- Wiki Hero SVG 路徑：存在。
- Wiki 三個章節圖像 SVG：存在。
- 雜誌封面 CSS 背景及內頁圖片路徑：均指向已追蹤 SVG。
- 雜誌舊的 coffee_atlas_hero.png 引用：未發現。
- Wiki 資料：5 冊、11 章、15 筆來源。
- 雜誌資料：32 頁（封面＋目錄＋30 頁教學內容）。
- 來源分布：8 篇學術研究、5 筆官方／機構資料、2 筆產業資料。
- 11 章正文與五冊 Markdown 對應：11／11 通過。
- 章節來源 ID：均能對應來源登錄。
- APA A4 作者順序：已修正。
- Graph＋Loop Mermaid、流程說明及驗證紀錄：存在。
- 公開規格未包含學生姓名或學號。

## 尚未完成／不可標示通過的項目
- 尚未在真實 Brave／Chrome／Edge 環境逐項操作搜尋、收藏、側邊抽屜、深淺色、字級調整、複製、列印、圖片放大、滑鼠滾輪、鍵盤切頁及全螢幕。
- 尚未對所有參考文獻逐筆完成出版社原頁、Crossref／DOI resolver 的完整交叉核驗。
- Word／PDF 報告與預覽 PNG 等二進位檔尚未匯入本 Repository；目前 GitHub 內容以網站程式、Markdown、JSON、SVG、參考資料及工作流程文件為主。

## 可重跑的靜態檢查
在專案根目錄執行：
```bash
python 06_Project_Source/validate_project.py
```
需安裝 Node.js，供 `node --check` 檢查內嵌 JavaScript。

靜態檢查不等於真實瀏覽器互動驗收。若有錯誤，應先記錄、修正，再重新執行檢查。