/*
 * 課程登記表 —— 全站唯一的課程清單來源。
 * 新增課程：在陣列「末端」加一筆，欄位格式請見 AGENTS.md 第 3 節。
 * 首頁卡片、上一課/下一課按鈕都由這裡自動產生。
 */
window.LESSONS = [
  {
    id: "L01",
    file: "lessons/L01-greetings.html",
    vi: "Chào hỏi",
    zh: "打招呼",
    level: "入門",
    summary: "用正確的稱謂打招呼、自我介紹、道謝與道別。"
  },
  {
    id: "L02",
    file: "lessons/L02-numbers.html",
    vi: "Số đếm",
    zh: "數字與殺價",
    level: "入門",
    summary: "數字 1–1000 的說法與變音規則，到市場問價錢。"
  },
  {
    id: "L03",
    file: "lessons/L03-food.html",
    vi: "Ăn uống",
    zh: "點餐",
    level: "入門",
    summary: "在河粉店點餐、說「好吃」、請服務生結帳。"
  }
];
