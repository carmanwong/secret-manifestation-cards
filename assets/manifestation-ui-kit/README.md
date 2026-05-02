# Manifestation UI Kit

這批素材由 `2026-05-02` 放喺 `Downloads` 嘅 GPT 生成圖整理而成，分成兩類：

- `design-reference/`
  - 用嚟定視覺方向、版面層次、情緒氣氛。
- `ui-kit/`
  - 已抽出、可直接放入 app 嘅透明資產。
- `backgrounds/`
  - 可直接做 full-screen 背景或 section 背景。

## 建議主方向

而家最值得做成真 app 嘅方向係：

- `home-entrance-concept.png`
  - 最適合做 app 首頁入口。
- `library-screen-concept.png`
  - 最清楚展示卡牌庫 / 篩選 / 搜尋結構。
- `card-result-screen-concept-b.png`
  - 最成熟，適合做抽卡結果頁主稿。

`card-result-screen-concept-a.png` 偏原始卡牌閱讀頁，可以保留做 alternative result layout。

## 檔案對照

### design-reference

- `home-entrance-concept.png`
  - 首頁、問題輸入、主卡牌 deck、主 CTA。
- `library-screen-concept.png`
  - 卡牌庫、搜尋欄、分類 chip、底部導覽。
- `card-result-screen-concept-a.png`
  - 結果頁版本 A，偏長文閱讀。
- `card-result-screen-concept-b.png`
  - 結果頁版本 B，偏 ritual/game 感。

### backgrounds

- `golden-altar-background.png`
  - 可用作首頁、結果頁、載入頁嘅主背景。

### ui-kit

- `cta-draw-card-red.png`
  - 「抽一張卡」主按鈕。
- `cta-open-library-cream.png`
  - 「瀏覽卡牌庫」次按鈕。
- `cta-save-card-pink.png`
  - 「收藏這張牌」主動作按鈕。
- `cta-redraw-cream.png`
  - 「再抽一張」按鈕。
- `row-share-card.png`
  - 「分享這張牌卡」橫列操作。
- `panel-daily-reflection-cream.png`
  - 結果頁底部反思 / 筆記 panel。
- `prompt-question-pill.png`
  - 首頁問題輸入提示區 / prompt pill。
- `card-face-what-do-i-want.png`
  - 單張卡面示例，可作卡牌 detail / mock card asset。

## 實作建議

- 首頁先用 CSS 還原 `home-entrance-concept.png` 嘅結構。
- 唔好將整張 concept 直接當 screenshot 背景塞入 app。
- `ui-kit/` 內嘅透明圖可以直接做 `<img>` asset，或者逐步用 CSS / SVG 重構。
- 長遠最穩陣做法係：
  - 先用圖片資產快速出一版
  - 再將重要元件逐件 code-native 化

## 下一步

下一步應該基於呢批素材，將 `secret_oracle_v6.html` 重做成：

- 首頁 / 抽卡入口
- 卡牌庫
- 抽卡結果頁

而唔再只係單頁 demo。
