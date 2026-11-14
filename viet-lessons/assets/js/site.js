/*
 * 全站共用功能（課程頁不需要、也不應該自己寫 script）
 * 1. 頁首、頁尾
 * 2. 首頁課程卡片
 * 3. 課程頁的上一課 / 下一課
 * 4. 小測驗互動
 * 5. 越南文朗讀按鈕（[data-say]）
 */
(function () {
  const body = document.body;
  const root = body.dataset.root || "";
  const lessons = window.LESSONS || [];
  const page = body.dataset.page || "";

  /* ---------- 1. 頁首、頁尾 ---------- */
  const header = document.createElement("header");
  header.className = "site-header";
  header.innerHTML = `
    <div class="inner">
      <a class="brand" href="${root}index.html"><span class="mark">Việt</span> 越來越好</a>
      <nav class="site-nav">
        <a href="${root}index.html" class="${page === "home" ? "active" : ""}">課程</a>
        <a href="${root}tones.html" class="${page === "tones" ? "active" : ""}">聲調表</a>
      </nav>
    </div>`;
  body.prepend(header);

  const footer = document.createElement("footer");
  footer.className = "site-footer";
  footer.innerHTML = `越來越好：越南語入門講義 · 北部（河內）音為準 · 共 ${lessons.length} 課`;
  body.append(footer);

  /* ---------- 2. 首頁課程卡片 ---------- */
  const grid = document.getElementById("lesson-grid");
  if (grid) {
    grid.innerHTML = lessons.map(l => `
      <a class="lesson-card" href="${root}${l.file}">
        <span class="id">${l.id}</span><span class="level">${l.level}</span>
        <span class="title-vi">${l.vi}</span>
        <span class="title-zh">${l.zh}</span>
        <p class="summary">${l.summary}</p>
      </a>`).join("");
  }

  /* ---------- 3. 上一課 / 下一課 ---------- */
  const current = body.dataset.lesson;
  const navBox = document.getElementById("lesson-nav");
  if (current && navBox) {
    const i = lessons.findIndex(l => l.id === current);
    const prev = lessons[i - 1];
    const next = lessons[i + 1];
    navBox.className = "lesson-nav";
    navBox.innerHTML =
      (prev ? `<a class="prev" href="${root}${prev.file}"><small>← 上一課</small>${prev.id} ${prev.zh}</a>` : `<span class="spacer"></span>`) +
      (next ? `<a class="next" href="${root}${next.file}"><small>下一課 →</small>${next.id} ${next.zh}</a>` : `<a class="next" href="${root}index.html"><small>完成！</small>回到課程列表</a>`);
    if (i >= 0) document.title = `${lessons[i].id} ${lessons[i].zh}｜越來越好`;
  }

  /* ---------- 4. 小測驗 ---------- */
  const items = document.querySelectorAll(".quiz-item");
  const scoreBox = document.getElementById("quiz-score");
  let answered = 0, correct = 0;
  items.forEach(item => {
    const answer = item.dataset.answer;
    const buttons = item.querySelectorAll(".choices button");
    buttons.forEach(btn => {
      btn.addEventListener("click", () => {
        if (item.classList.contains("answered")) return;
        item.classList.add("answered");
        answered++;
        buttons.forEach(b => {
          b.disabled = true;
          if (b.dataset.choice === answer) b.classList.add("correct");
        });
        if (btn.dataset.choice === answer) correct++;
        else btn.classList.add("wrong");
        if (scoreBox) {
          scoreBox.textContent = answered === items.length
            ? `完成！你答對 ${correct} / ${items.length} 題。`
            : `目前答對 ${correct} / ${answered} 題`;
        }
      });
    });
  });

  /* ---------- 5. 朗讀 ---------- */
  if ("speechSynthesis" in window) {
    let viVoice = null;
    const pickVoice = () => {
      viVoice = speechSynthesis.getVoices().find(v => v.lang && v.lang.toLowerCase().startsWith("vi")) || null;
    };
    pickVoice();
    speechSynthesis.onvoiceschanged = pickVoice;

    document.querySelectorAll("[data-say]").forEach(el => {
      const text = el.dataset.say || el.textContent.trim();
      const btn = document.createElement("button");
      btn.className = "say-btn";
      btn.type = "button";
      btn.title = "朗讀（需要裝置有越南語語音）";
      btn.textContent = "🔊";
      btn.addEventListener("click", () => {
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = "vi-VN";
        if (viVoice) u.voice = viVoice;
        u.rate = 0.85;
        speechSynthesis.speak(u);
      });
      el.append(" ", btn);
    });
  }
})();
