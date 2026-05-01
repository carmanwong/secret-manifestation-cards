import json
import re

with open('/Users/car/Documents/Codex/2026-05-01/files-mentioned-by-the-user-4cc1c565/cards_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract JSON
match = re.search(r'<template id="data">(.*?)</template>', content, re.DOTALL)
if match:
    db_json = match.group(1)
else:
    print("Could not find JSON")
    exit(1)

html_template = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
  <title>祕密實現卡｜求籤系統</title>
  <style>
    :root {
      --gold: #d4af37;
      --gold-bright: #f4dd97;
      --paper: #f9f1d7;
      --deep-red: #5a1f1d;
      --ink: #33251f;
      --shadow: rgba(0, 0, 0, 0.4);
    }
    
    body, html {
      margin: 0; padding: 0; height: 100%; overflow: hidden;
      background: #120908;
      font-family: "PingFang TC", "Noto Serif TC", serif;
      color: var(--paper);
      user-select: none;
    }

    /* 宇宙背景 */
    .universe {
      position: fixed; inset: 0;
      background: 
        radial-gradient(circle at 50% 50%, #4b1c17 0%, #120908 100%);
      z-index: -1;
    }

    .app {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      height: 100vh; padding: 20px; text-align: center;
      position: relative;
    }

    header h1 {
      color: var(--gold); font-size: 32px; margin: 0 0 8px; font-weight: 900;
      text-shadow: 0 2px 10px rgba(212, 175, 55, 0.4);
    }
    header p { opacity: 0.6; font-size: 16px; margin-bottom: 40px; }

    /* 牌堆視覺 */
    .deck-area {
      position: relative; width: 200px; height: 300px;
      cursor: pointer; transition: transform 0.3s;
    }
    .deck-area:active { transform: scale(0.95); }

    .card-back {
      position: absolute; inset: 0;
      background: var(--deep-red);
      border: 6px solid var(--gold);
      border-radius: 12px;
      box-shadow: 0 10px 40px var(--shadow);
      display: flex; align-items: center; justify-content: center;
    }
    .card-back::before { content: ""; position: absolute; inset: -4px; border: 1px solid var(--gold-bright); border-radius: 14px; opacity: 0.3; }
    .card-back span {
      writing-mode: vertical-rl; text-orientation: upright;
      font-size: 36px; font-weight: 900; color: var(--gold);
      letter-spacing: 12px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* 抽牌動畫 */
    .shaking { animation: shake 0.4s infinite; }

    /* 翻牌 Overlay */
    #overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.92);
      display: none; flex-direction: column; align-items: center; justify-content: center;
      z-index: 1000; padding: 20px; backdrop-filter: blur(8px);
    }

    /* Codex 原汁原味卡牌視覺 */
    article {
      width: 320px; aspect-ratio: 2/3;
      background:
        linear-gradient(180deg, rgba(255, 248, 231, 0.08), rgba(244, 224, 177, 0.08)),
        url("assets/original-card-background.png") center/cover no-repeat;
      border: 10px solid var(--card-border, #9d2b2b);
      border-radius: 20px;
      padding: 20px 18px 34px;
      display: flex; flex-direction: column;
      box-shadow: 0 18px 32px rgba(63, 28, 17, 0.26), inset 0 1px 0 rgba(255, 255, 255, 0.6);
      animation: flipIn 0.6s forwards;
      position: relative;
      overflow: hidden;
    }
    article::before {
      content: ""; position: absolute; inset: 12px;
      border: 2px solid rgba(219, 164, 54, 0.68); border-radius: 12px; pointer-events: none;
    }
    article::after {
      content: ""; position: absolute; inset: 0;
      background: radial-gradient(circle at center, rgba(255,255,255,0.32) 0 18%, transparent 56%), linear-gradient(135deg, rgba(255,255,255,0.14), transparent 35%, rgba(0,0,0,0.04) 65%, transparent);
      pointer-events: none; mix-blend-mode: screen;
    }

    .card-head {
      display: flex; align-items: flex-start; justify-content: center;
      position: relative; z-index: 1; min-height: 72px; padding-top: 18px;
    }
    h2 {
      margin: 0; font-size: 21px; line-height: 1.28; color: #2d1f19;
      text-shadow: 0 1px 0 rgba(255,255,255,0.24); text-align: center;
    }
    .text {
      position: relative; z-index: 1; color: var(--ink); line-height: 1.72; font-size: 14px;
      text-align: center; white-space: pre-line; flex: 1; display: flex; align-items: center; justify-content: center;
    }

    .ai-explanation {
      margin-top: 24px; color: var(--gold-bright); font-style: italic; font-size: 15px; max-width: 340px;
      background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 3px solid var(--gold);
    }

    .actions { margin-top: 40px; display: flex; gap: 15px; }
    .btn { padding: 12px 32px; border-radius: 999px; font-weight: bold; cursor: pointer; border: none; font-size: 16px; }
    .btn-gold { background: var(--gold); color: #000; }
    .btn-outline { background: transparent; border: 2px solid var(--gold); color: var(--gold); }

    @keyframes shake { 0%, 100% { transform: rotate(0); } 25% { transform: rotate(2deg); } 75% { transform: rotate(-2deg); } }
    @keyframes flipIn { from { transform: perspective(1000px) rotateY(90deg) scale(0.8); opacity: 0; } to { transform: perspective(1000px) rotateY(0) scale(1); opacity: 1; } }
  </style>
</head>
<body>
  <div class="universe"></div>
  <div class="app">
    <header><h1>祕密實現卡</h1><p>心誠則靈，宇宙會給你最好的安排</p></header>
    <div class="deck-area" onclick="handleDraw()">
      <div class="card-back" id="deck-top"><span>祕密實現</span></div>
    </div>
    <p style="margin-top: 40px; font-size: 14px; opacity: 0.4;">點擊牌堆求取指引</p>
  </div>

  <div id="overlay">
    <article id="active-card" style="--card-border: #d4af37">
      <div class="card-head"><h2 id="title">標題</h2></div>
      <div class="text" id="text">內容...</div>
    </article>
    <div class="ai-explanation" id="explanation">「宇宙正在為你排路，請保持信念。」</div>
    <div class="actions">
      <button class="btn btn-outline" onclick="reset()">重新求籤</button>
      <button class="btn btn-gold" onclick="share()">分享指引</button>
    </div>
  </div>

  <template id="db-json">DB_JSON_PLACEHOLDER</template>

  <script>
    const db = JSON.parse(document.getElementById('db-json').innerHTML);
    const validCards = db.cards.filter(c => c.title_zh); // Only cards with titles
    
    const colorMap = {
      green: '#3a9d5d', red: '#c63b43', pink: '#e06bb2', blue_green: '#45b9c8',
      burgundy: '#7e2a35', blue: '#426fcf', light_blue: '#74d5ef', teal: '#28a79a',
      yellow_green: '#7fb62e', olive: '#a79e28', yellow: '#e2b62a', orange: '#e98f1f', white: '#f2ede1'
    };

    const aiMessages = [
      "「宇宙正在為你排除障礙，請相信當下的直覺。」",
      "「保持高頻率的喜悅，你想要的事物正全速奔向你。」",
      "「放手並交託，最好的結果往往在你不經意時出現。」",
      "「你的思想具有強大磁性，今天請只專注於美好的事物。」",
      "「每一刻都是新的開始，你有權利選擇快樂。」"
    ];

    function handleDraw() {
      const deck = document.getElementById('deck-top');
      deck.classList.add('shaking');
      if (window.navigator.vibrate) window.navigator.vibrate([50, 50, 50]);
      setTimeout(() => { deck.classList.remove('shaking'); revealCard(); }, 800);
    }

    function revealCard() {
      const card = validCards[Math.floor(Math.random() * validCards.length)];
      const msg = aiMessages[Math.floor(Math.random() * aiMessages.length)];
      
      const borderColor = colorMap[card.border_color] || colorMap[card.border_colors[0]] || '#d4af37';
      
      document.getElementById('title').innerText = card.title_zh;
      document.getElementById('text').innerText = card.visible_text || '這是一張需要你用心感悟的卡片。';
      document.getElementById('explanation').innerText = msg;
      document.getElementById('active-card').style.setProperty('--card-color', borderColor);
      document.getElementById('active-card').style.setProperty('--card-border', borderColor);
      
      document.getElementById('overlay').style.display = 'flex';
    }

    function reset() { document.getElementById('overlay').style.display = 'none'; }
    function share() { alert("截圖即可分享你的今日指引！"); }
  </script>
</body>
</html>"""

html_template = html_template.replace('DB_JSON_PLACEHOLDER', db_json)

with open('/Users/car/Documents/Codex/2026-05-01/files-mentioned-by-the-user-4cc1c565/secret_oracle_v2.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Done")
