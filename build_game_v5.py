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

    .mode-switch {
      position: fixed; top: 25px; left: 50%; transform: translateX(-50%);
      display: flex; background: rgba(0,0,0,0.4); backdrop-filter: blur(15px);
      padding: 6px; border-radius: 999px; z-index: 2000; border: 1px solid rgba(212,175,55,0.25);
    }
    .mode-btn {
      padding: 10px 28px; border-radius: 999px; cursor: pointer; font-weight: bold; font-size: 13px;
      transition: all 0.4s; border: none; background: transparent; color: rgba(244,221,151,0.6);
      text-transform: uppercase; letter-spacing: 1px;
    }
    .mode-btn.active { background: var(--gold); color: black; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }

    /* Home / Oracle View */
    #oracle-view {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      height: 100vh; padding: 20px; text-align: center;
    }

    .brand-logo {
      width: 100px; height: 100px; background: #8f1c19; border-radius: 50%;
      border: 3px solid var(--gold); margin-bottom: 20px;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .brand-logo::after { content: "S"; font-size: 50px; font-weight: bold; color: var(--gold); font-family: cursive; }

    header h1 {
      font-size: 38px; color: var(--gold); margin: 0; font-weight: 400;
      letter-spacing: 2px; text-transform: uppercase;
    }
    header p { font-style: italic; opacity: 0.6; margin-top: 10px; font-size: 18px; }

    /* Elegant Deck Style - NOT a Temple Bucket */
    .deck-container {
      margin-top: 60px; width: 220px; height: 330px; cursor: pointer;
      position: relative; perspective: 1000px;
    }
    .card-pile {
      position: absolute; inset: 0; background: var(--deep-red);
      border-radius: 15px; border: 4px solid var(--gold);
      box-shadow: 
        0 10px 30px rgba(0,0,0,0.6),
        0 5px 0 var(--gold),
        0 8px 15px rgba(0,0,0,0.4);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      background-image: radial-gradient(circle, rgba(212,175,55,0.2) 0%, transparent 70%);
    }
    .card-pile::before {
      content: ""; position: absolute; inset: 10px; border: 1px solid rgba(212,175,55,0.3); border-radius: 10px;
    }
    .card-pile .secret-text {
      font-size: 24px; letter-spacing: 4px; color: var(--gold); text-transform: uppercase; font-weight: 900;
    }

    /* Library View */
    #library-view { display: none; padding: 120px 20px 60px; max-width: 1400px; margin: 0 auto; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 40px; justify-items: center; }

    /* Card Visual Fidelity */
    .card-visual {
      width: var(--card-w); height: var(--card-h);
      background: url("assets/original-card-background.png") center/cover no-repeat;
      border: 14px solid var(--card-border, #9d2b2b);
      border-radius: 24px; position: relative;
      display: flex; flex-direction: column;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8);
      overflow: hidden;
    }
    .card-visual::before { content: ""; position: absolute; inset: 10px; border: 1.5px solid rgba(212, 175, 55, 0.6); border-radius: 12px; pointer-events: none; }
    
    .wax-seal {
      position: absolute; bottom: 30px; left: 30px; width: 55px; height: 55px;
      background: #8f1c19; border-radius: 50%; z-index: 5;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.6); border: 2px solid rgba(212, 175, 55, 0.4);
    }
    .wax-seal::after { content: "Secret"; font-family: "Brush Script MT", cursive; font-size: 11px; color: var(--gold); }

    .card-inner { flex: 1; padding: 70px 35px; display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; text-align: center; }
    h2 { font-size: 25px; font-weight: 900; color: #2d1f19; margin: 0 0 45px; line-height: 1.25; font-family: "PingFang TC", sans-serif; }
    .card-body-text { font-size: 17px; line-height: 1.9; color: #33251f; font-weight: 600; flex: 1; display: flex; align-items: center; justify-content: center; font-family: "PingFang TC", sans-serif; }

    /* Overlay */
    #overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.96); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 3000; padding: 20px; backdrop-filter: blur(15px); }
    .ai-advice { margin-top: 35px; color: var(--gold-light); font-size: 16px; max-width: 340px; line-height: 1.6; text-align: center; font-style: italic; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 20px; }

    .actions { margin-top: 40px; display: flex; gap: 20px; }
    .btn { padding: 15px 40px; border-radius: 999px; font-weight: bold; cursor: pointer; border: none; font-size: 16px; transition: 0.3s; }
    .btn-gold { background: linear-gradient(180deg, #f4dd97, #d4af37); color: #1a0f0d; }
    .btn-outline { background: transparent; border: 2px solid var(--gold); color: var(--gold); }

    /* Shuffling / Drawing Animations */
    .shaking { animation: shuffle 0.6s cubic-bezier(.36,.07,.19,.97) infinite; }
    @keyframes shuffle { 0%, 100% { transform: rotate(0) translateY(0); } 25% { transform: rotate(5deg) translateY(-10px); } 75% { transform: rotate(-5deg) translateY(-5px); } }
    @keyframes flipIn { from { transform: perspective(1000px) rotateY(-90deg) scale(0.7); opacity: 0; } to { transform: perspective(1000px) rotateY(0) scale(1); opacity: 1; } }
    .animate-flip { animation: flipIn 0.8s cubic-bezier(0.23, 1, 0.32, 1) forwards; }

    .library-card { transform: scale(0.9); transition: 0.4s; cursor: pointer; }
    .library-card:hover { transform: scale(0.95); box-shadow: 0 30px 70px rgba(0,0,0,0.9); }
  </style>
</head>
<body>
  <div class="universe"></div>

  <div class="mode-switch">
    <button id="btn-oracle" class="mode-btn active" onclick="switchMode('oracle')">Ask the Secret</button>
    <button id="btn-library" class="mode-btn" onclick="switchMode('library')">The Collection</button>
  </div>
  
  <div id="oracle-view">
    <div class="brand-logo"></div>
    <header>
      <h1>The Secret</h1>
      <p>Manifestation Cards</p>
    </header>
    <div class="deck-container" onclick="handleDraw()">
      <div class="card-pile" id="deck-top">
        <div class="secret-text">The Secret</div>
      </div>
    </div>
    <p style="margin-top: 50px; font-size: 14px; opacity: 0.4; letter-spacing: 3px; text-transform: uppercase;">Tap to receive your guidance</p>
  </div>

  <div id="library-view">
    <header style="text-align:center; margin-bottom: 60px;">
        <h1>The Library</h1>
        <p>Explore the 47 Sacred Truths</p>
    </header>
    <div class="card-grid" id="grid"></div>
  </div>

  <div id="overlay">
    <article id="active-card" class="card-visual">
      <div class="card-inner">
        <h2 id="title">標題</h2>
        <div class="card-body-text" id="text">...</div>
      </div>
      <div class="wax-seal"></div>
    </article>
    <div class="ai-advice" id="explanation">...</div>
    <div class="actions">
      <button class="btn btn-outline" onclick="closeOverlay()">Close</button>
      <button class="btn btn-gold" onclick="alert('Screenshot to manifest this truth!')">Manifest</button>
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
      if (mode === 'library') renderLibrary();
    }

    function renderLibrary() {
      const grid = document.getElementById('grid');
      grid.innerHTML = cards.map(card => {
        const clr = colorMap[card.border_color] || colorMap[card.border_colors[0]] || '#d4af37';
        return `
          <div class="card-visual library-card" style="--card-border: ${clr}" onclick="showSpecificCard('${card.id}')">
            <div class="card-inner">
              <h2>${card.title_zh}</h2>
              <div class="card-body-text">${(card.visible_text || '').substring(0, 70)}...</div>
            </div>
            <div class="wax-seal"></div>
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
      updateOverlay(card, "Focus on this truth and let it sink into your subconscious.");
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

with open('/Users/car/Documents/Codex/2026-05-01/files-mentioned-by-the-user-4cc1c565/secret_oracle_v5.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
