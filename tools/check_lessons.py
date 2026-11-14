#!/usr/bin/env python3
"""
規則檢查腳本：確認每一課都符合 AGENTS.md 第 2–4 節的規格。
用法：在專案根目錄執行  python3 tools/check_lessons.py
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSON_DIR = ROOT / "lessons"
REGISTRY = ROOT / "assets" / "js" / "lessons.js"

SECTION_ORDER = ["dialogue", "vocab", "grammar", "culture", "quiz"]
TONE_CLASSES = {"t-ngang": "ngang", "t-huyen": "huyền", "t-sac": "sắc",
                "t-hoi": "hỏi", "t-nga": "ngã", "t-nang": "nặng"}
# 聲調符號（Unicode 組合字元）→ class
MARK_TO_CLASS = {"̀": "t-huyen", "́": "t-sac", "̉": "t-hoi",
                 "̃": "t-nga", "̣": "t-nang"}
FILENAME_RE = re.compile(r"^L(\d{2})-[a-z]+(-[a-z]+)*\.html$")

errors = []


def err(file, msg):
    errors.append(f"[{file}] {msg}")


def tone_of(syllable):
    """依照越南文音節上的聲調符號，判斷應該是哪個 class。"""
    for ch in unicodedata.normalize("NFD", syllable):
        if ch in MARK_TO_CLASS:
            return MARK_TO_CLASS[ch]
    return "t-ngang"


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


registry = REGISTRY.read_text(encoding="utf-8")
registered = re.findall(r'id:\s*"(L\d{2})"[\s\S]*?file:\s*"([^"]+)"', registry)
registered_ids = [i for i, _ in registered]

# 登記表本身
if registered_ids != sorted(registered_ids):
    err("lessons.js", "課程順序必須依編號排列")
expected = [f"L{n:02d}" for n in range(1, len(registered_ids) + 1)]
if registered_ids != expected:
    err("lessons.js", f"編號必須從 L01 連續不跳號，目前是 {registered_ids}")
for lid, f in registered:
    if not (ROOT / f).exists():
        err("lessons.js", f"{lid} 指向不存在的檔案 {f}")

files = sorted(LESSON_DIR.glob("*.html"))
for path in files:
    name = path.name
    html = path.read_text(encoding="utf-8")

    m = FILENAME_RE.match(name)
    if not m:
        err(name, "檔名不符合 L{NN}-{topic}.html 格式")
        continue
    lid = f"L{m.group(1)}"

    if lid not in registered_ids:
        err(name, f"{lid} 尚未登記在 assets/js/lessons.js")

    if f'data-lesson="{lid}"' not in html:
        err(name, f'<body> 必須有 data-lesson="{lid}"')
    if 'data-root="../"' not in html:
        err(name, '<body> 必須有 data-root="../"')

    # 區塊順序
    positions = [html.find(f'<section id="{s}"') for s in SECTION_ORDER]
    if -1 in positions:
        missing = [s for s, p in zip(SECTION_ORDER, positions) if p == -1]
        err(name, f"缺少區塊：{missing}")
    elif positions != sorted(positions):
        err(name, "區塊順序錯誤，必須是 dialogue → vocab → grammar → culture → quiz")

    if 'class="lesson-hero"' not in html:
        err(name, "缺少 .lesson-hero 課程頁首")
    goals = re.search(r'<ul class="goals">([\s\S]*?)</ul>', html)
    if not goals or goals.group(1).count("<li>") != 3:
        err(name, "學習目標必須剛好 3 條")

    # 禁止 inline style / script
    if "<style" in html or ' style="' in html:
        err(name, "不可使用 <style> 或 inline style")
    for sc in re.findall(r"<script([^>]*)>([\s\S]*?)</script>", html):
        if sc[1].strip():
            err(name, "課程頁不可寫 <script> 內容")

    # 對話
    lines = html.count('<div class="line">')
    if not 4 <= lines <= 8:
        err(name, f"對話必須 4–8 句，目前 {lines} 句")

    # 單字表
    vocab = re.search(r'<table class="vocab">([\s\S]*?)</table>', html)
    rows = re.findall(r"<tr>([\s\S]*?)</tr>", vocab.group(1)) if vocab else []
    rows = [r for r in rows if "<td" in r]
    if not 8 <= len(rows) <= 14:
        err(name, f"單字表必須 8–14 列，目前 {len(rows)} 列")
    for r in rows:
        cells = re.findall(r"<td[^>]*>([\s\S]*?)</td>", r)
        if len(cells) != 4:
            err(name, f"單字列必須剛好 4 欄：{strip_tags(r)[:30]}")
            continue
        word = strip_tags(cells[0])
        tones = re.findall(r'<span class="tone (t-[a-z]+)">([^<]+)</span>', cells[1])
        syllables = word.split()
        if len(tones) != len(syllables):
            err(name, f"「{word}」有 {len(syllables)} 個音節，但有 {len(tones)} 個聲調標籤")
            continue
        for syl, (cls, label) in zip(syllables, tones):
            if cls not in TONE_CLASSES:
                err(name, f"「{word}」使用了不存在的聲調 class {cls}")
            elif TONE_CLASSES[cls] != label:
                err(name, f"「{word}」的標籤文字 {label} 與 class {cls} 不一致")
            elif tone_of(syl) != cls:
                err(name, f"「{syl}」的聲調應該是 {TONE_CLASSES[tone_of(syl)]}，卻標成 {label}")
        if not strip_tags(cells[3]):
            err(name, f"「{word}」的備註欄不可留空（沒有內容請填 —）")

    # 文法
    gp = html.count('<div class="grammar-point">')
    if not 2 <= gp <= 3:
        err(name, f"文法重點必須 2–3 個，目前 {gp} 個")
    for block in re.findall(r'<div class="grammar-point">([\s\S]*?)</ul>', html):
        if 'class="pattern"' not in block:
            err(name, "每個文法重點都要有 .pattern 句型框")
        if block.count("<li>") < 2:
            err(name, "每個文法重點至少 2 個例句")

    # 文化
    culture = re.search(r'<aside class="culture-box">[\s\S]*?<p>([\s\S]*?)</p>', html)
    if not culture:
        err(name, "缺少文化小知識")
    else:
        n = len(strip_tags(culture.group(1)))
        if not 80 <= n <= 160:
            err(name, f"文化小知識建議 80–150 字，目前約 {n} 字")

    # 測驗
    items = re.findall(r'<div class="quiz-item" data-answer="([a-d])">([\s\S]*?)<p class="explain">', html)
    if len(items) != 5:
        err(name, f"小測驗必須剛好 5 題，目前 {len(items)} 題")
    answers = []
    for i, (ans, body) in enumerate(items, 1):
        choices = re.findall(r'data-choice="([a-d])"', body)
        answers.append(ans)
        if not 3 <= len(choices) <= 4:
            err(name, f"第 {i} 題必須有 3–4 個選項")
        if ans not in choices:
            err(name, f"第 {i} 題的答案 {ans} 不在選項中")
    if answers and len(set(answers)) == 1:
        err(name, "正解不可以全部放在同一個位置")
    if 'id="quiz-score"' not in html or 'id="lesson-nav"' not in html:
        err(name, "缺少 #quiz-score 或 #lesson-nav")

for lid, f in registered:
    if not (ROOT / f).name in [p.name for p in files]:
        err("lessons.js", f"{lid} 已登記，但 lessons/ 中找不到檔案")

print(f"檢查了 {len(files)} 課、登記表 {len(registered_ids)} 筆。")
if errors:
    print(f"\n❌ 發現 {len(errors)} 個問題：")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("✅ 全部符合 AGENTS.md 規則！")
