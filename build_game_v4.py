<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
  <title>祕密實現卡｜宇宙能量館</title>
  <style>
    :root {
      --gold: #d4af37;
      --gold-bright: #f4dd97;
      --paper: #f9f1d7;
      --deep-red: #8f1c19;
      --ink: #2b1d16;
      --card-w: 340px;
      --card-h: 560px;
    }
    
    body, html {
      margin: 0; padding: 0; min-height: 100%;
      background: #0d0605;
      font-family: "PingFang TC", "Noto Serif TC", "Songti TC", serif;
      color: var(--paper);
    }

    .universe {
      position: fixed; inset: 0;
      background: radial-gradient(circle at 50% 50%, #3a1510 0%, #0d0605 100%);
      z-index: -1;
    }

    /* 頂部切換按鈕 */
    .mode-switch {
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      display: flex; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
      padding: 5px; border-radius: 999px; z-index: 2000; border: 1px solid rgba(212,175,55,0.3);
    }
    .mode-btn {
      padding: 8px 24px; border-radius: 999px; cursor: pointer; font-weight: bold; font-size: 14px;
      transition: all 0.3s; border: none; background: transparent; color: var(--gold-bright);
    }
    .mode-btn.active { background: var(--gold); color: black; }

    /* 求籤頁面 */
    #oracle-view {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      height: 100vh; padding: 20px; text-align: center;
    }

    /* 瀏覽頁面 (Grid Layout) */
    #library-view {
      display: none; padding: 100px 20px 40px;
      max-width: 1400px; margin: 0 auto;
    }
    .card-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 30px; justify-items: center;
    }

    header h1 {
      color: var(--gold); font-size: 32px; margin: 0 0 10px; font-weight: 900;
      text-shadow: 0 4px 12px rgba(212, 175, 55, 0.5);
    }

    .deck-area { width: 180px; height: 270px; cursor: pointer; position: relative; margin-top: 30px; }
    .card-back {
      position: absolute; inset: 0; background: linear-gradient(135deg, #7e2a27, #4b1c17);
      border: 5px solid var(--gold); border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 15px 45px rgba(0,0,0,0.6); transition: all 0.3s;
    }
    .card-back::after {
      content: "祕密"; writing-mode: vertical-rl; text-orientation: upright;
      font-size: 32px; font-weight: 900; color: var(--gold); letter-spacing: 10px;
    }

    /* 翻牌 Overlay */
    #overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.94);
      display: none; flex-direction: column; align-items: center; justify-content: center;
      z-index: 3000; padding: 20px; backdrop-filter: blur(12px);
    }

    /* 精緻卡牌視覺 */
    .card-visual {
      width: var(--card-w); height: var(--card-h);
      background: url("assets/original-card-background.png") center/cover no-repeat;
      border: 14px solid var(--card-border, #9d2b2b);
      border-radius: 24px; position: relative;
      display: flex; flex-direction: column;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8), inset 0 0 40px rgba(0,0,0,0.1);
      overflow: hidden; text-align: center;
    }

    /* 內部金色細線框 */
    .card-visual::before {
      content: ""; position: absolute; inset: 10px;
      border: 1.5px solid rgba(212, 175, 55, 0.6); border-radius: 12px; pointer-events: none;
    }

    /* 左下角紅印章 (The Secret Logo) */
    .wax-seal {
      position: absolute; bottom: 25px; left: 25px; width: 60px; height: 60px;
      background: #8f1c19; border-radius: 50%; z-index: 5;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 2px 2px 5px rgba(0,0,0,0.4);
      border: 2px solid rgba(212, 175, 55, 0.4);
    }
    .wax-seal::after {
      content: "Secret"; font-family: cursive; font-size: 10px; color: var(--gold); font-weight: bold;
    }

    .card-inner {
      flex: 1; padding: 60px 30px; display: flex; flex-direction: column;
      align-items: center; position: relative; z-index: 2;
    }

    h2 {
      font-size: 26px; font-weight: 900; color: #2d1f19; margin: 0 0 35px;
      line-height: 1.2; text-shadow: 0 1px 1px rgba(255,255,255,0.4);
    }

    .card-body-text {
      font-size: 17px; line-height: 1.85; color: #33251f; font-weight: 600;
      flex: 1; display: flex; align-items: center; justify-content: center;
    }

    .ai-bubble {
      margin-top: 25px; background: rgba(255,236,173,0.08);
      border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px;
      padding: 15px 20px; font-size: 14px; color: var(--gold-bright);
      font-style: italic; max-width: 320px;
    }

    .actions { margin-top: 30px; display: flex; gap: 15px; }
    .btn {
      padding: 12px 30px; border-radius: 999px; font-weight: 900; cursor: pointer;
      border: none; font-size: 15px; transition: all 0.2s;
    }
    .btn-gold { background: linear-gradient(180deg, #f4dd97, #d4af37); color: #2b1d16; }
    .btn-outline { background: transparent; border: 2px solid var(--gold); color: var(--gold); }

    /* Library Mode 專用卡牌 (縮小版) */
    .library-card {
      width: 280px; height: 460px; transform: scale(0.9);
      transition: transform 0.3s; cursor: pointer;
    }
    .library-card:hover { transform: scale(0.95); }
    .library-card h2 { font-size: 20px; margin-bottom: 20px; }
    .library-card .card-body-text { font-size: 14px; line-height: 1.6; }

    /* Animations */
    .shaking { animation: shake 0.4s infinite; }
    @keyframes shake { 0%, 100% { transform: rotate(0); } 25% { transform: rotate(3deg); } 75% { transform: rotate(-3deg); } }
    @keyframes flipIn { from { transform: perspective(1000px) rotateY(90deg) scale(0.8); opacity: 0; } to { transform: perspective(1000px) rotateY(0) scale(1); opacity: 1; } }
    .animate-flip { animation: flipIn 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; }

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
    <button id="btn-oracle" class="mode-btn active" onclick="switchMode('oracle')">今日求籤</button>
    <button id="btn-library" class="mode-btn" onclick="switchMode('library')">瀏覽全集</button>
  </div>
  
  <!-- 求籤 View -->
  <div id="oracle-view" class="app">
    <header><h1>祕密實現館</h1><p>心誠則靈，宇宙會給你最好的安排</p></header>
    <div class="deck-area" onclick="handleDraw()">
      <div class="card-back" id="deck-top"></div>
    </div>
    <p style="margin-top: 40px; font-size: 14px; opacity: 0.4; letter-spacing: 2px;">點擊牌堆求取指引</p>
  </div>

  <!-- 瀏覽 View -->
  <div id="library-view">
    <header style="text-align:center; margin-bottom: 40px;">
        <h1>卡牌典藏</h1>
        <p style="opacity:0.5">目前已收錄 47 張神聖智慧</p>
    </header>
    <div class="card-grid" id="grid"></div>
  </div>

  <!-- 單張顯示 Overlay -->
  <div id="overlay">
    <article id="active-card" class="card-visual">
      <div class="card-inner">
        <h2 id="title">標題</h2>
        <div class="card-body-text" id="text">...</div>
      </div>
      <div class="wax-seal"></div>
    </article>
    <div class="ai-bubble" id="explanation">「這是宇宙今日特別為你準備的訊息。」</div>
    <div class="actions">
      <button class="btn btn-outline" onclick="closeOverlay()">關閉</button>
      <button class="btn btn-gold" onclick="alert('截圖即可分享！')">分享指引</button>
    </div>
  </div>

  <template id="db-json">{
  "deck": {
    "name_zh": "祕密實現卡",
    "name_en": "The Secret Manifestation Cards",
    "author": "Rhonda Byrne",
    "total_cards": 65,
    "language": "繁體中文",
    "source_note": "由使用者提供的商品圖和牌卡照片整理；只收錄圖片中可見或大致可辨認的卡牌。",
    "copyright_note": "建議作個人索引用途。若日後公開網站或 app，請改用摘要、筆記、引用來源或取得授權圖片。"
  },
  "summary": {
    "unique_visible_cards": 47,
    "needs_review_cards": 1,
    "uncertain_sightings": 4,
    "estimated_missing_cards": 18,
    "source_images": 12
  },
  "cards": [
    {
      "id": "SMC-001",
      "title_zh": "感恩之情就是財富",
      "visible_text": "「每日的感恩練習，是財富降臨你身上的管道之一。」—— 華勒思・華特斯（Wallace D. Wattles），《失落的致富經典》作者",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/01_green_gratitude.jpg", "source_images/08_table_green.webp"],
      "visibility": "clear",
      "confidence": 0.99,
      "status": "collected"
    },
    {
      "id": "SMC-002",
      "title_zh": "這個世界喜愛你的快樂",
      "visible_text": "",
      "border_colors": ["red"],
      "border_color": "red",
      "source_images": ["source_images/03_promo_overview.jpg"],
      "visibility": "small_preview",
      "confidence": 0.75,
      "status": "collected"
    },
    {
      "id": "SMC-003",
      "title_zh": "今天來創造你的明天",
      "visible_text": "這是在床上就能進行的強效練習：醒睜、回顧當天的美好時刻，愛心地表示感謝。想想明天，並計劃把明天活成人生中最精采的一天。",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/03_promo_overview.jpg", "source_images/08_table_green.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-004",
      "title_zh": "我有覺察嗎？",
      "visible_text": "要加強覺知，就停下來問自己：「我現在在想什麼？我現在有什麼感覺？」或者，你也可以問自己：「我有覺察嗎？」一旦你這麼問，你就開始覺察了，因為你把你的意念帶回了當下。",
      "border_colors": ["pink"],
      "border_color": "pink",
      "source_images": ["source_images/03_promo_overview.jpg", "source_images/11_table_pink_white.webp"],
      "visibility": "clear",
      "confidence": 0.98,
      "status": "collected"
    },
    {
      "id": "SMC-005",
      "title_zh": "改變意念，改變未來",
      "visible_text": "每天入睡前，回顧這一天的經歷。如果有不如意的事件，就在腦中用你想要的方式重新演練一遍。現在，你已經徹底改變了你的未來。",
      "border_colors": ["blue_green"],
      "border_color": "blue_green",
      "source_images": ["source_images/03_promo_overview.jpg", "source_images/05_table_blue_green.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-006",
      "title_zh": "感恩具有強大的實現力",
      "visible_text": "請記住：想倍增力大或小，是你決定的。不斷感恩引來更多天地，不斷帶可引來更多美好。",
      "border_colors": ["burgundy"],
      "border_color": "burgundy",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "clear",
      "confidence": 0.86,
      "status": "collected",
      "notes": "細字有少量不確定，建議日後用更清晰單卡照校對。"
    },
    {
      "id": "SMC-007",
      "title_zh": "意念會化為現實",
      "visible_text": "",
      "border_colors": ["burgundy"],
      "border_color": "burgundy",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "partial",
      "confidence": 0.9,
      "status": "collected"
    },
    {
      "id": "SMC-008",
      "title_zh": "免於焦慮",
      "visible_text": "一切都聽從吸引力法則向你展現有意義的一切。如果你要焦慮和憂慮，你想要的事物會來嗎？那就做出這個選擇：「我總是無阻的。」",
      "border_colors": ["burgundy"],
      "border_color": "burgundy",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "clear",
      "confidence": 0.82,
      "status": "collected",
      "notes": "標題清楚，內文需校對。"
    },
    {
      "id": "SMC-009",
      "title_zh": "你的願望在於自己",
      "visible_text": "",
      "border_colors": ["burgundy"],
      "border_color": "burgundy",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "clear",
      "confidence": 0.9,
      "status": "collected"
    },
    {
      "id": "SMC-010",
      "title_zh": "你生來就是創作者",
      "visible_text": "",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "partial",
      "confidence": 0.88,
      "status": "collected"
    },
    {
      "id": "SMC-011",
      "title_zh": "沒有限制，沒有欠缺",
      "visible_text": "如果你有這個意識，很可能你在人生中體驗到限制和匱乏。你的心思是過著一切美好的創造力，怎麼會有任何缺乏呢？不可能的！你有無限的念力，所以能化無限的意念為現實。",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "clear",
      "confidence": 0.92,
      "status": "collected"
    },
    {
      "id": "SMC-012",
      "title_zh": "專注於解決問題",
      "visible_text": "當你抗拒目前的處境，你就給予這個處境更多能量和力量。這個事件或狀況只會越來越大，因為這是宇宙的法則。要讓這個你不想要的情況變小，就把你的能量和力量集中在你想要的境遇上。",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-013",
      "title_zh": "改變心念，改變人生",
      "visible_text": "",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/05_table_blue_green.webp"],
      "visibility": "clear",
      "confidence": 0.9,
      "status": "collected"
    },
    {
      "id": "SMC-014",
      "title_zh": "只要專注於豐盛",
      "visible_text": "",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/05_table_blue_green.webp"],
      "visibility": "clear",
      "confidence": 0.9,
      "status": "collected"
    },
    {
      "id": "SMC-015",
      "title_zh": "金錢願望不是努力地朝我而來",
      "visible_text": "",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/05_table_blue_green.webp"],
      "visibility": "partial",
      "confidence": 0.62,
      "status": "needs_review",
      "notes": "標題可見但不夠清晰，可能有字誤。"
    },
    {
      "id": "SMC-016",
      "title_zh": "幸福會吸引你想要的一切",
      "visible_text": "",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/05_table_blue_green.webp"],
      "visibility": "partial",
      "confidence": 0.86,
      "status": "collected"
    },
    {
      "id": "SMC-017",
      "title_zh": "感恩是實現心願的快速通道",
      "visible_text": "想要大幅加快經驗實現的速度，就把感恩融合到創造的三個步驟中：要求、相信、接收。進行第一步「要求」時，不滿於口語和要求物的事物。",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/05_table_blue_green.webp"],
      "visibility": "clear",
      "confidence": 0.88,
      "status": "collected",
      "notes": "內文需校對。"
    },
    {
      "id": "SMC-018",
      "title_zh": "你的人生就在你手中",
      "visible_text": "",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/06_table_blue.webp"],
      "visibility": "clear",
      "confidence": 0.93,
      "status": "collected"
    },
    {
      "id": "SMC-019",
      "title_zh": "思而後行",
      "visible_text": "養成習慣，每天都先在腦海中思考人生事件的後果。在你去任何地方、做任何事之前，都讓宇宙之力為你鋪路。你只要在事情思考你要的發展就行了。如此一來，你就是在有意識地開創人生。",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/06_table_blue.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-020",
      "title_zh": "相信你已經收到了",
      "visible_text": "宇宙不需要時間來實現你的願望。你慢慢得到的不準時，是因為你還不相信。不知道、沒感覺到你已經擁有，這是因為你把自己放在「想要」的頻率上。當你把自己放在「已經擁有」的頻率上，你想要的就會出現。",
      "border_colors": ["blue_green"],
      "border_color": "blue_green",
      "source_images": ["source_images/06_table_blue.webp"],
      "visibility": "clear",
      "confidence": 0.92,
      "status": "collected",
      "notes": "內文需校對。"
    },
    {
      "id": "SMC-021",
      "title_zh": "人生應該輕鬆不費力",
      "visible_text": "",
      "border_colors": ["light_blue"],
      "border_color": "light_blue",
      "source_images": ["source_images/06_table_blue.webp"],
      "visibility": "clear",
      "confidence": 0.93,
      "status": "collected"
    },
    {
      "id": "SMC-022",
      "title_zh": "吸引力法則一直在聽",
      "visible_text": "如果你覺得人生很困苦、艱難，根據吸引力法則，你的人生就會變得很困苦、艱難。現在就改口：「人生輕鬆不費力。」「人生很精彩。」「所有的好事都會降臨在我身上。」「一切都會順順利利。」",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/06_table_blue.webp"],
      "visibility": "clear",
      "confidence": 0.95,
      "status": "collected"
    },
    {
      "id": "SMC-023",
      "title_zh": "善意是雙贏的",
      "visible_text": "當你對別人懷有善意，你將會體驗到那些善意體驗在你身上。你不能用惡意傷害別人，你只會傷害自己。如果你對他人抱有善念，猜猜誰會受惠？就是你！",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/06_table_blue.webp"],
      "visibility": "clear",
      "confidence": 0.97,
      "status": "collected"
    },
    {
      "id": "SMC-024",
      "title_zh": "注意力就是一切",
      "visible_text": "如果你在想某件事、在談論某件事，你就是在邀請這件事來到你的生命中。",
      "border_colors": ["blue"],
      "border_color": "blue",
      "source_images": ["source_images/07_table_teal.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-025",
      "title_zh": "多想想你要什麼",
      "visible_text": "人之所以沒有活在夢想中的人生裡，唯一的原因在於：他們太常想著自己不想要什麼，而不是他們想要什麼。實際上，如果你只想著你要什麼，你就只會得到你所想要的。",
      "border_colors": ["light_blue"],
      "border_color": "light_blue",
      "source_images": ["source_images/07_table_teal.webp"],
      "visibility": "clear",
      "confidence": 0.95,
      "status": "collected"
    },
    {
      "id": "SMC-026",
      "title_zh": "在你動念之前……",
      "visible_text": "「每個意念都成真，除非你用相反的意念去抵消它。」—— 萊斯特・雷文森（Lester Levenson），生命導師",
      "border_colors": ["light_blue"],
      "border_color": "light_blue",
      "source_images": ["source_images/07_table_teal.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-027",
      "title_zh": "改變人生就靠感恩",
      "visible_text": "感恩帶來教育，抱怨帶來教育，這是你選擇手中的黃金守則。適用於幸福與健康、人際關係、工作與財富。",
      "border_colors": ["teal"],
      "border_color": "teal",
      "source_images": ["source_images/07_table_teal.webp"],
      "visibility": "clear",
      "confidence": 0.86,
      "status": "collected",
      "notes": "內文有字詞需校對。"
    },
    {
      "id": "SMC-028",
      "title_zh": "你擁有無懈可擊的健康",
      "visible_text": "",
      "border_colors": ["teal"],
      "border_color": "teal",
      "source_images": ["source_images/07_table_teal.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-029",
      "title_zh": "珍惜會強化人際關係",
      "visible_text": "想要讓一段很難經營的關係變得更好，我們就要把注意力集中在欣賞對方。當我們抱怨一段關係時，就只會吸引更多想要抱怨的事情。在接下來的 28 天裡，寫下你欣賞對方的所有事情，每天都多寫一點點，你將會看到你的珍惜如何化腐朽為神奇。",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/07_table_teal.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-030",
      "title_zh": "數算你的祝福",
      "visible_text": "養成每天坐下來寫下十項祝福的習慣。即使你只做這個練習，它也能翻轉你的人生。",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/08_table_green.webp"],
      "visibility": "clear",
      "confidence": 0.97,
      "status": "collected"
    },
    {
      "id": "SMC-031",
      "title_zh": "想要有精彩的一天，就讓早晨充滿感恩之心",
      "visible_text": "你可以和我一樣，下床走去浴室或廚房的時候，就輕柔而緩慢地步伐，每踏出一步都說「謝謝」。你正在感謝你所擁有的一切、你愛的每一個人，還有今天即將發生的一切好事！",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/08_table_green.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-032",
      "title_zh": "現在就選擇幸福",
      "visible_text": "抗拒可能讓你願望實現。當你不能定自己是否能實現你想要的一切，而開始感到焦慮或偏離時，就是在創造抗拒和阻礙。只要在願望還沒實現之前，現在找到一種感覺幸福快樂的方式，你就可以消除這些創造抗拒、阻礙心願的負面感受。",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/08_table_green.webp"],
      "visibility": "clear",
      "confidence": 0.88,
      "status": "collected",
      "notes": "內文需校對。"
    },
    {
      "id": "SMC-033",
      "title_zh": "感激你所擁有的一切",
      "visible_text": "當你對你所擁有的一切心存感激，你不僅會看到你所擁有的事物越來越多，同時你也會打開一道大門，迎接你渴望的一切，迎來真正幸福圓滿的人生。",
      "border_colors": ["green"],
      "border_color": "green",
      "source_images": ["source_images/08_table_green.webp"],
      "visibility": "clear",
      "confidence": 0.97,
      "status": "collected"
    },
    {
      "id": "SMC-034",
      "title_zh": "你抗拒的一直都在",
      "visible_text": "顯然不想論你多堅強烈地不想要某事，你都在邀請那件事靠近你。不抗拒你的強烈情緒投放在你想要的事物上，將你想要的事物引向你。",
      "border_colors": ["yellow_green"],
      "border_color": "yellow_green",
      "source_images": ["source_images/09_table_olive_yellow.webp"],
      "visibility": "clear",
      "confidence": 0.84,
      "status": "collected",
      "notes": "內文需校對。"
    },
    {
      "id": "SMC-035",
      "title_zh": "注意力就是實現力",
      "visible_text": "加上情緒的專注就是強大的實現力！",
      "border_colors": ["olive"],
      "border_color": "olive",
      "source_images": ["source_images/09_table_olive_yellow.webp"],
      "visibility": "clear",
      "confidence": 0.95,
      "status": "collected"
    },
    {
      "id": "SMC-036",
      "title_zh": "過最棒的一天",
      "visible_text": "你是否為今天做了計畫？還是你打算睡昨天的思緒，繼續主導著今天？以下這些話能帶給你好的開始：今天所有的好事都會降臨到我身上。今天我的願望都能實現。今天魔法和奇蹟會一直跟隨著我。",
      "border_colors": ["olive"],
      "border_color": "olive",
      "source_images": ["source_images/09_table_olive_yellow.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-037",
      "title_zh": "你有能力締造世界和平",
      "visible_text": "這個世界會變化，我們的地球會變化，如同每個人的內心都在變化，一個人可以影響千萬其他人，他們再次影響千萬人，該千萬人又會影響十億人，我們就是用這個方式為地球帶來和平、和諧。",
      "border_colors": ["yellow"],
      "border_color": "yellow",
      "source_images": ["source_images/09_table_olive_yellow.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-038",
      "title_zh": "幸福吸引幸福",
      "visible_text": "這個公式真是簡單明瞭。你必須現在就感到幸福快樂，才能憑藉吸引力法則，把讓你感到幸福快樂的一切吸引到生命中。",
      "border_colors": ["orange"],
      "border_color": "orange",
      "source_images": ["source_images/10_table_orange_red.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-039",
      "title_zh": "你的力量就在心中",
      "visible_text": "當你越想越糟時，運用方法可以讓你停下來：深吸一口氣，把注意力集中在心口，專注感受心中的愛。",
      "border_colors": ["orange"],
      "border_color": "orange",
      "source_images": ["source_images/10_table_orange_red.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-040",
      "title_zh": "你的自然狀態就是喜悅",
      "visible_text": "",
      "border_colors": ["orange"],
      "border_color": "orange",
      "source_images": ["source_images/10_table_orange_red.webp"],
      "visibility": "clear",
      "confidence": 0.93,
      "status": "collected"
    },
    {
      "id": "SMC-041",
      "title_zh": "你只需要保持正面和善意",
      "visible_text": "想要活出最精采的人生，其實很簡單：正面的意念、正面的話語、善意的舉動，就是這樣！",
      "border_colors": ["orange"],
      "border_color": "orange",
      "source_images": ["source_images/10_table_orange_red.webp"],
      "visibility": "clear",
      "confidence": 0.97,
      "status": "collected"
    },
    {
      "id": "SMC-042",
      "title_zh": "感謝你所面對的挑戰",
      "visible_text": "",
      "border_colors": ["red"],
      "border_color": "red",
      "source_images": ["source_images/10_table_orange_red.webp"],
      "visibility": "partial",
      "confidence": 0.88,
      "status": "collected"
    },
    {
      "id": "SMC-043",
      "title_zh": "金錢不能帶來快樂，但快樂能創造金錢",
      "visible_text": "如果你一直想著「我需要錢」，那你就會一直吸引「需要錢」的境遇。你現在必須找到不用錢就能快樂的方式，現在就感到心滿意足，沉浸在喜悅中，因為美好的感覺才是把金錢吸引過來的關鍵。",
      "border_colors": ["red"],
      "border_color": "red",
      "source_images": ["source_images/10_table_orange_red.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    },
    {
      "id": "SMC-044",
      "title_zh": "你是永恆的存在",
      "visible_text": "",
      "border_colors": ["white"],
      "border_color": "white",
      "source_images": ["source_images/11_table_pink_white.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-045",
      "title_zh": "地球為你而轉動",
      "visible_text": "",
      "border_colors": ["pink"],
      "border_color": "pink",
      "source_images": ["source_images/11_table_pink_white.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-046",
      "title_zh": "你想什麼，你就成為什麼",
      "visible_text": "",
      "border_colors": ["pink"],
      "border_color": "pink",
      "source_images": ["source_images/11_table_pink_white.webp"],
      "visibility": "clear",
      "confidence": 0.94,
      "status": "collected"
    },
    {
      "id": "SMC-047",
      "title_zh": "現在就給自己好心情",
      "visible_text": "現在就愛開心，現在就感受好心情，這是你唯一需要做的事情。如果這是你從這套牌卡得到的唯一訊息，那麼你已經獲得了《祕密》裡最重要的一部分。",
      "border_colors": ["pink"],
      "border_color": "pink",
      "source_images": ["source_images/11_table_pink_white.webp"],
      "visibility": "clear",
      "confidence": 0.96,
      "status": "collected"
    }
  ],
  "uncertain_sightings": [
    {
      "title_guess": "一切自然在安然在正軌上",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "reason": "標題細字模糊，暫不列入 confirmed unique count。"
    },
    {
      "title_guess": "金錢富足好能……",
      "source_images": ["source_images/04_table_burgundy.webp"],
      "reason": "只見到部分標題。"
    },
    {
      "title_guess": "你的焦點是說，世界感謝你的心靈而動",
      "source_images": ["source_images/09_table_olive_yellow.webp"],
      "reason": "標題可能讀錯，需要更清晰圖片。"
    },
    {
      "title_guess": "底部中間橄欖色卡牌",
      "source_images": ["source_images/09_table_olive_yellow.webp"],
      "reason": "被黃色手持卡遮住，未能辨認。"
    }
  ],
  "missing_slots": [
    {"id": "SMC-MISSING-048", "status": "not_seen"},
    {"id": "SMC-MISSING-049", "status": "not_seen"},
    {"id": "SMC-MISSING-050", "status": "not_seen"},
    {"id": "SMC-MISSING-051", "status": "not_seen"},
    {"id": "SMC-MISSING-052", "status": "not_seen"},
    {"id": "SMC-MISSING-053", "status": "not_seen"},
    {"id": "SMC-MISSING-054", "status": "not_seen"},
    {"id": "SMC-MISSING-055", "status": "not_seen"},
    {"id": "SMC-MISSING-056", "status": "not_seen"},
    {"id": "SMC-MISSING-057", "status": "not_seen"},
    {"id": "SMC-MISSING-058", "status": "not_seen"},
    {"id": "SMC-MISSING-059", "status": "not_seen"},
    {"id": "SMC-MISSING-060", "status": "not_seen"},
    {"id": "SMC-MISSING-061", "status": "not_seen"},
    {"id": "SMC-MISSING-062", "status": "not_seen"},
    {"id": "SMC-MISSING-063", "status": "not_seen"},
    {"id": "SMC-MISSING-064", "status": "not_seen"},
    {"id": "SMC-MISSING-065", "status": "not_seen"}
  ]
}
</template>

  <script>
    const db = JSON.parse(document.getElementById('db-json').innerHTML);
    const cards = db.cards.filter(c => c.title_zh);
    
    const colorMap = {
      green: '#3a9d5d', red: '#c63b43', pink: '#e06bb2', blue_green: '#45b9c8',
      burgundy: '#7e2a35', blue: '#426fcf', light_blue: '#74d5ef', teal: '#28a79a',
      yellow_green: '#7fb62e', olive: '#a79e28', yellow: '#e2b62a', orange: '#e98f1f', white: '#f2ede1'
    };

    const aiMessages = [
      "「宇宙正在為你排除障礙，請相信當下的直覺。」",
      "「保持高頻率的喜悅，你想要的事物正全速奔向你。」",
      "「放手並交託，最好的結果往往在你不經意時出現。」",
      "「你的思想具有強大磁性，今天請只專注於美好的事物。」"
    ];

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
              <div class="card-body-text">${(card.visible_text || '').substring(0, 80)}...</div>
            </div>
            <div class="wax-seal"></div>
          </div>
        `;
      }).join('');
    }

    function handleDraw() {
      const deck = document.getElementById('deck-top');
      deck.classList.add('shaking');
      setTimeout(() => { deck.classList.remove('shaking'); revealCard(); }, 800);
    }

    function revealCard() {
      const card = cards[Math.floor(Math.random() * cards.length)];
      updateOverlay(card, aiMessages[Math.floor(Math.random() * aiMessages.length)]);
    }

    function showSpecificCard(id) {
      const card = cards.find(c => c.id === id);
      updateOverlay(card, "「細細品味這張卡片的智慧。」");
    }

    function updateOverlay(card, msg) {
      const clr = colorMap[card.border_color] || colorMap[card.border_colors[0]] || '#d4af37';
      document.getElementById('title').innerText = card.title_zh;
      document.getElementById('text').innerText = card.visible_text || '這是一張充滿能量的卡片。';
      document.getElementById('explanation').innerText = msg;
      document.getElementById('active-card').style.setProperty('--card-border', clr);
      document.getElementById('active-card').classList.remove('animate-flip');
      void document.getElementById('active-card').offsetWidth; // Trigger reflow
      document.getElementById('active-card').classList.add('animate-flip');
      document.getElementById('overlay').style.display = 'flex';
    }

    function closeOverlay() { document.getElementById('overlay').style.display = 'none'; }
    switchMode('oracle');
  </script>
</body>
</html>