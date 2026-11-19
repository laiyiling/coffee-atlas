from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

class RefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value and not value.startswith(("http:", "https:", "mailto:", "#", "data:", "javascript:")):
                self.refs.append(value)

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def load(rel):
    return json.loads(read(rel))

def extract_array(source, variable):
    marker = variable + "="
    pos = source.find(marker)
    if pos < 0:
        marker = variable + " ="
        pos = source.find(marker)
    assert pos >= 0, f"HTML 內找不到資料陣列：{variable}"
    start = source.find("[", pos + len(marker))
    assert start >= 0, f"資料陣列缺少左括號：{variable}"
    data, _ = json.JSONDecoder().raw_decode(source[start:])
    return data

wiki = read("01_Wiki/index.html")
mag = read("02_HTML_Magazine/index.html")
hero = wiki.split('<section class="hero">', 1)[1].split("</section>", 1)[0]
assert '{"id"' not in hero and '"summary":' not in hero and '"body":' not in hero, "首頁 Hero 區塊不應顯示原始 JSON"
for badge in ('5 VOL.', '11 CHAPTERS', '15 SOURCES', 'APA 7TH'):
    assert badge in hero, f"首頁缺少統計標籤：{badge}"
books = load("01_Wiki/books.json")
chapters = extract_array(wiki, "chapters")
html_books = extract_array(wiki, "books")
html_sources = extract_array(wiki, "sources")
slides = extract_array(mag, "slides")
source_register = load("03_Sources/source_register.json")

assert (len(books), len(html_books), len(chapters), len(slides), len(source_register)) == (5, 5, 11, 32, 15), "冊數／章節／頁數／來源數量不符合規格"
assert books == html_books, "books.json 與 Wiki 內嵌資料不一致"
assert {x["id"] for x in html_sources} == {x["id"] for x in source_register}, "Wiki 來源與來源登錄 ID 不一致"
assert sum(x["type"] == "學術研究" for x in source_register) == 8
assert sum(x["type"].startswith("官方") for x in source_register) == 5
assert sum(x["type"] == "專業產業資料" for x in source_register) == 2
source_ids = {x["id"] for x in source_register}
markdown_files = list((ROOT / "01_Wiki/books").glob("VOL_*.md"))
assert len(markdown_files) == 5, "Markdown 分冊數量不是五冊"

for chapter in chapters:
    assert chapter["sources"] and set(chapter["sources"]).issubset(source_ids), f"章節 {chapter['id']} 來源 ID 不存在"
    assert chapter["body"].strip(), f"章節 {chapter['id']} 缺少正文"
    matches = [p.read_text(encoding="utf-8") for p in markdown_files if chapter["body"].strip() in p.read_text(encoding="utf-8")]
    assert len(matches) == 1, f"章節 {chapter['id']} Markdown 正文不存在或重複"

refs = read("03_Sources/references_APA7.md")
a4 = "Cordoba Castro, N. M., Ruiz Pardo, R. Y., Moreno Moreno, F. L., & Fernandez Alduenda, M. R."
assert a4 in refs, "A4 APA 作者順序不正確"

for rel in ("01_Wiki/index.html", "02_HTML_Magazine/index.html"):
    page = ROOT / rel
    text = page.read_text(encoding="utf-8")
    parser = RefParser()
    parser.feed(text)
    assert len(parser.ids) == len(set(parser.ids)), f"{rel} 有重複 id"
    for ref in parser.refs:
        target = (page.parent / ref.split("#")[0].split("?")[0]).resolve()
        assert target.exists(), f"{rel} 找不到 HTML 資源：{ref}"
    for part in text.split("url(")[1:]:
        ref = part.split(")", 1)[0].strip().strip("'").strip('"')
        if ref and not ref.startswith(("http:", "https:", "data:")):
            assert (page.parent / ref).resolve().exists(), f"{rel} 找不到 CSS 資源：{ref}"
    assert text.count("<script>") == 1 and text.count("</script>") == 1, f"{rel} script 標籤數量異常"
    script = text.split("<script>", 1)[1].split("</script>", 1)[0]
    node = subprocess.run(["node", "--check", "-"], input=script, text=True, capture_output=True)
    assert node.returncode == 0, f"{rel} JavaScript 語法錯誤：{node.stderr}"

for asset in ("coffee_atlas_hero.svg", "processing_methods.svg", "flavor_wheel.svg", "brewing_steps.svg"):
    assert (ROOT / "01_Wiki/assets" / asset).exists(), f"缺少 SVG 素材：{asset}"
assert "coffee_atlas_hero.png" not in mag, "雜誌仍引用不存在的舊 PNG"
assert "115213518" not in read("06_Project_Source/project_spec.md"), "公開規格不應包含學號"

print("PASS：五冊、11 章、32 頁（封面＋目錄＋30 頁教學）、15 筆來源（8＋5＋2）。")
print("PASS：Wiki 內嵌資料、books.json、五冊 Markdown 與來源 ID 對應。")
print("PASS：APA 7 A4 作者排序、四個 SVG、HTML／CSS 本地資源路徑。")
print("PASS：HTML ID、script 標籤與 Node.js JavaScript 語法檢查。")
print("NOTE：此為靜態檢查；搜尋、收藏、滾輪、側欄、圖片放大與全螢幕仍需真實瀏覽器人工測試。")
