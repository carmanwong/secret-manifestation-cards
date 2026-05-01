import json
import re

with open('/Users/car/Documents/Codex/2026-05-01/files-mentioned-by-the-user-4cc1c565/cards_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract JSON from Codex's original viewer
match = re.search(r'<template id="data">(.*?)</template>', content, re.DOTALL)
if match:
    db_json = match.group(1)
else:
    print("Error: Could not find JSON data in cards_viewer.html")
    exit(1)

html_template = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
  <title>The Secret Manifestation Cards</title>
  <style>
    :root {
      --gold: #d4af37;
      --gold-light: #f4dd97;
      --paper: #f9f1d7;
      --deep-red: #721c1a;
      --ink: #2b1d16;
      --card-w: 340px;
      --card-h: 560px;
    }
    
    body, html {
      margin: 0; padding: 0; min-height: 100%;
      background: #0d0605;
      font-family: "Baskerville", "Times New Roman", "PingFang TC", serif;
      color: var(--paper);
    }

    .universe {
      position: fixed; inset: 0;
      background: 
        radial-gradient(circle at 50% 50%, #2a0a08 0%, #0d0605 100%),
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
      z-index: -1;
    }

    /* 高級感切換按鈕 */
    .mode-switch {
      position: fixed; top: 25px; left: 50%; transform: translateX(-50%);
      display: flex; background: rgba(0,0,0,0.6); backdrop-filter: blur(20px);
      padding: 6px; border-radius: 999px; z-index: 2000; border: 1px solid rgba(212,175,55,0.3);
      box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    .mode-btn {
      padding: 12px 32px; border-radius: 999px; cursor: pointer; font-weight: bold; font-size: 13px;
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); border: none; background: transparent; 
      color: rgba(244,221,151,0.5); text-transform: uppercase; letter-spacing: 1.5px;
    }
    .mode-btn.active { background: var(--gold); color: #000; box-shadow: 0 4px 15px rgba(212,175,55,0.4); }

    /* Oracle / Ask the Secret View */
    #oracle-view {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      height: 100vh; padding: 20px; text-align: center;
    }

    .brand-seal {
      width: 110px; height: 110px; background: #8f1c19; border-radius: 50%;
      border: 3px solid var(--gold); margin-bottom: 25px;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 15px 40px rgba(0,0,0,0.7); position: relative;
    }
    .brand-seal::after { content: "S"; font-size: 55px; font-weight: bold; color: var(--gold); font-family: cursive; }
    .brand-seal::before { content: ""; position: absolute; inset: -8px; border: 1px solid rgba(212,175,55,0.2); border-radius: 50%; }

    header h1 {
      font-size: 42px; color: var(--gold); margin: 0; font-weight: 400;
      letter-spacing: 4px; text-transform: uppercase; font-family: "Baskerville", serif;
    }
    header p { font-style: italic; opacity: 0.6; margin-top: 15px; font-size: 20px; letter-spacing: 1px; }

    /* Elegant Pile Visualization */
    .deck-container {
      margin-top: 60px; width: 220px; height: 330px; cursor: pointer;
      position: relative; perspective: 1500px;
    }
    .card-stack-effect {
      position: absolute; inset: 0; background: var(--deep-red);
      border-radius: 15px; border: 5px solid var(--gold);
      box-shadow: 
        0 15px 50px rgba(0,0,0,0.8),
        0 6px 0 var(--gold),
        0 12px 20px rgba(0,0,0,0.5);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      background-image: radial-gradient(circle, rgba(212,175,55,0.15) 0%, transparent 80%);
    }
    .card-stack-effect::before { content: ""; position: absolute; inset: 12px; border: 1px solid rgba(212,175,55,0.4); border-radius: 10px; }
    .card-stack-effect .title-vertical { font-size: 26px; letter-spacing: 6px; color: var(--gold); text-transform: uppercase; font-weight: 900; }

    /* Collection / Library View */
    #library-view { display: none; padding: 130px 20px 80px; max-width: 1400px; margin: 0 auto; min-height: 100vh; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 50px; justify-items: center; }

    /* High Fidelity Card Component */
    .card-visual {
      width: var(--card-w); height: var(--card-h);
      background: url("assets/original-card-background.png") center/cover no-repeat;
      border: 14px solid var(--card-border, #9d2b2b);
      border-radius: 24px; position: relative;
      display: flex; flex-direction: column;
      box-shadow: 0 30px 70px rgba(0,0,0,0.8);
      overflow: hidden;
    }
    .card-visual::before { content: ""; position: absolute; inset: 10px; border: 1.5px solid rgba(212, 175, 55, 0.6); border-radius: 12px; pointer-events: none; }
    
    .card-seal-detail {
      position: absolute; bottom: 35px; left: 35px; width: 58px; height: 55px;
      background: #8f1c19; border-radius: 50%; z-index: 5;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.6); border: 2px solid rgba(212, 175, 55, 0.4);
    }
    .card-seal-detail::after { content: "Secret"; font-family: cursive; font-size: 11px; color: var(--gold); font-weight: bold; }

    .card-inner { flex: 1; padding: 75px 40px; display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; text-align: center; }
    h2 { font-size: 26px; font-weight: 900; color: #2d1f19; margin: 0 0 50px; line-height: 1.2; font-family: "PingFang TC", sans-serif; text-shadow: 0 1px 0 rgba(255,255,255,0.3); }
    .card-body-text { font-size: 18px; line-height: 1.95; color: #33251f; font-weight: 600; flex: 1; display: flex; align-items: center; justify-content: center; font-family: "PingFang TC", sans-serif; }

    /* Overlay / Modal */
    #overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.97); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 4000; padding: 20px; backdrop-filter: blur(25px); }
    .ai-wisdom { margin-top: 40px; color: var(--gold-light); font-size: 17px; max-width: 360px; line-height: 1.7; text-align: center; font-style: italic; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 25px; }

    .actions { margin-top: 45px; display: flex; gap: 20px; }
    .btn { padding: 16px 45px; border-radius: 999px; font-weight: 900; cursor: pointer; border: none; font-size: 16px; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
    .btn-gold { background: linear-gradient(180deg, #f4dd97, #d4af37); color: #1a0f0d; box-shadow: 0 5px 20px rgba(212,175,55,0.4); }
    .btn-gold:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(212,175,55,0.6); }
    .btn-outline { background: transparent; border: 2px solid var(--gold); color: var(--gold); }

    /* Animations */
    .shaking { animation: shuffle 0.6s cubic-bezier(.36,.07,.19,.97) infinite; }
    @keyframes shuffle { 0%, 100% { transform: rotate(0) translateY(0); } 25% { transform: rotate(4deg) translateY(-12px); } 75% { transform: rotate(-4deg) translateY(-6px); } }
    @keyframes flipIn { from { transform: perspective(1500px) rotateY(-90deg) scale(0.6); opacity: 0; } to { transform: perspective(1500px) rotateY(0) scale(1); opacity: 1; } }
    .animate-flip { animation: flipIn 0.8s cubic-bezier(0.23, 1, 0.32, 1) forwards; }

    .library-card { transform: scale(0.85); transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; opacity: 0.8; }
    .library-card:hover { transform: scale(0.92) translateY(-10px); opacity: 1; box-shadow: 0 40px 90px rgba(0,0,0,1); z-index: 10; }
    
    @media (max-width: 480px) {
      :root { --card-w: 300px; --card-h: 500px; }
      h2 { font-size: 22px; }
      .card-body-text { font-size: 15px; }
    }
  </style>
</head>
<body>
  <div class="universe"></div>

  <div class="mode-switch">
    <button id="btn-oracle" class="mode-btn active" onclick="switchMode('oracle')">Ask the Secret</button>
    <button id="btn-library" class="mode-btn" onclick="switchMode('library')">The Collection</button>
  </div>
  
  <div id="oracle-view">
    <div class="brand-seal"></div>
    <header>
      <h1>The Secret</h1>
      <p>Manifestation Cards</p>
    </header>
    <div class="deck-container" onclick="handleDraw()">
      <div class="card-stack-effect" id="deck-top">
        <div class="title-vertical">THE SECRET</div>
      </div>
    </div>
    <p style="margin-top: 50px; font-size: 13px; opacity: 0.4; letter-spacing: 4px; text-transform: uppercase;">Tap to align your vibration</p>
  </div>

  <div id="library-view">
    <header style="text-align:center; margin-bottom: 70px;">
        <h1>The Library</h1>
        <p style="opacity:0.6">Explore the 47 Ancient Truths</p>
    </header>
    <div class="card-grid" id="grid"></div>
  </div>

  <div id="overlay">
    <article id="active-card" class="card-visual">
      <div class="card-inner">
        <h2 id="title">標題</h2>
        <div class="card-body-text" id="text">...</div>
      </div>
      <div class="card-seal-detail"></div>
    </article>
    <div class="ai-wisdom" id="explanation">...</div>
    <div class="actions">
      <button class="btn btn-outline" onclick="closeOverlay()">Close</button>
      <button class="btn btn-gold" onclick="alert('This truth is now yours. Screenshot to manifest.')">Manifest</button>
    </div>
  </div>

  <template id="db-json">DB_JSON_PLACEHOLDER</template>

  <script>
    const db = JSON.parse(document.getElementById('db-json').innerHTML);
    const cards = db.cards.filter(c => c.title_zh);
    const colorMap = {
      green: '#3a9d5d', red: '#c63b43', pink: '#e06bb2', blue_green: '#45b9c8',
      burgundy: '#7e2a35', blue: '#426fcf', light_blue: '#74d5ef', teal: '#28a79a',
      yellow_green: '#7fb62e', olive: '#a79e28', yellow: '#e2b62a', orange: '#e98f1f', white: '#f2ede1'
    };

    function switchMode(mode) {
      document.getElementById('oracle-view').style.display = (mode === 'oracle') ? 'flex' : 'none';
      document.getElementById('library-view').style.display = (mode === 'library') ? 'block' : 'none';
      document.getElementById('btn-oracle').classList.toggle('active', mode === 'oracle');
      document.getElementById('btn-library').classList.toggle('active', mode === 'library');
      if (mode === 'library') {
          renderLibrary();
          window.scrollTo(0, 0);
      }
    }

    function renderLibrary() {
      const grid = document.getElementById('grid');
      grid.innerHTML = cards.map(card => {
        const clr = colorMap[card.border_color] || colorMap[card.border_colors[0]] || '#d4af37';
        return `
          <div class="card-visual library-card" style="--card-border: ${clr}" onclick="showSpecificCard('${card.id}')">
            <div class="card-inner">
              <h2>${card.title_zh}</h2>
              <div class="card-body-text">${(card.visible_text || '').substring(0, 65)}...</div>
            </div>
            <div class="card-seal-detail"></div>
          </div>`;
      }).join('');
    }

    function handleDraw() {
      const deck = document.getElementById('deck-top');
      deck.classList.add('shaking');
      setTimeout(() => { deck.classList.remove('shaking'); revealCard(); }, 1200);
    }

    function revealCard() {
      const card = cards[Math.floor(Math.random() * cards.length)];
      updateOverlay(card, "Your thoughts are magnetic. You are attracting this reality right now.");
    }

    function showSpecificCard(id) {
      const card = cards.find(c => c.id === id);
      updateOverlay(card, "Focus on this sacred truth and let it align your frequency.");
    }

    function updateOverlay(card, msg) {
      const clr = colorMap[card.border_color] || colorMap[card.border_colors[0]] || '#d4af37';
      document.getElementById('title').innerText = card.title_zh;
      document.getElementById('text').innerText = card.visible_text || '這是一張充滿能量的卡片。';
      document.getElementById('explanation').innerText = msg;
      document.getElementById('active-card').style.setProperty('--card-border', clr);
      document.getElementById('active-card').classList.remove('animate-flip');
      void document.getElementById('active-card').offsetWidth;
      document.getElementById('active-card').classList.add('animate-flip');
      document.getElementById('overlay').style.display = 'flex';
    }

    function closeOverlay() { document.getElementById('overlay').style.display = 'none'; }
    switchMode('oracle');
  </script>
</body>
</html>"""

html_template = html_template.replace('DB_JSON_PLACEHOLDER', db_json)

with open('/Users/car/Documents/Codex/2026-05-01/files-mentioned-by-the-user-4cc1c565/secret_manifestation_cards.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Build Complete")
