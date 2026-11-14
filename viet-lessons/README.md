# 越來越好：越南語入門講義

給台灣華語使用者的越南語入門講義網站，以北部（河內）音為標準。
純 HTML / CSS / JavaScript，部署在 GitHub Pages。

## 特色

- **每一課的版面完全相同**：課程頁首 → 情境對話 → 單字表 → 文法重點 → 文化小知識 → 小測驗
- **聲調彩色標籤**：每個音節都標出六個聲調之一，顏色和〈聲調表〉頁一致
- **朗讀按鈕**：使用瀏覽器內建的越南語語音（Web Speech API）
- **互動小測驗**：點選答案就會顯示解析與分數
- **規則檢查腳本**：`tools/check_lessons.py` 會自動檢查格式、題數，甚至會比對聲調標籤和越南文的聲調符號是否一致

## 專案結構

```
index.html              首頁（課程卡片由 lessons.js 自動產生）
tones.html              聲調總表
lessons/                每一課一個 HTML
templates/              新增課程用的範本
assets/css/style.css    全站樣式
assets/js/lessons.js    課程登記表
assets/js/site.js       共用功能
tools/check_lessons.py  規則檢查
AGENTS.md               給 AI 的專案規則（CLAUDE.md 指向它）
```

## 如何新增一課

完整規則請見 [AGENTS.md](AGENTS.md)。簡單來說，只要對 AI 說：

> 請依照 AGENTS.md，新增第 4 課，主題是「交通 Đi lại」。

AI 就會：

1. 複製 `templates/lesson-template.html` 成 `lessons/L04-transport.html`
2. 依規格填入對話、單字（含聲調標籤）、文法、文化、5 題測驗
3. 在 `assets/js/lessons.js` 新增一筆 → 首頁卡片和上一課／下一課按鈕自動更新
4. 執行 `python3 tools/check_lessons.py` 確認全部符合規則

## 這套規則如何幫助 AI 持續擴充

- **有範本可以複製**：AI 不需要重新設計版面，只要填內容，所以每課風格都一致。
- **只需要改兩個地方**：新課程檔案和 `lessons.js`。導覽、首頁、上一課／下一課都會自動更新，不會漏改。
- **內容規格寫成具體數字**：對話 4–8 句、單字 8–14 個、測驗剛好 5 題、聲調標籤數＝音節數，AI 有明確的標準可以遵守。
- **有語言標準**：北部音、台灣繁體中文、南部說法寫在備註，避免 AI 混用。
- **有自動檢查**：AI 做完可以自己跑檢查腳本，標錯聲調、少題目、忘記登記都會被抓出來。
- **有課程路線圖**：AGENTS.md 第 7 節列出接下來要做的主題，AI 知道下一課該做什麼。
