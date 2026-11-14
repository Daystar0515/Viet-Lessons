# AGENTS.md — 越來越好：越南語入門講義

> 這份文件是寫給 AI（Claude、Codex、Copilot 等）與協作者看的「專案說明書」。
> 在新增或修改任何內容之前，**請先完整讀完本文件**，並嚴格依照規則執行。

---

## 1. 專案目的

- 這是一個給**台灣華語使用者**的越南語入門講義網站，部署在 GitHub Pages。
- 每一課是一個獨立的 HTML 頁面，**所有課程使用完全相同的版面與區塊順序**，讓學習者每課都知道該往哪裡看。
- 目標：之後只要對 AI 說「依照 AGENTS.md 新增第 N 課，主題是 ○○」，就能產出一頁風格一致、可直接上線的講義。

### 語言標準
- 越南語以**北部（河內）音與用詞**為標準。
- 若南部說法不同，放在單字表「備註」欄，格式：`南部：ly`。
- 中文一律使用**台灣繁體中文**與台灣慣用詞（例：「影片」不是「視頻」、「計程車」不是「出租車」）。
- **不使用羅馬拼音或注音標示越南語發音**，越南文本身就是拉丁字母；發音靠聲調標籤與朗讀按鈕輔助。

---

## 2. 檔案結構

```
/
├── index.html                  首頁：網站介紹 + 課程卡片（由 lessons.js 自動產生）
├── tones.html                  聲調總表（全站共用參考頁）
├── lessons/
│   ├── L01-greetings.html      第 1 課
│   ├── L02-numbers.html        第 2 課
│   └── L03-food.html           第 3 課
├── templates/
│   └── lesson-template.html    ★ 新增課程時「複製這個檔案」開始
├── assets/
│   ├── css/style.css           全站唯一的樣式表
│   └── js/
│       ├── lessons.js          ★ 課程登記表（唯一的課程清單來源）
│       └── site.js             共用功能：頁首頁尾、課程卡片、上一課/下一課、測驗、朗讀
├── tools/
│   └── check_lessons.py        規則檢查腳本
├── AGENTS.md                   本文件
├── CLAUDE.md                   指向本文件
├── README.md                   給人類看的專案簡介
└── .nojekyll                   讓 GitHub Pages 不經 Jekyll 處理
```

### 命名規則
- 課程檔名：`lessons/L{兩位數編號}-{英文小寫主題}.html`
  - 例：`L04-transport.html`、`L12-shopping.html`
  - 主題只用小寫英文與連字號 `-`，不用空白、底線、中文。
- 課程 ID：`L01`、`L02`……與檔名開頭一致。
- 編號**連續、不跳號、不重複使用**。刪除課程時不要重排編號。

---

## 3. 新增一課的標準流程（必須全部完成）

1. **複製** `templates/lesson-template.html` → `lessons/L{NN}-{topic}.html`
2. 修改 `<body>` 的 `data-lesson="L{NN}"`（`data-root="../"` 保持不變）
3. 依第 4 節的規格填寫六個區塊，**不可增減或調換順序**
4. 在 `assets/js/lessons.js` 的 `window.LESSONS` 陣列**末端**新增一筆：
   ```js
   {
     id: "L04",
     file: "lessons/L04-transport.html",
     vi: "Đi lại",
     zh: "交通",
     level: "入門",
     summary: "一句話說明這課學什麼（25 字以內）"
   }
   ```
   首頁卡片、導覽列、上一課/下一課按鈕都會**自動更新**，不需要手動改 `index.html`。
5. 執行 `python3 tools/check_lessons.py`，必須顯示全部通過。

---

## 4. 課程頁面規格（每一課都一樣）

頁面 `<main>` 內依序包含以下區塊，`id` 必須完全相同：

| 順序 | 區塊 id | 標題 | 內容規定 |
|---|---|---|---|
| 0 | （`.lesson-hero`） | 課名 | `L{NN}`、越南文課名、中文課名、3 條「學習目標」 |
| 1 | `#dialogue` | 情境對話 | 4–8 句，兩位角色交替；每句都有越南文 + 中文 |
| 2 | `#vocab` | 單字表 | 8–14 個單字或片語，四欄：越南文／聲調／中文／備註 |
| 3 | `#grammar` | 文法重點 | 2–3 個重點，每個都有「句型框」與 2 個以上例句 |
| 4 | `#culture` | 文化小知識 | 1 則，80–150 字，和本課主題相關 |
| 5 | `#quiz` | 小測驗 | 剛好 5 題選擇題，每題 3–4 個選項，附解析 |

### 4.1 情境對話
```html
<div class="line">
  <span class="speaker">A</span>
  <div>
    <p class="vi" data-say>Chào chị!</p>
    <p class="zh">姐姐好！</p>
  </div>
</div>
```
- 角色用 `A`、`B`，或用越南文身分（如 `Khách` 客人、`Phục vụ` 服務生）。
- 對話中出現的關鍵字，**必須**出現在單字表中。

### 4.2 單字表
```html
<tr>
  <td class="vi" data-say>cảm ơn</td>
  <td><span class="tone t-hoi">hỏi</span><span class="tone t-ngang">ngang</span></td>
  <td>謝謝</td>
  <td>最常用的道謝</td>
</tr>
```
- **聲調欄**：依音節順序，每個音節一個標籤，標籤數量 = 音節數量。
- 聲調只能使用以下六個 class（和 `tones.html` 一致）：

| class | 聲調名 | 符號 | 例 |
|---|---|---|---|
| `t-ngang` | ngang 平聲 | （無） | ma |
| `t-huyen` | huyền 玄聲 | ` | mà |
| `t-sac` | sắc 銳聲 | ´ | má |
| `t-hoi` | hỏi 問聲 | ̉ | mả |
| `t-nga` | ngã 跌聲 | ~ | mã |
| `t-nang` | nặng 重聲 | ̣ | mạ |

- 備註欄沒有內容時填 `—`，不可留空。

### 4.3 文法重點
```html
<div class="grammar-point">
  <h3>1. 標題</h3>
  <p>一到三句中文說明。</p>
  <div class="pattern">主詞 + là + 名詞</div>
  <ul class="examples">
    <li><span class="vi" data-say>Tôi là sinh viên.</span><span class="zh">我是學生。</span></li>
  </ul>
</div>
```

### 4.4 文化小知識
```html
<aside class="culture-box">
  <h3>標題</h3>
  <p>內文……</p>
</aside>
```

### 4.5 小測驗
```html
<div class="quiz-item" data-answer="b">
  <p class="q">1. 題目？</p>
  <div class="choices">
    <button data-choice="a">選項</button>
    <button data-choice="b">選項</button>
    <button data-choice="c">選項</button>
  </div>
  <p class="explain">解析：為什麼答案是 b。</p>
</div>
```
- 5 題中**至少 1 題考聲調、至少 1 題考文法**，其餘考單字或對話理解。
- 正解不要永遠放同一個位置。
- 互動行為由 `site.js` 自動處理，**不要在課程頁寫任何 `<script>` 內容**（只保留範本中引入的兩支 JS）。

---

## 5. 視覺風格

- 設計關鍵字：**溫暖、紙質感、像一本整齊的講義**。
- 配色（已定義在 `style.css` 的 CSS 變數中，**不要另外寫死顏色**）：
  - `--paper` 米白底 `#faf6ee`
  - `--ink` 深墨色文字 `#2b2a26`
  - `--bamboo` 竹綠主色 `#2f6b4f`
  - `--lacquer` 漆紅強調色 `#b23a2e`
  - `--lotus` 蓮粉輔色 `#f3d9d2`
- 字型：越南文用 `Be Vietnam Pro`（完整支援越南文聲調符號），中文用 `Noto Sans TC`。
- 越南文一律套用 `.vi` class（會使用越南文字型並加粗）；中文翻譯套用 `.zh`。
- 手機優先：所有頁面在 375px 寬度下都必須能正常閱讀，表格可以橫向捲動。

---

## 6. AI 修改內容時必須遵守的規則

1. **不要改動共用檔案的結構**（`style.css`、`site.js`），除非使用者明確要求「改全站樣式／功能」。只是新增課程時，只需動到 `lessons/` 新檔案與 `lessons.js`。
2. **不要在個別頁面寫 inline style 或 `<style>`**。需要新樣式時，加進 `style.css` 並在本文件第 5 節補充說明。
3. **不引入任何外部 JS 框架或建置工具**（React、Vue、npm build……）。本站是純 HTML/CSS/JS，必須能直接被 GitHub Pages 讀取。
4. **越南文正確性優先**：每個聲調符號都要正確；不確定的用法寧可不寫，也不要編造。
5. 所有路徑都使用**相對路徑**（課程頁用 `../assets/...`），確保部署在 `https://帳號.github.io/repo名稱/` 子路徑下也能運作。
6. 每次新增或修改課程後，執行 `python3 tools/check_lessons.py`。
7. 如果修改了規則本身（例如新增一種區塊），**必須同步更新 AGENTS.md、範本、檢查腳本三處**，保持一致。

---

## 7. 已規劃的課程路線（可依序新增）

| ID | 主題 | 越南文 | 狀態 |
|---|---|---|---|
| L01 | 打招呼 | Chào hỏi | ✅ 已完成 |
| L02 | 數字與殺價 | Số đếm | ✅ 已完成 |
| L03 | 點餐 | Ăn uống | ✅ 已完成 |
| L04 | 交通 | Đi lại | 待新增 |
| L05 | 時間與日期 | Thời gian | 待新增 |
| L06 | 家庭 | Gia đình | 待新增 |
| L07 | 購物 | Mua sắm | 待新增 |
| L08 | 天氣 | Thời tiết | 待新增 |

新增課程後，請把該列狀態改成 `✅ 已完成`。
