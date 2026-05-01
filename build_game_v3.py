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
  <title>祕密實現卡｜宇宙求籤</title>
  <style>
    :root {
      --gold: #d4af37;
      --gold-bright: #f4dd97;
      --paper: #f9f1d7;
      --deep-red: #5a1f1d;
      --ink: #2b1d16;
      --card-w: 340px;
      --card-h: 560px;
    }
    
    body, html {
      margin: 0; padding: 0; height: 100%; overflow: hidden;
      background: #0d0605;
      font-family: "PingFang TC", "Noto Serif TC", serif;
      color: var(--paper);
    }

    .universe {
      position: fixed; inset: 0;
      background: radial-gradient(circle at 50% 50%, #3a1510 0%, #0d0605 100%);
      z-index: -1;
    }

    .app {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      height: 100vh; padding: 20px;
    }

    header h1 {
      color: var(--gold); font-size: 36px; margin: 0 0 10px; font-weight: 900;
      text-shadow: 0 4px 12px rgba(212, 175, 55, 0.5);
    }
    header p { opacity: 0.5; font-size: 15px; margin-bottom: 50px; }

    .deck-area {
      width: 180px; height: 270px; cursor: pointer;
      position: relative;
    }
    .card-back {
      position: absolute; inset: 0;
      background: linear-gradient(135deg, #7e2a27, #4b1c17);
      border: 5px solid var(--gold); border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 15px 45px rgba(0,0,0,0.6);
      transition: all 0.3s;
    }
    .card-back::after {
      content: "祕密"; writing-mode: vertical-rl; text-orientation: upright;
      font-size: 32px; font-weight: 900; color: var(--gold); letter-spacing: 10px;
    }

    #overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.94);
      display: none; flex-direction: column; align-items: center; justify-content: center;
      z-index: 1000; padding: 20px; backdrop-filter: blur(12px);
    }

    /* 修正後的卡牌尺寸與比例 */
    article {
      width: var(--card-w); height: var(--card-h);
      background: url("assets/original-card-background.png") center/cover no-repeat;
      border: 14px solid var(--card-border, #9d2b2b);
      border-radius: 24px;
      position: relative;
      display: flex; flex-direction: column;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8), inset 0 0 40px rgba(0,0,0,0.1);
      animation: revealCard 0.7s cubic-bezier(0.23, 1, 0.32, 1) forwards;
      overflow: hidden;
    }

    /* 燙金邊框裝飾 */
    article::before {
      content: ""; position: absolute; inset: 10px;
      border: 2px solid rgba(212, 175, 55, 0.7); border-radius: 12px; pointer-events: none;
    }

    .card-content {
      flex: 1; padding: 50px 30px; display: flex; flex-direction: column;
      align-items: center; text-align: center; position: relative; z-index: 2;
    }

    h2 {
      font-size: 28px; font-weight: 900; color: #2d1f19; margin: 0 0 40px;
      line-height: 1.3; text-shadow: 0 1px 1px rgba(255,255,255,0.4);
    }

    .main-text {
      font-size: 19px; line-height: 1.9; color: #33251f; font-weight: 600;
      flex: 1; display: flex; align-items: center; justify-content: center;
    }

    /* 下方 AI 解說泡泡 */
    .ai-bubble {
      margin-top: 30px; background: rgba(255,236,173,0.08);
      border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px;
      padding: 18px 20px; font-size: 15px; color: var(--gold-bright);
      font-style: italic; max-width: 320px;
    }

    .actions { margin-top: 35px; display: flex; gap: 20px; }
    .btn {
      padding: 14px 36px; border-radius: 999px; font-weight: 900; cursor: pointer;
      border: none; font-size: 17px; transition: all 0.2s;
    }
    .btn-gold { background: linear-gradient(180deg, #f4dd97, #d4af37); color: #2b1d16; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); }
    .btn-outline { background: transparent; border: 2px solid var(--gold); color: var(--gold); }

    @keyframes revealCard {
      0% { transform: perspective(1000px) rotateX(-20deg) translateY(50px) scale(0.8); opacity: 0; }
      100% { transform: perspective(1000px) rotateX(0) translateY(0) scale(1); opacity: 1; }
    }
    .shaking { animation: shake 0.4s infinite; }
    @keyframes shake { 0%, 100% { transform: rotate(0); } 25% { transform: rotate(3deg); } 75% { transform: rotate(-3deg); } }

    @media (max-height: 700px) {
      :root { --card-w: 280px; --card-h: 460px; }
      h2 { font-size: 22px; margin-bottom: 20px; }
      .main-text { font-size: 16px; }
    }
  </style>
</head>
<body>
  <div class="universe"></div>
  <div class="app">
    <header><h1>祕密實現卡</h1><p>專注於你想要的，宇宙會為你鋪路</p></header>
    <div class="deck-area" onclick="handleDraw()"><div class="card-back" id="deck-top"></div></div>
    <p style="margin-top: 50px; font-size: 14px; opacity: 0.4; letter-spacing: 2px;">點擊牌堆獲取啟發</p>
  </div>

  <div id="overlay">
    <article id="active-card">
      <div class="card-content">
        <h2 id="title">標題</h2>
        <div class="main-text" id="text">...</div>
      </div>
    </article>
    <div class="ai-bubble" id="explanation">「保持正向意念，奇蹟即將發生。」</div>
    <div class="actions">
      <button class="btn btn-outline" onclick="reset()">重新求籤</button>
      <button class="btn btn-gold" onclick="share()">分享指引</button>
    </div>
  </div>

  <template id="db-json">DB_JSON_PLACEHOLDER</template>

  <script>
    const db = JSON.parse(document.getElementById('db-json').innerHTML);
    const validCards = db.cards.filter(c => c.title_zh);
    
    const colorMap = {
      green: '#3a9d5d', red: '#c63b43', pink: '#e06bb2', blue_green: '#45b9c8',
      burgundy: '#7e2a35', blue: '#426fcf', light_blue: '#74d5ef', teal: '#28a79a',
      yellow_green: '#7fb62e', olive: '#a79e28', yellow: '#e2b62a', orange: '#e98f1f', white: '#f2ede1'
    };

    function handleDraw() {
      const deck = document.getElementById('deck-top');
      deck.classList.add('shaking');
      if (window.navigator.vibrate) window.navigator.vibrate([40, 40, 40]);
      setTimeout(() => { deck.classList.remove('shaking'); revealCard(); }, 800);
    }

    function revealCard() {
      const card = validCards[Math.floor(Math.random() * validCards.length)];
      const borderColor = colorMap[card.border_color] || colorMap[card.border_colors[0]] || '#d4af37';
      
      document.getElementById('title').innerText = card.title_zh;
      document.getElementById('text').innerText = card.visible_text || '這是一張需要你用心感悟的卡片。';
      document.getElementById('active-card').style.setProperty('--card-border', borderColor);
      
      document.getElementById('overlay').style.display = 'flex';
    }

    function reset() { document.getElementById('overlay').style.display = 'none'; }
    function share() { alert("已為你鎖定這份指引，截圖即可分享！"); }
  </script>
</body>
</html>"""

html_template = html_template.replace('DB_JSON_PLACEHOLDER', db_json)

with open('/Users/car/Documents/Codex/2026-05-01/files-mentioned-by-the-user-4cc1c565/secret_oracle_v3.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("V3 Done")
