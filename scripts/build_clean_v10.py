import re
import os
import json

keiba_app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_html_path = os.path.join(keiba_app_dir, 'index.html')
main_js_path = os.path.join(keiba_app_dir, 'src', 'main.js')
style_css_path = os.path.join(keiba_app_dir, 'src', 'style.css')
entries_json_path = os.path.join(keiba_app_dir, 'src', 'entries_data.json')
pred_json_path = os.path.join(keiba_app_dir, 'src', 'prediction_data.json')
payouts_json_path = os.path.join(keiba_app_dir, 'src', 'payouts_data.json')
hist_js_path = os.path.join(keiba_app_dir, 'src', 'historical_results.js')
base_html_path = os.path.join(keiba_app_dir, 'scripts', 'data', 'orig_index.html')
autumn_json_path = os.path.join(keiba_app_dir, 'scripts', 'data', 'scraped_2026_autumn.json')

with open(base_html_path, 'r', encoding='utf-8') as f:
    base_html = f.read()

with open(pred_json_path, 'r', encoding='utf-8') as f:
    pred_data = json.load(f)

with open(entries_json_path, 'r', encoding='utf-8') as f:
    entries_data = json.load(f)

with open(payouts_json_path, 'r', encoding='utf-8') as f:
    payouts_data = json.load(f)

with open(autumn_json_path, 'r', encoding='utf-8') as f:
    autumn_data = json.load(f)

with open(hist_js_path, 'r', encoding='utf-8') as f:
    hist_raw = f.read()
h_match = re.search(r'export const HISTORICAL_FULL_RESULTS = (\{[\s\S]*?\});\s*$', hist_raw)
hist_full_data = json.loads(h_match.group(1))

# Extract G1_RACES (all 24 races)
g1_match = re.search(r'const G1_RACES = (\[[\s\S]*?\n\s*\]);', base_html)
g1_races_raw = g1_match.group(1)

# In G1_RACES, update 13, 14, 15, 16 to finished
g1_13_finished = """        {
          id: '13',
          name: 'スプリンターズステークス',
          englishName: 'Sprinters Stakes',
          date: '2026-09-27T15:40:00',
          location: '中山',
          course: '芝 1200m',
          status: 'finished',
          weather: '曇',
          trackCondition: '稍重',
          cushionValue: '9.1',
          type: 'older-mile',
          winner: 'ピューロマジック', winnerJockey: '岩田望来', winnerGate: 16, time: '1:09.2',
          second: 'ワールズエンド', secondJockey: '津村明秀', secondGate: 6,
          third: 'サウンドモリアーナ', thirdJockey: '吉田隼人', thirdGate: 5,
          payouts: { win: 2450, trifecta: 462120 }
        }"""

g1_14_finished = """        {
          id: '14',
          name: '秋華賞',
          englishName: 'Shuka Sho',
          date: '2026-10-18T15:40:00',
          location: '京都',
          course: '芝 2000m',
          status: 'finished',
          weather: '晴',
          trackCondition: '良',
          cushionValue: '9.6',
          type: 'three-year-old',
          winner: 'チェルヴィニア', winnerJockey: 'C.ルメール', winnerGate: 5, time: '1:57.1',
          second: 'ボンドガール', secondJockey: '武豊', secondGate: 10,
          third: 'ステレンボッシュ', thirdJockey: '戸崎圭太', thirdGate: 14,
          payouts: { win: 530, trifecta: 11940 }
        }"""

g1_15_finished = """        {
          id: '15',
          name: '菊花賞',
          englishName: 'Kikuka Sho',
          date: '2026-10-25T15:40:00',
          location: '京都',
          course: '芝 3000m',
          status: 'finished',
          weather: '晴',
          trackCondition: '良',
          cushionValue: '9.8',
          type: 'three-year-old',
          winner: 'アーバンシック', winnerJockey: 'C.ルメール', winnerGate: 13, time: '3:04.1',
          second: 'ヘデントール', secondJockey: '戸崎圭太', secondGate: 16,
          third: 'アドマイヤテラ', thirdJockey: '武豊', thirdGate: 17,
          payouts: { win: 370, trifecta: 19260 }
        }"""

g1_16_finished = """        {
          id: '16',
          name: '天皇賞（秋）',
          englishName: 'Tenno Sho (Autumn)',
          date: '2026-11-01T15:40:00',
          location: '東京',
          course: '芝 2000m',
          status: 'finished',
          weather: '晴',
          trackCondition: '良',
          cushionValue: '9.5',
          type: 'older-middle',
          winner: 'ダノンデサイル', winnerJockey: '戸崎圭太', winnerGate: 17, time: '1:56.7',
          second: 'ネブラディスク', secondJockey: '川田将雅', secondGate: 10,
          third: 'レガレイラ', thirdJockey: '岩田望来', thirdGate: 3,
          payouts: { win: 1080, trifecta: 297820 }
        }"""

g1_races_raw = re.sub(r'\{\s*id:\s*\'13\'[\s\S]*?\}', g1_13_finished.strip(), g1_races_raw)
g1_races_raw = re.sub(r'\{\s*id:\s*\'14\'[\s\S]*?\}', g1_14_finished.strip(), g1_races_raw)
g1_races_raw = re.sub(r'\{\s*id:\s*\'15\'[\s\S]*?\}', g1_15_finished.strip(), g1_races_raw)
g1_races_raw = re.sub(r'\{\s*id:\s*\'16\'[\s\S]*?\}', g1_16_finished.strip(), g1_races_raw)

g1_races_str = f"const G1_RACES = {g1_races_raw};"

# Extract RESULTS_DATA and inject autumn data
results_match = re.search(r'const RESULTS_DATA = (\{[\s\S]*?\n\s*\});', base_html)
results_raw = results_match.group(1)
res_dict = {}
for i in range(1, 13):
    m = re.search(rf"'{i}':\s*(\[[\s\S]*?\])(?=,\s*'\d+'|\s*\}})", results_raw)
    if m:
        res_dict[str(i)] = json.loads(m.group(1).replace("'", '"'))

res_dict['13'] = autumn_data['13']
res_dict['14'] = autumn_data['14']
res_dict['15'] = autumn_data['15']
res_dict['16'] = autumn_data['16']

new_results_data_str = "const RESULTS_DATA = " + json.dumps(res_dict, ensure_ascii=False, indent=2) + ";"

# Generate complete HISTORICAL_DATA for ALL 24 RACES (2016-2025)
base_hist = json.loads(re.search(r'const HISTORICAL_DATA = (\{[\s\S]*?\n\s*\});', base_html).group(1).replace("'", '"'))
full_hist_summary = {}

for r_id in map(str, range(1, 25)):
    if r_id in base_hist and len(base_hist[r_id]) >= 10:
        full_hist_summary[r_id] = base_hist[r_id]
    elif r_id in hist_full_data:
        race_years = hist_full_data[r_id]
        sorted_years = sorted(race_years.keys(), key=lambda y: int(y), reverse=True)
        race_rows = []
        for y in sorted_years:
            starters = race_years[y]
            winner = next((h for h in starters if h.get('rank') == 1), None)
            if not winner and starters:
                winner = starters[0]
            if winner:
                pop_val = winner.get('pop', 1)
                try:
                    pop_val = int(pop_val)
                except Exception:
                    pop_val = 1
                race_rows.append([
                    int(y),
                    winner.get('horseName', '-'),
                    winner.get('jockey', '-'),
                    winner.get('time', '-'),
                    pop_val,
                    winner.get('stable', '-')
                ])
        full_hist_summary[r_id] = race_rows
    else:
        full_hist_summary[r_id] = base_hist.get(r_id, [])

historical_data_str = "const HISTORICAL_DATA = " + json.dumps(full_hist_summary, ensure_ascii=False, indent=2) + ";"
entries_data_str = "const ENTRIES_DATA = " + json.dumps(entries_data, ensure_ascii=False, indent=2) + ";"
payouts_data_str = "const PAYOUTS_DATA = " + json.dumps(payouts_data, ensure_ascii=False, indent=2) + ";"
hist_full_str = "const HISTORICAL_FULL_RESULTS = " + json.dumps(hist_full_data, ensure_ascii=False, indent=2) + ";"
pred_data_str = "const PREDICTION_DATA = " + json.dumps(pred_data, ensure_ascii=False, indent=2) + ";"

# Add anti-flicker early route detector script in <head>
anti_flicker_script = """
    <!-- Anti-flicker route restoration -->
    <script>
      (function() {
        try {
          var h = window.location.hash || '';
          if (!h || h === '#' || h === '#/') {
            var saved = localStorage.getItem('keiba_active_route');
            if (saved && (saved.startsWith('#prediction') || saved.startsWith('#race-') || saved.startsWith('#sec-'))) {
              h = saved;
            }
          }
          if (h.startsWith('#prediction') || h.startsWith('#sec-')) {
            document.documentElement.classList.add('route-prediction');
          } else {
            document.documentElement.classList.add('route-calendar');
          }
        } catch (e) {}
      })();
    </script>
"""

with open(style_css_path, 'r', encoding='utf-8') as f:
    style_css_content = f.read()

new_base_html = re.sub(r'<style>[\s\S]*?</style>', f'<style>\n{style_css_content}\n    </style>', base_html)
new_base_html = new_base_html.replace('</head>', anti_flicker_script + '\n  </head>')

# Add navigation items for Prediction View
new_nav_menu = """<nav class="nav-menu">
          <a class="nav-item active" data-target="calendar" style="cursor: pointer;">
            <i data-lucide="calendar"></i>
            <span>G1カレンダー</span>
          </a>
          <a class="nav-item" data-target="prediction" style="cursor: pointer;">
            <i data-lucide="trending-up"></i>
            <span>予想・攻略分析</span>
          </a>
        </nav>"""
nav_match = re.search(r'<nav class="nav-menu">[\s\S]*?</nav>', new_base_html)
new_base_html = new_base_html[:nav_match.start()] + new_nav_menu + new_base_html[nav_match.end():]

# Update countdown hero section
new_hero_section = """<section class="countdown-section" id="hero-countdown-banner" style="cursor: pointer;">
          <div class="countdown-content">
            <div class="next-badge">
              <span class="pulse-dot"></span> NEXT G1 RACE (タップで予想へ)
            </div>
            <h2 class="race-title" id="next-race-name">第51回 エリザベス女王杯</h2>
            <p class="race-meta" id="next-race-meta">2026.11.15 (日) 京都 芝 2200m (G1)</p>
            <div style="margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap;">
              <button id="btn-hero-prediction" class="btn-hero-action" style="background: var(--gold); color: #111; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 800; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);">
                🎯 エリザベス女王杯 予想・攻略を見る
              </button>
              <button id="btn-hero-detail" class="btn-hero-action" style="background: rgba(255, 255, 255, 0.1); color: #fff; border: 1px solid var(--border-color); padding: 8px 14px; border-radius: 8px; font-weight: 700; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                📋 出馬表モーダル
              </button>
            </div>
          </div>
          <div class="countdown-timer">
            <div class="time-block">
              <div class="time-num" id="timer-days">--</div>
              <div class="time-label">DAYS</div>
            </div>
            <div class="time-block">
              <div class="time-num" id="timer-hours">--</div>
              <div class="time-label">HOURS</div>
            </div>
            <div class="time-block">
              <div class="time-num" id="timer-minutes">--</div>
              <div class="time-label">MINUTES</div>
            </div>
            <div class="time-block">
              <div class="time-num" id="timer-seconds">--</div>
              <div class="time-label">SECONDS</div>
            </div>
          </div>
        </section>"""
hero_match = re.search(r'<section class="countdown-section"[^>]*>[\s\S]*?</section>', new_base_html)
new_base_html = new_base_html[:hero_match.start()] + new_hero_section + new_base_html[hero_match.end():]

main_start = new_base_html.find('<main class="main-content">')
top_header_pos = new_base_html.find('<header class="top-header">', main_start)
race_grid_end = new_base_html.find('</section>', new_base_html.find('<section class="race-grid" id="race-grid-container">')) + len('</section>')

calendar_content = new_base_html[top_header_pos:race_grid_end]

# Prediction view HTML with Multiple Race Switcher
prediction_view_html = """
        <!-- 予想・攻略分析 専用ビュー -->
        <div id="view-prediction" class="app-view" style="display: none;">
          <!-- 対象レース切替スイッチャー (エリ女〜有馬記念＆結果レビュー) -->
          <div class="pred-race-switcher-container">
            <div class="pred-race-switcher-pills" id="pred-race-switcher-pills">
              <!-- JSで動的生成 -->
            </div>
          </div>

          <!-- 予想ページヘッダー -->
          <div class="pred-header-card">
            <div class="pred-breadcrumb">
              <a id="btn-back-to-calendar"><i data-lucide="arrow-left" style="width: 14px; height: 14px;"></i> ダッシュボードに戻る</a>
              <span>/</span>
              <span id="pred-header-subtitle">2026年 G1第17戦</span>
            </div>
            <h1 class="pred-title">
              <span id="pred-header-title">第51回 エリザベス女王杯</span>
              <span id="pred-header-badge" style="font-size: 11px; background: rgba(16, 185, 129, 0.2); color: var(--primary); padding: 2px 8px; border-radius: 4px; font-weight: 700; border: 1px solid rgba(16,185,129,0.3);">枠順確定済</span>
            </h1>
            <div class="pred-meta-chips" id="pred-meta-chips">
              <span class="pred-chip"><i data-lucide="calendar"></i> 11/15(日) 15:40発走</span>
              <span class="pred-chip"><i data-lucide="map-pin"></i> 京都芝2200m (外回り)</span>
              <span class="pred-chip"><i data-lucide="award"></i> 定量 / 全16頭</span>
            </div>
            <!-- 終了レースの場合のレビューポディウム表示コンテナ -->
            <div id="pred-finished-review-container"></div>
          </div>

          <!-- クイックジャンプナビ（親指ワンタップ） -->
          <div class="pred-quick-nav">
            <a href="#sec-starters" class="btn-quick-nav">
              <i data-lucide="list" style="width: 16px; height: 16px;"></i>
              <span>出馬表</span>
            </a>
            <a href="#sec-memo" class="btn-quick-nav">
              <i data-lucide="check-square" style="width: 16px; height: 16px; color: var(--gold);"></i>
              <span style="color: var(--gold);">予想印</span>
            </a>
            <a href="#sec-occult" class="btn-quick-nav">
              <i data-lucide="sparkles" style="width: 16px; height: 16px; color: #c084fc;"></i>
              <span style="color: #c084fc;">Xオカルト</span>
            </a>
            <a href="#sec-memo" class="btn-quick-nav">
              <i data-lucide="edit-3" style="width: 16px; height: 16px;"></i>
              <span>メモ帳</span>
            </a>
          </div>

          <!-- 1. 出走馬一覧＆オッズ管理（発売前:予想オッズ / 発売後:随時更新） -->
          <section id="sec-starters" style="margin-bottom: 20px;">
            <!-- オッズ状態＆切替コントロールバー -->
            <div class="odds-control-card">
              <div class="odds-status-row">
                <div class="odds-mode-badge pre-sale" id="odds-mode-badge">
                  <span class="pulse-dot-gold"></span>
                  <span id="odds-mode-text">想定予想オッズ (netkeiba参考)</span>
                </div>
                <div class="odds-sales-countdown" id="odds-sales-countdown">
                  ※金曜 18:30夜間発売開始とともに確定オッズへ自動切替
                </div>
              </div>

              <div class="odds-action-row">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <div class="odds-type-toggle">
                    <button id="btn-odds-estimated" class="btn-odds-mode active">予想オッズ</button>
                    <button id="btn-odds-live" class="btn-odds-mode">発売中 (最新)</button>
                  </div>
                  <div style="display: flex; gap: 2px;">
                    <button id="btn-sort-gate" class="btn-sort active" data-sort="gate" style="padding: 4px 8px; font-size: 11px;">馬番順</button>
                    <button id="btn-sort-pop" class="btn-sort" data-sort="pop" style="padding: 4px 8px; font-size: 11px;">人気順</button>
                  </div>
                </div>

                <div style="display: flex; align-items: center; gap: 6px;">
                  <span id="odds-update-time" style="font-size: 11px; color: var(--text-muted);">● リアルタイム</span>
                  <button id="btn-refresh-odds" class="btn-refresh-odds-btn">
                    <i data-lucide="rotate-cw" style="width: 13px; height: 13px;"></i>
                    <span>オッズ更新</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- スマホ最適化 リスト型出馬表（横スクロール完全不要） -->
            <div class="netkeiba-horse-table-wrapper">
              <!-- 固定ヘッダー行 -->
              <div class="nh-table-header">
                <div class="nh-col-gate">番</div>
                <div class="nh-col-mark">印</div>
                <div class="nh-col-info">馬名 / 騎手 / 斤量</div>
                <div class="nh-col-odds">オッズ</div>
                <div class="nh-col-weight">馬体重</div>
                <div class="nh-col-detail">詳細</div>
              </div>

              <!-- 馬リスト本体（JS動的描画） -->
              <div id="netkeiba-horse-list" class="nh-table-body">
                <!-- 動的レンダリング -->
              </div>
            </div>
          </section>

          <!-- 2. 印の集計サマリー ＆ 買い目メモ -->
          <section id="sec-memo" class="pred-card" style="margin-bottom: 20px;">
            <div class="pred-card-header">
              <h3 class="pred-card-title">
                <i data-lucide="check-square" style="color: var(--gold);"></i> 予想印サマリー ＆ 買い目メモ
              </h3>
            </div>
            
            <!-- 打った印のクイックサマリーバッジ -->
            <div id="user-marks-summary" class="user-marks-summary-bar">
              <div class="mark-summary-pill"><span class="mark-tag mark-honmei">◎</span> <span id="summary-mark-honmei" class="mark-horse-name">未選択</span></div>
              <div class="mark-summary-pill"><span class="mark-tag mark-taiko">○</span> <span id="summary-mark-taiko" class="mark-horse-name">未選択</span></div>
              <div class="mark-summary-pill"><span class="mark-tag mark-tanana">▲</span> <span id="summary-mark-tanana" class="mark-horse-name">未選択</span></div>
              <div class="mark-summary-pill"><span class="mark-tag mark-renka">△</span> <span id="summary-mark-renka" class="mark-horse-name">未選択</span></div>
              <div class="mark-summary-pill"><span class="mark-tag mark-ana">☆</span> <span id="summary-mark-ana" class="mark-horse-name">未選択</span></div>
            </div>

            <div style="margin-top: 14px;">
              <label style="font-size: 12px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px;">
                📝 予想メモ・購入予定馬券（自動保存）
              </label>
              <textarea id="prediction-user-memo" class="memo-textarea" placeholder="例: 3連複 軸相手手広く流し。Xオカルトサインと調教抜群馬の組み合わせを重視。" rows="3"></textarea>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                <span id="memo-save-status" style="font-size: 11px; color: var(--primary);"></span>
                <button id="btn-clear-memo" style="background: transparent; border: none; color: var(--text-muted); font-size: 11px; cursor: pointer;">
                  メモをクリア
                </button>
              </div>
            </div>
          </section>

          <!-- 3. X (Twitter) バズり・オカルトサイン考察 -->
          <section id="sec-occult" class="pred-card" style="margin-bottom: 20px;">
            <div class="pred-card-header">
              <h3 class="pred-card-title">
                <i data-lucide="sparkles" style="color: #c084fc;"></i> X (Twitter) 話題・オカルトサイン考察
              </h3>
              <span style="font-size: 11px; color: var(--text-muted); background: rgba(192, 132, 252, 0.1); border: 1px solid rgba(192, 132, 252, 0.3); padding: 2px 8px; border-radius: 12px;">リアルタイム分析</span>
            </div>
            <div id="occult-cards-list" class="occult-grid">
              <!-- JSで動的描画 -->
            </div>
          </section>

          <!-- 印選択ボトムシート（モーダル） -->
          <div id="mark-bottom-sheet" class="mark-bottom-sheet">
            <div class="mark-sheet-header">
              <div class="sheet-title">
                <span id="sheet-target-gate" class="nh-gate-cell">--</span>
                <span id="sheet-target-name" style="font-weight: 800; font-size: 15px; margin-left: 8px;">馬名</span>
              </div>
              <button id="btn-close-sheet" class="btn-sheet-close"><i data-lucide="x"></i></button>
            </div>
            <div class="mark-options-grid">
              <button class="btn-sheet-mark" data-mark="◎">
                <span class="mark-bubble mark-honmei">◎</span>
                <span class="mark-label">本命</span>
              </button>
              <button class="btn-sheet-mark" data-mark="○">
                <span class="mark-bubble mark-taiko">○</span>
                <span class="mark-label">対抗</span>
              </button>
              <button class="btn-sheet-mark" data-mark="▲">
                <span class="mark-bubble mark-tanana">▲</span>
                <span class="mark-label">単穴</span>
              </button>
              <button class="btn-sheet-mark" data-mark="△">
                <span class="mark-bubble mark-renka">△</span>
                <span class="mark-label">連下</span>
              </button>
              <button class="btn-sheet-mark" data-mark="☆">
                <span class="mark-bubble mark-ana">☆</span>
                <span class="mark-label">穴</span>
              </button>
              <button class="btn-sheet-mark" data-mark="消">
                <span class="mark-bubble mark-keshi">消</span>
                <span class="mark-label">消し</span>
              </button>
              <button class="btn-sheet-mark clear" data-mark="未">
                <span class="mark-bubble mark-clear">✕</span>
                <span class="mark-label">取消</span>
              </button>
            </div>
          </div>
          <div id="mark-sheet-backdrop" class="mark-sheet-backdrop"></div>
        </div>
"""

new_main_content = (
    new_base_html[:top_header_pos]
    + '<div id="view-calendar" class="app-view">\n'
    + calendar_content
    + '\n        </div>\n'
    + prediction_view_html
    + new_base_html[race_grid_end:]
)

# Strip out old script (use rfind to get the main script at the bottom of the body, not the scripts in <head>)
script_start = new_main_content.rfind('<script>')
new_main_content = new_main_content[:script_start + len('<script>\n')]

# Extract helpers from base_html
pools_idx = base_html.find('const POOLS = {')
payouts_idx = base_html.find('const PAYOUTS_DATA = {')
hydrate_payouts_idx = base_html.find('function hydratePayouts(race) {')
open_detail_idx = base_html.find('function openRaceDetail(id) {')

existing_helpers = (
    base_html[pools_idx:payouts_idx]
    + "\n\n"
    + base_html[hydrate_payouts_idx:open_detail_idx]
)

# Update renderRaces in existing_helpers to include 枠順確定 / 出走馬公開 badge
existing_helpers = re.sub(
    r'let footerContent = \'\';[\s\S]*?container\.appendChild\(card\);',
    """let footerContent = '';
          const hasEntries = typeof ENTRIES_DATA !== 'undefined' && ENTRIES_DATA[r.id];

          if (r.status === 'finished') {
            footerContent = `
              <div class="card-result-preview">
                <div class="winner-row">
                  <svg class="winner-crown" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M2 4l3 5 7-6 7 6 3-5v14c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V4zm2 5.5l1.6-2.7 2.1 3.5 4.3-3.7 4.3 3.7 2.1-3.5L20 9.5V18H4V9.5z"/></svg>
                  <span class="winner-name">${r.winner}</span>
                  <span class="text-muted">(${r.winnerJockey})</span>
                </div>
                <div class="card-action-text">結果詳細を見る <i data-lucide="arrow-right"></i></div>
              </div>
            `;
          } else {
            const badgeText = (r.id === '17') ? '枠順確定' : (hasEntries ? '出走馬・オカルト' : '');
            footerContent = `
              <div class="card-result-preview">
                <span class="text-muted" style="font-size: 13px;">${badgeText ? `<span style="background: rgba(16,185,129,0.2); color: var(--primary); padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px; margin-right: 6px;">${badgeText}</span>` : ''}発走予定: 15:40</span>
                <div class="card-action-text">出馬表・詳細 <i data-lucide="arrow-right"></i></div>
              </div>
            `;
          }

          card.innerHTML = `
            <div class="card-header-row">
              <span class="race-date-badge">${dateStr} (${weekdayStr})</span>
              <span class="race-status-badge ${r.status}">
                ${r.status === 'finished' ? '開催済' : '今後の予定'}
              </span>
            </div>
            <h3>${r.name}</h3>
            <div class="race-meta-info">
              <span>${r.location}競馬場</span>
              <span>|</span>
              <span>${r.course}</span>
            </div>
            <div class="race-card-footer">
              ${footerContent}
            </div>
          `;

          container.appendChild(card);""",
    existing_helpers
)

# Remove old DOMContentLoaded from existing_helpers
existing_helpers = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\'[\s\S]*?\}\);', '', existing_helpers)

# Complete Prediction JS Logic with Routing, LifeCycle, and Multi-race Switcher
prediction_js_logic = """
      // ----------------------------------------------------
      // SPA Hash ルーティング ＆ ナビゲーション
      // ----------------------------------------------------
      let currentAppView = 'calendar';
      let lastMainView = 'calendar';
      let predictionSortType = 'gate';
      let activeSheetGate = null;
      let currentPredictionRaceId = '17'; // デフォルトは次走エリ女

      let oddsMode = 'estimated'; // 'estimated' または 'live'
      let oddsAutoRefreshTimer = null;
      let lastOddsRefreshTime = null;
      let liveOddsData = null;

      const MARK_CLASSES = {
        '◎': 'mark-honmei',
        '○': 'mark-taiko',
        '▲': 'mark-tanana',
        '△': 'mark-renka',
        '☆': 'mark-ana',
        '消': 'mark-keshi'
      };

      function refreshIcons() {
        if (typeof window !== 'undefined' && window.lucide && typeof window.lucide.createIcons === 'function') {
          window.lucide.createIcons();
        }
      }

      function navigateTo(routeHash) {
        if (typeof window === 'undefined') return;
        if (window.location.hash !== routeHash) {
          window.location.hash = routeHash;
        } else {
          handleRoute(false);
        }
      }

      function handleRoute(shouldScroll = false) {
        if (typeof window === 'undefined') return;

        let hash = window.location.hash || '';
        if (!hash || hash === '#' || hash === '#/') {
          if (typeof localStorage !== 'undefined') {
            const saved = localStorage.getItem('keiba_active_route');
            if (saved && (saved.startsWith('#prediction') || saved.startsWith('#race-') || saved.startsWith('#sec-'))) {
              hash = saved;
              if (window.history && window.history.replaceState) {
                window.history.replaceState(null, '', hash);
              }
            } else {
              hash = '#calendar';
            }
          } else {
            hash = '#calendar';
          }
        }

        // 1. レース詳細モーダル ルート (#race-16, #race-17 など)
        if (hash.startsWith('#race-')) {
          const raceId = hash.replace('#race-', '');
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('keiba_active_route', hash);
          }
          const baseView = (typeof localStorage !== 'undefined' && localStorage.getItem('keiba_last_main_view') === 'prediction') ? 'prediction' : 'calendar';
          switchView(baseView, false, false);
          openRaceDetail(raceId, false);
          return;
        }

        // 2. 予想ページ ルート (#prediction または #prediction-17 など)
        if (hash.startsWith('#prediction') || hash.startsWith('#sec-')) {
          closeModal();
          if (hash.startsWith('#prediction-')) {
            const targetId = hash.replace('#prediction-', '');
            if (typeof PREDICTION_DATA !== 'undefined' && PREDICTION_DATA.races && PREDICTION_DATA.races[targetId]) {
              currentPredictionRaceId = targetId;
            }
          }
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('keiba_active_route', hash.startsWith('#prediction') ? hash : '#prediction');
            localStorage.setItem('keiba_last_main_view', 'prediction');
          }
          switchView('prediction', shouldScroll, false);

          if (hash.startsWith('#sec-')) {
            const secId = hash.replace('#', '');
            const targetEl = document.getElementById(secId);
            if (targetEl) {
              setTimeout(() => {
                targetEl.scrollIntoView({ behavior: 'smooth' });
              }, 80);
            }
          }
          return;
        }

        // 3. カレンダー一覧 トップページ ルート (#calendar またはデフォルト)
        closeModal();
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('keiba_active_route', '#calendar');
          localStorage.setItem('keiba_last_main_view', 'calendar');
        }
        switchView('calendar', shouldScroll, false);
      }

      function switchView(viewName, shouldScroll = true, updateRoute = false) {
        if (updateRoute) {
          navigateTo('#' + viewName);
          return;
        }

        currentAppView = viewName;
        lastMainView = viewName;
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('keiba_last_main_view', viewName);
          localStorage.setItem('keiba_active_route', '#' + viewName);
        }

        const calView = document.getElementById('view-calendar');
        const predView = document.getElementById('view-prediction');
        const navItems = document.querySelectorAll('.nav-item');

        if (viewName === 'prediction') {
          if (document.documentElement) {
            document.documentElement.classList.add('route-prediction');
            document.documentElement.classList.remove('route-calendar');
          }
          if (calView) calView.style.display = 'none';
          if (predView) predView.style.display = 'block';
          navItems.forEach(n => {
            if (n.getAttribute('data-target') === 'prediction') n.classList.add('active');
            else n.classList.remove('active');
          });
          renderPredictionView();
          if (shouldScroll && typeof window !== 'undefined' && window.scrollTo) {
            window.scrollTo({ top: 0, behavior: 'instant' });
          }
        } else {
          if (document.documentElement) {
            document.documentElement.classList.remove('route-prediction');
            document.documentElement.classList.add('route-calendar');
          }
          if (predView) predView.style.display = 'none';
          if (calView) calView.style.display = 'block';
          navItems.forEach(n => {
            if (n.getAttribute('data-target') === 'calendar') n.classList.add('active');
            else n.classList.remove('active');
          });
          if (shouldScroll && typeof window !== 'undefined' && window.scrollTo) {
            window.scrollTo({ top: 0, behavior: 'instant' });
          }
        }
      }

      function closeModal() {
        const modal = document.getElementById('modal-race-detail');
        if (modal) {
          modal.classList.remove('open');
          modal.classList.remove('active');
        }
        document.body.style.overflow = '';
        if (typeof window !== 'undefined') {
          const baseRoute = (currentAppView === 'prediction') ? ('#prediction-' + currentPredictionRaceId) : '#calendar';
          if (window.location.hash.startsWith('#race-')) {
            if (window.history && window.history.replaceState) {
              window.history.replaceState(null, '', baseRoute);
            } else {
              window.location.hash = baseRoute;
            }
            if (typeof localStorage !== 'undefined') {
              localStorage.setItem('keiba_active_route', baseRoute);
            }
          }
        }
      }

      // 次回G1レースを自動判定（現在時刻から最も近い未終了レース）
      function getNextUpcomingRace() {
        const now = new Date();
        const upcoming = G1_RACES.filter(r => new Date(r.date) > now)
                                 .sort((a, b) => new Date(a.date) - new Date(b.date));
        return upcoming.length > 0 ? upcoming[0] : G1_RACES[G1_RACES.length - 1];
      }

      // 全自動ライフサイクル管理エンジン
      function autoLifecycleEngine() {
        const now = new Date();
        let changed = false;
        G1_RACES.forEach(r => {
          if (new Date(r.date) <= now && r.status !== 'finished') {
            r.status = 'finished';
            changed = true;
          }
        });
        if (changed) {
          renderRaces();
          updateTabCounts();
        }
        startNextRaceCountdown();
      }

      function isJraTicketSalesStarted(raceDateStr) {
        const now = new Date();
        if (!raceDateStr) return false;
        const raceDate = new Date(raceDateStr);
        const dayOfWeek = raceDate.getDay();
        const daysToFriday = (dayOfWeek === 0) ? 2 : (dayOfWeek === 6 ? 1 : 2);
        const salesStart = new Date(raceDate.getTime() - daysToFriday * 24 * 60 * 60 * 1000);
        salesStart.setHours(18, 30, 0, 0);
        return now >= salesStart;
      }

      function getTicketSalesStartTime(raceDateStr) {
        if (!raceDateStr) return '金曜 18:30';
        const raceDate = new Date(raceDateStr);
        const dayOfWeek = raceDate.getDay();
        const daysToFriday = (dayOfWeek === 0) ? 2 : (dayOfWeek === 6 ? 1 : 2);
        const salesStart = new Date(raceDate.getTime() - daysToFriday * 24 * 60 * 60 * 1000);
        salesStart.setHours(18, 30, 0, 0);
        const m = salesStart.getMonth() + 1;
        const d = salesStart.getDate();
        return `${m}/${d}(金) 18:30`;
      }

      function getActivePredictionStarters() {
        if (typeof PREDICTION_DATA !== 'undefined') {
          if (PREDICTION_DATA.races && PREDICTION_DATA.races[currentPredictionRaceId]) {
            return PREDICTION_DATA.races[currentPredictionRaceId].starters || [];
          }
          if (PREDICTION_DATA.starters) {
            return PREDICTION_DATA.starters;
          }
        }
        return [];
      }

      function initOddsState() {
        const raceObj = G1_RACES.find(r => r.id === currentPredictionRaceId);
        const isFinished = raceObj && raceObj.status === 'finished';

        if (isFinished) {
          oddsMode = 'live';
        } else if (typeof localStorage !== 'undefined') {
          const savedMode = localStorage.getItem('keiba_odds_mode_' + currentPredictionRaceId);
          if (savedMode === 'live' || savedMode === 'estimated') {
            oddsMode = savedMode;
          } else {
            oddsMode = isJraTicketSalesStarted(raceObj ? raceObj.date : null) ? 'live' : 'estimated';
          }
        } else {
          oddsMode = isJraTicketSalesStarted(raceObj ? raceObj.date : null) ? 'live' : 'estimated';
        }

        liveOddsData = null;
        if (typeof localStorage !== 'undefined') {
          try {
            const savedLive = localStorage.getItem('keiba_live_odds_' + currentPredictionRaceId);
            if (savedLive) liveOddsData = JSON.parse(savedLive);
          } catch(e) {}
        }

        if (!liveOddsData) {
          generateInitialLiveOdds();
        }
      }

      function generateInitialLiveOdds() {
        liveOddsData = {};
        const starters = getActivePredictionStarters();
        starters.forEach(s => {
          const baseWin = parseFloat(s.odds) || 10.0;
          liveOddsData[s.gate] = {
            win: baseWin,
            place: s.placeOdds || `${(baseWin * 0.35).toFixed(1)} - ${(baseWin * 0.55).toFixed(1)}`,
            pop: s.pop || 99
          };
        });
      }

      function refreshLiveOdds(simulateShift = true) {
        if (!liveOddsData || Object.keys(liveOddsData).length === 0) generateInitialLiveOdds();

        if (simulateShift) {
          const gates = Object.keys(liveOddsData);
          gates.forEach(g => {
            const currentWin = liveOddsData[g].win;
            let delta = 0;
            if (currentWin < 4.0) {
              delta = (Math.floor(Math.random() * 5) - 2) * 0.1;
            } else if (currentWin < 15.0) {
              delta = (Math.floor(Math.random() * 7) - 3) * 0.2;
            } else if (currentWin < 50.0) {
              delta = (Math.floor(Math.random() * 7) - 3) * 0.5;
            } else {
              delta = (Math.floor(Math.random() * 5) - 2) * 1.5;
            }
            let newWin = Math.max(1.1, +(currentWin + delta).toFixed(1));
            liveOddsData[g].win = newWin;
            
            const pMin = Math.max(1.1, +(newWin * 0.32).toFixed(1));
            const pMax = Math.max(pMin + 0.2, +(newWin * 0.52).toFixed(1));
            liveOddsData[g].place = `${pMin.toFixed(1)} - ${pMax.toFixed(1)}`;
          });

          // 単勝オッズ順に人気を自動再計算
          const sorted = gates.map(g => ({ gate: g, win: liveOddsData[g].win }))
                              .sort((a, b) => a.win - b.win);
          sorted.forEach((item, idx) => {
            liveOddsData[item.gate].pop = idx + 1;
          });

          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('keiba_live_odds_' + currentPredictionRaceId, JSON.stringify(liveOddsData));
          }
        }

        const now = new Date();
        lastOddsRefreshTime = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;
        renderNetkeibaHorseList();
        updateOddsControlUI();
        triggerOddsHighlight();
      }

      function setOddsMode(mode) {
        oddsMode = mode;
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('keiba_odds_mode_' + currentPredictionRaceId, mode);
        }
        if (mode === 'live' && (!liveOddsData || Object.keys(liveOddsData).length === 0)) {
          generateInitialLiveOdds();
        }
        renderNetkeibaHorseList();
        updateOddsControlUI();
      }

      function updateOddsControlUI() {
        if (typeof document === 'undefined') return;
        const btnEstimated = document.getElementById('btn-odds-estimated');
        const btnLive = document.getElementById('btn-odds-live');
        const badge = document.getElementById('odds-mode-badge');
        const badgeText = document.getElementById('odds-mode-text');
        const countdown = document.getElementById('odds-sales-countdown');
        const timeEl = document.getElementById('odds-update-time');
        const oddsCard = document.querySelector('.odds-control-card');

        const raceObj = G1_RACES.find(r => r.id === currentPredictionRaceId);
        const isFinished = raceObj && raceObj.status === 'finished';

        if (isFinished) {
          if (oddsCard) oddsCard.style.display = 'none';
          return;
        } else {
          if (oddsCard) oddsCard.style.display = 'block';
        }

        if (btnEstimated && btnLive) {
          if (oddsMode === 'estimated') {
            btnEstimated.classList.add('active');
            btnLive.classList.remove('active');
          } else {
            btnEstimated.classList.remove('active');
            btnLive.classList.add('active');
          }
        }

        const salesTimeStr = getTicketSalesStartTime(raceObj ? raceObj.date : null);

        if (badge && badgeText) {
          if (oddsMode === 'estimated') {
            badge.className = 'odds-mode-badge pre-sale';
            badgeText.innerText = '想定予想オッズ (netkeiba参考)';
            if (countdown) {
              countdown.innerText = `※${salesTimeStr}夜間発売開始とともに確定オッズへ自動切替`;
            }
          } else {
            badge.className = 'odds-mode-badge live-sale';
            badgeText.innerText = '● 発売中・リアルタイムオッズ (30秒自動更新)';
            if (countdown) {
              countdown.innerText = '※JRA公式発売オッズ連動シミュレーション中';
            }
          }
        }

        if (timeEl) {
          if (lastOddsRefreshTime) {
            timeEl.innerText = `● ${lastOddsRefreshTime} 自動更新済`;
          } else {
            timeEl.innerText = '● リアルタイム';
          }
        }
      }

      function startOddsAutoRefresh() {
        if (oddsAutoRefreshTimer) clearInterval(oddsAutoRefreshTimer);
        oddsAutoRefreshTimer = setInterval(() => {
          const currentView = document.querySelector('.app-view:not([style*="display: none"])');
          if (currentView && currentView.id === 'view-prediction') {
            const raceObj = G1_RACES.find(r => r.id === currentPredictionRaceId);
            if (raceObj && raceObj.status !== 'finished') {
              if (oddsMode === 'live') {
                refreshLiveOdds(true);
              } else {
                if (isJraTicketSalesStarted(raceObj.date)) {
                  setOddsMode('live');
                }
              }
            }
          }
        }, 30000);
      }

      function triggerOddsHighlight() {
        const oddsCells = document.querySelectorAll('.nh-odds-val');
        oddsCells.forEach(c => {
          c.style.transition = 'color 0.3s ease, transform 0.3s ease';
          c.style.color = 'var(--gold)';
          c.style.transform = 'scale(1.08)';
          setTimeout(() => {
            c.style.color = '';
            c.style.transform = '';
          }, 800);
        });
      }

      function initWeightState() {}
      function updateWeightControlUI() {}

      function getUserMarks() {
        if (typeof localStorage === 'undefined') return {};
        try {
          return JSON.parse(localStorage.getItem('keiba_marks_' + currentPredictionRaceId)) || {};
        } catch(e) {
          return {};
        }
      }

      function setUserMark(gate, mark) {
        const marks = getUserMarks();
        if (mark === '未' || !mark) {
          delete marks[gate];
        } else {
          marks[gate] = mark;
        }
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('keiba_marks_' + currentPredictionRaceId, JSON.stringify(marks));
        }
        updateMarksUI();
      }

      function updateMarksUI() {
        const marks = getUserMarks();
        const starters = getActivePredictionStarters();

        document.querySelectorAll('.nh-mark-btn').forEach(btn => {
          const g = btn.getAttribute('data-gate');
          const m = marks[g] || '';
          btn.innerText = m;
          btn.className = `nh-mark-btn ${MARK_CLASSES[m] || ''}`;
        });

        const markTypes = [
          { mark: '◎', id: 'summary-mark-honmei' },
          { mark: '○', id: 'summary-mark-taiko' },
          { mark: '▲', id: 'summary-mark-tanana' },
          { mark: '△', id: 'summary-mark-renka' },
          { mark: '☆', id: 'summary-mark-ana' }
        ];

        markTypes.forEach(mt => {
          const el = document.getElementById(mt.id);
          if (!el) return;
          const assignedGates = Object.keys(marks).filter(g => marks[g] === mt.mark);
          if (assignedGates.length > 0) {
            const horseNames = assignedGates.map(g => {
              const h = starters.find(s => s.gate === Number(g));
              return h ? `${g}.${h.horseName}` : `${g}番`;
            });
            el.innerText = horseNames.join(', ');
            el.classList.add('has-assigned');
          } else {
            el.innerText = '未選択';
            el.classList.remove('has-assigned');
          }
        });
      }

      function openMarkSheet(gate) {
        activeSheetGate = gate;
        const starters = getActivePredictionStarters();
        const horse = starters.find(s => s.gate === Number(gate));
        if (!horse) return;

        const sheet = document.getElementById('mark-bottom-sheet');
        const backdrop = document.getElementById('mark-sheet-backdrop');
        const gateBadge = document.getElementById('sheet-target-gate');
        const nameEl = document.getElementById('sheet-target-name');

        if (gateBadge) {
          gateBadge.className = `nh-gate-cell waku-${horse.waku}`;
          gateBadge.innerText = horse.gate;
        }
        if (nameEl) {
          nameEl.innerText = `${horse.horseName} (${horse.jockey})`;
        }

        const currentMark = getUserMarks()[gate] || '';
        document.querySelectorAll('.btn-sheet-mark').forEach(btn => {
          if (btn.getAttribute('data-mark') === currentMark) {
            btn.classList.add('selected');
          } else {
            btn.classList.remove('selected');
          }
        });

        if (sheet && backdrop) {
          sheet.classList.add('open', 'active');
          backdrop.classList.add('open', 'active');
        }
      }

      function closeMarkSheet() {
        const sheet = document.getElementById('mark-bottom-sheet');
        const backdrop = document.getElementById('mark-sheet-backdrop');
        if (sheet && backdrop) {
          sheet.classList.remove('open', 'active');
          backdrop.classList.remove('open', 'active');
        }
        activeSheetGate = null;
      }

      // レース切替タブの描画（エリ女以降の全G1レースに対応）
      function renderPredictionRaceSwitcher() {
        const container = document.getElementById('pred-race-switcher-pills');
        if (!container) return;
        
        const targetRaces = [
          { id: '17', label: '👑 エリザベス女王杯 (11/15)', badge: '次回', isNext: true },
          { id: '18', label: '⚡ マイルCS (11/22)', badge: '次走', isNext: true },
          { id: '19', label: '🇯🇵 ジャパンC (11/29)', badge: '世界決戦', isNext: true },
          { id: '20', label: '🏜️ チャンピオンズC (12/6)', badge: 'ダート頂上', isNext: true },
          { id: '21', label: '🌸 阪神JF (12/13)', badge: '2歳女王', isNext: true },
          { id: '22', label: '🏇 朝日杯FS (12/20)', badge: '2歳牡馬', isNext: true },
          { id: '23', label: '⭐ ホープフルS (12/26)', badge: '登竜門', isNext: true },
          { id: '24', label: '💎 有馬記念 (12/27)', badge: 'グランプリ', isNext: true },
          { id: '16', label: '📜 天皇賞（秋）', badge: '結果レビュー', isNext: false }
        ];
        
        container.innerHTML = targetRaces.map(r => {
          const isActive = r.id === currentPredictionRaceId;
          const badgeClass = r.isNext ? 'pill-badge' : 'pill-badge review';
          return `
            <button class="pred-race-pill ${isActive ? 'active' : ''}" data-race-id="${r.id}">
              <span class="${badgeClass}">${r.badge}</span>
              <span class="pill-name">${r.label}</span>
            </button>
          `;
        }).join('');
        
        container.querySelectorAll('.pred-race-pill').forEach(btn => {
          btn.addEventListener('click', () => {
            const rid = btn.getAttribute('data-race-id');
            if (rid && rid !== currentPredictionRaceId) {
              setPredictionRace(rid);
            }
          });
        });
      }

      function renderPredictionHeader() {
        const titleEl = document.getElementById('pred-header-title');
        const badgeEl = document.getElementById('pred-header-badge');
        const subtitleEl = document.getElementById('pred-header-subtitle');
        const chipsEl = document.getElementById('pred-meta-chips');
        const reviewContainer = document.getElementById('pred-finished-review-container');
        
        const raceObj = G1_RACES.find(r => r.id === currentPredictionRaceId);
        const currentPred = (PREDICTION_DATA.races && PREDICTION_DATA.races[currentPredictionRaceId]) 
          ? PREDICTION_DATA.races[currentPredictionRaceId] 
          : PREDICTION_DATA;
          
        if (subtitleEl) subtitleEl.innerText = `2026年 G1第${currentPredictionRaceId}戦`;
        if (titleEl) titleEl.innerText = currentPred.raceName || (raceObj ? raceObj.name : '');
        
        const isFinished = raceObj && raceObj.status === 'finished';
        if (badgeEl) {
          if (isFinished) {
            badgeEl.innerText = '公式結果確定';
            badgeEl.style.background = 'rgba(245, 158, 11, 0.2)';
            badgeEl.style.color = 'var(--gold)';
            badgeEl.style.borderColor = 'rgba(245, 158, 11, 0.4)';
          } else if (currentPredictionRaceId === '17') {
            badgeEl.innerText = '枠順確定済 / 予想公開中';
            badgeEl.style.background = 'rgba(16, 185, 129, 0.2)';
            badgeEl.style.color = 'var(--primary)';
            badgeEl.style.borderColor = 'rgba(16, 185, 129, 0.4)';
          } else {
            badgeEl.innerText = '出走登録馬・特別先行予想';
            badgeEl.style.background = 'rgba(147, 51, 234, 0.2)';
            badgeEl.style.color = '#c084fc';
            badgeEl.style.borderColor = 'rgba(147, 51, 234, 0.4)';
          }
        }
        
        const startersCount = currentPred.starters ? currentPred.starters.length : 16;
        const dateStr = currentPred.date ? currentPred.date.replace('2026年', '').trim() : (raceObj ? raceObj.date : '');
        const courseStr = raceObj ? `${raceObj.location} ${raceObj.course}` : '芝';
        
        if (chipsEl) {
          chipsEl.innerHTML = `
            <span class="pred-chip"><i data-lucide="calendar"></i> ${dateStr}</span>
            <span class="pred-chip"><i data-lucide="map-pin"></i> ${courseStr}</span>
            <span class="pred-chip"><i data-lucide="award"></i> 全${startersCount}頭</span>
          `;
        }
        
        if (reviewContainer) {
          if (isFinished && raceObj && raceObj.winner) {
            reviewContainer.innerHTML = `
              <div class="finished-review-card">
                <div class="review-header">
                  <div class="review-title">
                    <span>🏆 第174回 天皇賞（秋） 公式レース結果確定</span>
                  </div>
                  <button class="btn-open-result-modal" id="btn-review-modal-trigger" data-race-id="${currentPredictionRaceId}">
                    全17頭の着順・払戻金を見る <i data-lucide="arrow-right" style="width:13px;height:13px;"></i>
                  </button>
                </div>
                <div class="review-podium">
                  <div class="podium-item first">
                    <span class="podium-rank">1着</span>
                    <span class="podium-gate">${raceObj.winnerGate || 17}</span>
                    <span class="podium-name">${raceObj.winner}</span>
                    <div class="podium-sub">${raceObj.winnerJockey} / ${raceObj.time || '1:56.7'} (4人気)</div>
                  </div>
                  <div class="podium-item second">
                    <span class="podium-rank">2着</span>
                    <span class="podium-gate">${raceObj.secondGate || 10}</span>
                    <span class="podium-name">${raceObj.second || 'ネブラディスク'}</span>
                    <div class="podium-sub">${raceObj.secondJockey || '川田将雅'} (8人気)</div>
                  </div>
                  <div class="podium-item third">
                    <span class="podium-rank">3着</span>
                    <span class="podium-gate">${raceObj.thirdGate || 3}</span>
                    <span class="podium-name">${raceObj.third || 'レガレイラ'}</span>
                    <div class="podium-sub">${raceObj.thirdJockey || '岩田望来'} (3人気)</div>
                  </div>
                </div>
                <div class="review-payout-ribbon">
                  <span>単勝: <b>¥1,080</b></span>
                  <span>馬連: <b>¥12,970</b></span>
                  <span>3連複: <b>¥42,010</b></span>
                  <span class="highlight-trifecta">3連単: <b>¥297,820</b></span>
                </div>
              </div>
            `;
            const btnModal = document.getElementById('btn-review-modal-trigger');
            if (btnModal) {
              btnModal.addEventListener('click', () => {
                openRaceDetail(currentPredictionRaceId);
              });
            }
          } else {
            reviewContainer.innerHTML = '';
          }
        }
      }

      function setPredictionRace(raceId) {
        if (!PREDICTION_DATA.races || !PREDICTION_DATA.races[raceId]) return;
        currentPredictionRaceId = raceId;
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('keiba_pred_race_id', raceId);
        }
        
        initOddsState();
        initWeightState();
        renderPredictionRaceSwitcher();
        renderPredictionHeader();
        renderNetkeibaHorseList();
        renderPredictionOccult();
        renderPredictionMemo();
        updateMarksUI();
        updateOddsControlUI();
        updateWeightControlUI();
        refreshIcons();

        if (window.history && window.history.replaceState) {
          window.history.replaceState({ view: 'prediction', raceId: currentPredictionRaceId }, '', '#prediction-' + currentPredictionRaceId);
        }
      }

      function renderPredictionView() {
        if (typeof document === 'undefined') return;
        const container = document.getElementById('view-prediction');
        if (!container) return;

        if (!currentPredictionRaceId || !PREDICTION_DATA.races || !PREDICTION_DATA.races[currentPredictionRaceId]) {
          const nextRace = getNextUpcomingRace();
          currentPredictionRaceId = (nextRace && PREDICTION_DATA.races && PREDICTION_DATA.races[nextRace.id]) ? nextRace.id : '17';
        }

        initOddsState();
        initWeightState();
        renderPredictionRaceSwitcher();
        renderPredictionHeader();
        renderNetkeibaHorseList();
        renderPredictionOccult();
        renderPredictionMemo();
        updateMarksUI();
        updateOddsControlUI();
        updateWeightControlUI();
        refreshIcons();
      }

      // NetKeiba完全準拠 リストレンダラー
      // ユーザー指定の厳格な順序: [馬番] [印] [馬情報] ➔ [オッズ] ➔ [馬体重] ➔ [詳細▼]
      function renderNetkeibaHorseList() {
        if (typeof document === 'undefined') return;
        const listContainer = document.getElementById('netkeiba-horse-list');
        if (!listContainer) return;

        const currentPred = (PREDICTION_DATA.races && PREDICTION_DATA.races[currentPredictionRaceId])
          ? PREDICTION_DATA.races[currentPredictionRaceId]
          : PREDICTION_DATA;
        const rawStarters = getActivePredictionStarters();

        const raceObj = G1_RACES.find(r => r.id === currentPredictionRaceId);
        const venueText = raceObj ? `${raceObj.location}芝・ダート適性` : 'コース適性';

        let starters = rawStarters.map(s => {
          let winVal = s.odds || '--';
          let placeVal = s.placeOdds || '-';
          let popVal = s.pop || 99;

          if (oddsMode === 'live' && liveOddsData && liveOddsData[s.gate]) {
            winVal = liveOddsData[s.gate].win.toFixed(1);
            placeVal = liveOddsData[s.gate].place;
            popVal = liveOddsData[s.gate].pop;
          }

          let jockeyDisplay = `${s.jockey} / ${venueText}`;
          if (currentPred.jockeysCompatibility) {
            const jc = currentPred.jockeysCompatibility.find(j => j.horse === s.horseName || j.jockey === s.jockey);
            if (jc) {
              jockeyDisplay = `${jc.rating} (${jc.switchType})`;
            }
          }

          let rawComment = (s.trainingComment || s.comment || '').trim();
          let hasRealComment = rawComment && rawComment !== '-' && rawComment !== 'null' && rawComment !== 'undefined';
          let commentDisplay = hasRealComment ? rawComment : '-';

          return {
            ...s,
            winOdds: winVal,
            placeOdds: placeVal,
            pop: popVal,
            comment: commentDisplay,
            jockeyStat: jockeyDisplay
          };
        });

        if (predictionSortType === 'pop') {
          starters.sort((a, b) => a.pop - b.pop);
        } else {
          starters.sort((a, b) => a.gate - b.gate);
        }

        const marks = getUserMarks();
        let html = '';

        starters.forEach(s => {
          const m = marks[s.gate] || '';
          const mClass = MARK_CLASSES[m] || '';
          const isTop3Pop = s.pop <= 3;
          const displayOdds = s.winOdds || s.odds || '--';

          let displayWeight = '-';
          let displayWeightSub = `<span class="weight-tag-prev">前走</span>`;

          if (s.confirmedWeight) {
            displayWeight = `${s.confirmedWeight}kg`;
            const diff = s.weightDiff || '0';
            let diffClass = 'diff-zero';
            let diffText = (diff === '0' || diff === '+0' || diff === '-0') ? '±0' : diff;
            if (diff.startsWith('+') && diff !== '+0') diffClass = 'diff-plus';
            else if (diff.startsWith('-') && diff !== '-0') diffClass = 'diff-minus';
            displayWeightSub = `<span class="weight-tag-diff ${diffClass}">${diffText}</span>`;
          } else if (s.lastRaceWeight || s.prevWeight) {
            const pw = s.lastRaceWeight || s.prevWeight;
            displayWeight = `${pw}kg`;
            displayWeightSub = `<span class="weight-tag-prev">前走</span>`;
          } else if (s.trainingWeight) {
            displayWeight = `${s.trainingWeight}kg`;
            displayWeightSub = `<span class="weight-tag-pre">調教後</span>`;
          } else {
            displayWeight = '-';
            displayWeightSub = `<span style="font-size:10px;color:var(--text-muted);">-</span>`;
          }

          html += `
            <div class="nh-row-container">
              <div class="nh-main-row" data-gate="${s.gate}">
                <!-- 1. 馬番（26px 枠色セル） -->
                <div class="nh-gate-cell waku-${s.waku}">
                  ${s.gate}
                </div>

                <!-- 2. 印ボタン (30px) -->
                <div class="nh-mark-cell">
                  <button class="nh-mark-btn ${mClass}" data-gate="${s.gate}" aria-label="印選択">
                    ${m}
                  </button>
                </div>

                <!-- 3. 馬情報（中央・可変幅・重なりなし） -->
                <div class="nh-info-cell" data-action="toggle-drawer" data-gate="${s.gate}">
                  <div class="nh-name-row">
                    <span class="nh-horse-name">${s.horseName}</span>
                  </div>
                  <div class="nh-sub-row">
                    <span>${s.sexAge}</span>
                    <span class="nh-jockey">${s.jockey}</span>
                    <span class="nh-load">${s.load}kg</span>
                  </div>
                </div>

                <!-- 4. オッズ・人気（48px固定・右寄せ） -->
                <div class="nh-odds-cell" data-action="toggle-drawer" data-gate="${s.gate}">
                  <div class="nh-odds-line">
                    ${oddsMode === 'estimated' ? '<span class="nh-odds-badge-yosou">予</span>' : ''}
                    <span class="nh-odds-val ${isTop3Pop ? 'highlight-fav' : ''}">${displayOdds}</span>
                  </div>
                  <div class="nh-pop-badge">${s.pop}人気</div>
                </div>

                <!-- 5. 馬体重（52px固定・右寄せ） -->
                <div class="nh-weight-cell" data-action="toggle-drawer" data-gate="${s.gate}">
                  <div class="nh-weight-val">${displayWeight}</div>
                  <div class="nh-weight-sub">${displayWeightSub}</div>
                </div>

                <!-- 6. 詳細▼ボタン (34px固定) -->
                <div class="nh-detail-toggle-cell" data-action="toggle-drawer" data-gate="${s.gate}">
                  <button class="nh-drawer-toggle-btn" id="nh-toggle-btn-${s.gate}" aria-label="詳細展開">
                    <span class="toggle-text" id="nh-toggle-text-${s.gate}">詳細</span>
                    <span class="toggle-arrow" id="nh-arrow-${s.gate}">▾</span>
                  </button>
                </div>
              </div>

              <!-- タップで展開されるアコーディオン詳細 -->
              <div class="nh-detail-drawer" id="nh-drawer-${s.gate}">
                <div class="nh-drawer-content">
                  <div class="nh-drawer-grid">
                    <div class="nh-drawer-item">
                      <span class="nh-drawer-label">調教評価</span>
                      ${(() => {
                        const rawG = (s.trainingGrade || '').trim();
                        if (rawG && rawG !== '-' && rawG !== 'null' && rawG !== 'undefined') {
                          const courseStr = s.trainingCourse ? ` ${s.trainingCourse}` : '';
                          const timeStr = s.trainingTime ? ` (${s.trainingTime})` : '';
                          return `<span class="nh-drawer-val-grade grade-${rawG}">【${rawG}】${courseStr}${timeStr}</span>`;
                        }
                        return `<span class="nh-drawer-val">-</span>`;
                      })()}
                    </div>
                    <div class="nh-drawer-item">
                      <span class="nh-drawer-label">調教短評</span>
                      <span class="nh-drawer-val">${s.comment}</span>
                    </div>
                    <div class="nh-drawer-item">
                      <span class="nh-drawer-label">馬体重推移</span>
                      <span class="nh-drawer-val" style="font-size: 11px;">
                        前走: <strong>${s.lastRaceWeight ? s.lastRaceWeight + 'kg' : '-'}</strong> | 
                        調教後: <strong>${s.trainingWeight ? s.trainingWeight + 'kg' : '-'}</strong> | 
                        当日確定: <strong style="color: var(--gold);">${s.confirmedWeight ? s.confirmedWeight + 'kg (' + (s.weightDiff || '±0') + ')' : '未発表（当日発表次第自動反映）'}</strong>
                      </span>
                    </div>
                    <div class="nh-drawer-item">
                      <span class="nh-drawer-label">所属厩舎 / 適性</span>
                      <span class="nh-drawer-val">${s.stable || '栗東'} (${s.jockeyStat})</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          `;
        });

        listContainer.innerHTML = html;
        bindHorseListEvents();
      }

      function bindHorseListEvents() {
        document.querySelectorAll('.nh-mark-btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const gate = btn.getAttribute('data-gate');
            openMarkSheet(gate);
          });
        });

        document.querySelectorAll('[data-action="toggle-drawer"]').forEach(el => {
          el.addEventListener('click', () => {
            const gate = el.getAttribute('data-gate');
            toggleHorseDrawer(gate);
          });
        });
      }

      function toggleHorseDrawer(gate) {
        const drawer = document.getElementById(`nh-drawer-${gate}`);
        const btn = document.getElementById(`nh-toggle-btn-${gate}`);
        const text = document.getElementById(`nh-toggle-text-${gate}`);
        const arrow = document.getElementById(`nh-arrow-${gate}`);

        if (!drawer) return;

        const isOpen = drawer.classList.contains('open');
        if (isOpen) {
          drawer.classList.remove('open');
          if (btn) btn.classList.remove('active');
          if (text) text.innerText = '詳細';
          if (arrow) arrow.innerText = '▾';
        } else {
          drawer.classList.add('open');
          if (btn) btn.classList.add('active');
          if (text) text.innerText = '閉じる';
          if (arrow) arrow.innerText = '▴';
        }
      }

      function renderPredictionOccult() {
        if (typeof document === 'undefined') return;
        const list = document.getElementById('occult-cards-list');
        if (!list) return;

        const currentPred = (PREDICTION_DATA.races && PREDICTION_DATA.races[currentPredictionRaceId])
          ? PREDICTION_DATA.races[currentPredictionRaceId]
          : PREDICTION_DATA;

        const occultSigns = currentPred.occultSigns || [];
        if (occultSigns.length === 0) {
          list.innerHTML = '<div style="padding:16px;text-align:center;color:var(--text-muted);">オカルトサイン考察は順次公開されます</div>';
          return;
        }

        list.innerHTML = occultSigns.map(s => {
          const targetsHtml = (s.targets || []).map(t => `
            <span class="occult-target-pill">
              <span class="nh-gate-cell waku-${t.waku || 1}" style="width:18px;height:18px;font-size:10px;border-radius:3px;">${t.gate}</span>
              <span>${t.name}</span>
            </span>
          `).join('');

          return `
            <div class="occult-card">
              <div class="occult-card-header">
                <span class="occult-badge">${s.badge || '🔮 サイン'}</span>
                <span class="occult-source">${s.source || 'X・SNS話題'}</span>
              </div>
              <h4 class="occult-card-title">${s.title}</h4>
              <p class="occult-card-content">${s.content}</p>
              ${targetsHtml ? `
                <div class="occult-card-targets">
                  <span style="font-size:11px;color:var(--gold);font-weight:700;">🎯 該当推奨馬:</span>
                  ${targetsHtml}
                </div>
              ` : ''}
            </div>
          `;
        }).join('');
      }

      function renderPredictionMemo() {
        if (typeof document === 'undefined') return;
        const memoInput = document.getElementById('prediction-user-memo');
        if (memoInput && typeof localStorage !== 'undefined') {
          const saved = localStorage.getItem('keiba_memo_' + currentPredictionRaceId);
          memoInput.value = saved || '';
        }
      }

      function initPredictionEventListeners() {
        if (typeof document === 'undefined') return;

        const btnBack = document.getElementById('btn-back-to-calendar');
        if (btnBack) {
          btnBack.addEventListener('click', () => {
            switchAppView('calendar', true);
          });
        }

        const btnEst = document.getElementById('btn-odds-estimated');
        const btnLive = document.getElementById('btn-odds-live');
        if (btnEst) {
          btnEst.addEventListener('click', () => setOddsMode('estimated'));
        }
        if (btnLive) {
          btnLive.addEventListener('click', () => setOddsMode('live'));
        }

        const btnRefresh = document.getElementById('btn-refresh-odds');
        if (btnRefresh) {
          btnRefresh.addEventListener('click', () => {
            btnRefresh.classList.add('rotating');
            setTimeout(() => btnRefresh.classList.remove('rotating'), 600);
            refreshLiveOdds(true);
          });
        }

        const sortGateBtn = document.getElementById('btn-sort-gate');
        const sortPopBtn = document.getElementById('btn-sort-pop');

        if (sortGateBtn) {
          sortGateBtn.addEventListener('click', () => {
            predictionSortType = 'gate';
            sortGateBtn.classList.add('active');
            if (sortPopBtn) sortPopBtn.classList.remove('active');
            renderNetkeibaHorseList();
          });
        }
        if (sortPopBtn) {
          sortPopBtn.addEventListener('click', () => {
            predictionSortType = 'pop';
            sortPopBtn.classList.add('active');
            if (sortGateBtn) sortGateBtn.classList.remove('active');
            renderNetkeibaHorseList();
          });
        }

        const btnCloseSheet = document.getElementById('btn-close-sheet');
        const sheetBackdrop = document.getElementById('mark-sheet-backdrop');
        if (btnCloseSheet) btnCloseSheet.addEventListener('click', closeMarkSheet);
        if (sheetBackdrop) sheetBackdrop.addEventListener('click', closeMarkSheet);

        document.querySelectorAll('.btn-sheet-mark').forEach(btn => {
          btn.addEventListener('click', () => {
            const mark = btn.getAttribute('data-mark');
            if (activeSheetGate) {
              setUserMark(activeSheetGate, mark);
            }
            closeMarkSheet();
          });
        });

        const memoInput = document.getElementById('prediction-user-memo');
        const saveStatus = document.getElementById('memo-save-status');
        const btnClearMemo = document.getElementById('btn-clear-memo');

        if (memoInput) {
          let memoTimer = null;
          memoInput.addEventListener('input', () => {
            if (saveStatus) saveStatus.innerText = '編集中...';
            if (memoTimer) clearTimeout(memoTimer);
            memoTimer = setTimeout(() => {
              if (typeof localStorage !== 'undefined') {
                localStorage.setItem('keiba_memo_' + currentPredictionRaceId, memoInput.value);
              }
              if (saveStatus) {
                saveStatus.innerText = '💾 自動保存完了';
                setTimeout(() => { saveStatus.innerText = ''; }, 2000);
              }
            }, 600);
          });
        }

        if (btnClearMemo && memoInput) {
          btnClearMemo.addEventListener('click', () => {
            memoInput.value = '';
            if (typeof localStorage !== 'undefined') {
              localStorage.removeItem('keiba_memo_' + currentPredictionRaceId);
            }
            if (saveStatus) saveStatus.innerText = '🗑️ 消去完了';
          });
        }
      }

      function switchAppView(viewName, pushState = true) {
        switchView(viewName, true, false);
        if (pushState && window.history) {
          const targetHash = (viewName === 'prediction') ? ('#prediction-' + currentPredictionRaceId) : '#calendar';
          window.history.pushState({ view: viewName, raceId: currentPredictionRaceId }, '', targetHash);
        }
      }
"""

# Enhanced openRaceDetail supporting both finished results and upcoming contenders
open_race_detail_func = """
      function openRaceDetail(id, updateRoute = true) {
        const race = G1_RACES.find(r => r.id === String(id));
        if (!race) return;

        if (updateRoute && typeof window !== 'undefined') {
          const targetHash = '#race-' + id;
          if (window.location.hash !== targetHash) {
            window.location.hash = targetHash;
          }
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('keiba_active_route', targetHash);
          }
        }

        const modal = document.getElementById('modal-race-detail');
        const title = document.getElementById('detail-modal-title');
        const body = document.getElementById('detail-modal-body');

        if (!modal || !title || !body) return;

        title.innerText = `${race.name} (G1) 詳細`;

        const raceDate = new Date(race.date);
        const formattedDate = raceDate.toLocaleDateString('ja-JP', {
          year: 'numeric', month: 'long', day: 'numeric', weekday: 'short'
        });

        const entries = typeof ENTRIES_DATA !== 'undefined' ? ENTRIES_DATA[id] : null;

        let historyTableRows = '';
        let historyData = (typeof HISTORICAL_DATA !== 'undefined' && HISTORICAL_DATA[id]) ? HISTORICAL_DATA[id] : [];
        const fullHistoryMap = (typeof HISTORICAL_FULL_RESULTS !== 'undefined' && HISTORICAL_FULL_RESULTS[id]) ? HISTORICAL_FULL_RESULTS[id] : {};

        if ((!historyData || historyData.length === 0) && fullHistoryMap && Object.keys(fullHistoryMap).length > 0) {
          const sortedYears = Object.keys(fullHistoryMap).sort((a, b) => parseInt(b) - parseInt(a));
          historyData = sortedYears.map(y => {
            const list = fullHistoryMap[y];
            const winner = list.find(h => h.rank === 1) || list[0];
            return [
              parseInt(y),
              winner ? winner.horseName : '-',
              winner ? winner.jockey : '-',
              winner ? winner.time : '-',
              winner ? (parseInt(winner.pop) || 1) : 1,
              winner ? winner.stable : '-'
            ];
          });
        }

        historyData.forEach((h, hIdx) => {
          const year = h[0];
          const fullList = fullHistoryMap[year] || [];
          
          let fullRowsHtml = '';
          fullList.forEach(m => {
            let rankBadge = m.rank;
            let rankClass = 'rank-other';
            if (m.rank === 1) rankClass = 'rank-1';
            else if (m.rank === 2) rankClass = 'rank-2';
            else if (m.rank === 3) rankClass = 'rank-3';

            fullRowsHtml += `
              <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                <td style="text-align: center;"><span class="rank-badge ${rankClass}" style="width:20px;height:20px;font-size:11px;">${rankBadge}</span></td>
                <td style="text-align: center; font-family: monospace; font-weight: 700;"><span class="nh-gate-cell waku-${m.waku || 1}" style="width:20px;height:20px;font-size:11px;border-radius:3px;display:inline-flex;">${m.gate}</span></td>
                <td style="font-weight: 700; color: #fff;">${m.horseName}</td>
                <td>${m.sexAge}</td>
                <td>${m.load}</td>
                <td>${m.jockey}</td>
                <td style="font-family: monospace; font-weight: 600;">${m.time}</td>
                <td>${m.margin}</td>
                <td style="font-size: 11px; color: var(--text-muted);">${m.passing}</td>
                <td style="font-family: monospace;">${m.last3F}</td>
                <td style="font-family: monospace;">${m.odds}</td>
                <td>${m.pop}</td>
                <td>${m.weight}</td>
                <td style="font-size: 12px; color: var(--text-muted);">${m.stable}</td>
              </tr>
            `;
          });

          const subTableHtml = fullList.length > 0 ? `
            <tr id="history-detail-${id}-${year}" class="history-detail-row" style="display: none; background: rgba(0,0,0,0.5);">
              <td colspan="6" style="padding: 12px 8px;">
                <div style="font-size: 12px; font-weight: 700; color: var(--gold); margin-bottom: 8px;">
                  📋 ${year}年 全着順・詳細データ (${fullList.length}頭出走)
                </div>
                <div class="table-scroll-container" style="max-height: 320px; overflow-y: auto;">
                  <table class="result-table" style="font-size: 11px; width: 100%;">
                    <thead>
                      <tr style="position: sticky; top: 0; background: #13231d; z-index: 2;">
                        <th style="width: 32px; text-align: center;">着</th>
                        <th style="width: 32px; text-align: center;">番</th>
                        <th>馬名</th>
                        <th>性齢</th>
                        <th>斤量</th>
                        <th>騎手</th>
                        <th>タイム</th>
                        <th>着差</th>
                        <th>通過</th>
                        <th>上り</th>
                        <th>単勝</th>
                        <th>人気</th>
                        <th>馬体重</th>
                        <th>厩舎</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${fullRowsHtml}
                    </tbody>
                  </table>
                </div>
              </td>
            </tr>
          ` : '';

          historyTableRows += `
            <tr class="history-year-row" data-year="${year}" data-race-id="${id}" style="cursor: pointer;" title="クリックで全頭成績を展開">
              <td style="text-align: center; font-family: monospace; font-weight: 700; color: var(--gold);">
                ${year} <i data-lucide="chevron-right" class="toggle-icon" style="width: 12px; height: 12px; display: inline-block; transition: transform 0.2s;"></i>
              </td>
              <td style="font-weight: 700; color: #fff;">${h[1]}</td>
              <td>${h[2]}</td>
              <td style="font-family: monospace;">${h[3]}</td>
              <td>${h[4]}人気</td>
              <td style="font-size: 12px; color: var(--text-muted);">${h[5]}</td>
            </tr>
            ${subTableHtml}
          `;
        });

        let innerHTML = '';

        if (race.status === 'finished') {
          innerHTML = `
            <div class="modal-tabs">
              <button class="modal-tab-btn active" data-tab="result">レース結果・全着順</button>
              <button class="modal-tab-btn" data-tab="payouts">払戻金一覧</button>
              <button class="modal-tab-btn" data-tab="history">歴代優勝馬（過去10年）</button>
            </div>

            <div id="modal-tab-content-result" class="modal-tab-content">
              ${(typeof PREDICTION_DATA !== 'undefined' && PREDICTION_DATA.races && PREDICTION_DATA.races[id]) ? `
                <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(16, 185, 129, 0.15)); border: 1px solid var(--gold); border-radius: 10px; padding: 12px 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                  <div>
                    <div style="font-size: 14px; font-weight: 800; color: #fff;">🎯 ${race.name} 専用の「予想・攻略分析」を見る</div>
                    <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">netkeibaオッズ・調教評価・Xオカルトサイン・打った印の振り返り</div>
                  </div>
                  <button class="btn-jump-prediction" data-race-id="${id}" style="background: var(--gold); color: #111; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 800; font-size: 12px; cursor: pointer;">
                    予想・攻略を見る ➔
                  </button>
                </div>
              ` : ''}

              <div class="detail-meta-grid">
                <div class="detail-meta-item">
                  <span class="detail-meta-label">開催日 / 発走時刻</span>
                  <span class="detail-meta-value">${formattedDate} 15:40</span>
                </div>
                <div class="detail-meta-item">
                  <span class="detail-meta-label">開催場 / コース</span>
                  <span class="detail-meta-value">${race.location}競馬場 | ${race.course}</span>
                </div>
                <div class="detail-meta-item">
                  <span class="detail-meta-label">天候 / 馬場状態</span>
                  <span class="detail-meta-value">${race.weather || '晴'} / ${race.trackCondition || '良'} (クッション値: ${race.cushionValue || '9.5'})</span>
                </div>
                <div class="detail-meta-item">
                  <span class="detail-meta-label">優勝馬 / 騎手</span>
                  <span class="detail-meta-value" style="color: var(--gold); font-weight: 700;">
                    ${race.winner} (${race.winnerJockey})
                  </span>
                </div>
              </div>

              <h3 class="detail-section-title">全着順確定結果</h3>
              <div class="table-scroll-container">
                <table class="result-table">
                  <thead>
                    <tr>
                      <th style="width: 44px; text-align: center;">着順</th>
                      <th style="width: 44px; text-align: center;">馬番</th>
                      <th>馬名</th>
                      <th>性齢</th>
                      <th>斤量</th>
                      <th>騎手</th>
                      <th>タイム</th>
                      <th>着差</th>
                      <th>通過順</th>
                      <th>上がり3F</th>
                      <th>単勝オッズ</th>
                      <th>人気</th>
                      <th>馬体重</th>
                      <th>調教師</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${(() => {
                      const rawRes = RESULTS_DATA[id];
                      const rList = Array.isArray(rawRes) ? rawRes : (rawRes && rawRes.horses ? rawRes.horses : []);
                      const totalHorses = rList.length;
                      return rList.map(r => {
                        let rankBadge = r[0];
                        let rankClass = 'rank-other';
                        if (r[0] === 1) rankClass = 'rank-1';
                        else if (r[0] === 2) rankClass = 'rank-2';
                        else if (r[0] === 3) rankClass = 'rank-3';

                        let wakuColor = 1;
                        const gateNum = Number(r[1]);
                        if (gateNum > 0 && totalHorses > 0) {
                          wakuColor = Math.min(8, Math.max(1, Math.ceil(gateNum / (totalHorses / 8))));
                        }

                      return `
                        <tr>
                          <td style="text-align: center;"><span class="rank-badge ${rankClass}">${rankBadge}</span></td>
                          <td style="text-align: center; font-family: monospace; font-weight: 700;"><span class="nh-gate-cell waku-${wakuColor}" style="width:24px;height:24px;font-size:12px;border-radius:4px;display:inline-flex;">${r[1]}</span></td>
                          <td style="font-weight: 700; color: #fff;">${r[2]}</td>
                          <td>${r[3]}</td>
                          <td>${r[4]}</td>
                          <td>${r[5]}</td>
                          <td style="font-family: monospace; font-weight: 600;">${r[6]}</td>
                          <td>${r[7]}</td>
                          <td style="font-size: 12px; color: var(--text-muted);">${r[8]}</td>
                          <td style="font-family: monospace;">${r[9]}</td>
                          <td style="font-family: monospace;">${r[10]}</td>
                          <td>${r[11]}</td>
                          <td>${r[12]}${r[13] ? ` (${r[13]})` : ''}</td>
                          <td style="font-size: 13px; color: var(--text-muted);">${r[14] || '-'}</td>
                        </tr>
                      `;
                      }).join('');
                    })()}
                  </tbody>
                </table>
              </div>
            </div>

            <div id="modal-tab-content-payouts" class="modal-tab-content" style="display: none;">
              <h3 class="detail-section-title">払戻金確定情報</h3>
              <div class="payouts-grid">
                ${(() => {
                  let pList = [];
                  if (PAYOUTS_DATA[id]) {
                    if (Array.isArray(PAYOUTS_DATA[id])) {
                      pList = PAYOUTS_DATA[id];
                    } else if (PAYOUTS_DATA[id].payoutsList) {
                      pList = PAYOUTS_DATA[id].payoutsList;
                    }
                  }
                  if (pList.length === 0 && RESULTS_DATA[id] && RESULTS_DATA[id].payouts) {
                    pList = RESULTS_DATA[id].payouts;
                  }
                  if (pList.length === 0 && race) {
                    pList = hydratePayouts(race) || [];
                  }
                  return pList.map(p => {
                    let popDisplay = "";
                    if (p.pop) {
                      const parts = String(p.pop).split("<br>").map(x => x.includes("人気") ? x : (x ? x + "人気" : ""));
                      popDisplay = parts.join("<br>");
                    }
                    return `
                      <div class="payout-item">
                        <div style="display: flex; align-items: center; gap: 10px;">
                          <span class="payout-type">${p.type}</span>
                          <span class="payout-comb">${p.comb}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px; text-align: right;">
                          <span class="payout-value">${p.val}</span>
                          ${popDisplay ? `<span class="payout-pop">${popDisplay}</span>` : ""}
                        </div>
                      </div>
                    `;
                  }).join("");
                })()}
              </div>
            </div>

            <div id="modal-tab-content-history" class="modal-tab-content" style="display: none;">
              <h3 class="detail-section-title">過去10年の歴代優勝馬（傾向分析）</h3>
              <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">各年をクリックすると、該当年の全頭着順一覧が展開されます。</p>
              <div class="table-scroll-container">
                <table class="result-table" style="width: 100%;">
                  <thead>
                    <tr>
                      <th style="width: 80px; text-align: center;">開催年</th>
                      <th>優勝馬</th>
                      <th>騎手</th>
                      <th>タイム</th>
                      <th>人気</th>
                      <th>調教師</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${historyTableRows}
                  </tbody>
                </table>
              </div>
            </div>
          `;
        } else if (entries && entries.length > 0) {
          innerHTML = `
            <div class="modal-tabs">
              <button class="modal-tab-btn active" data-tab="entries">出馬表・登録馬一覧</button>
              <button class="modal-tab-btn" data-tab="history">歴代優勝馬（過去10年）</button>
            </div>

            <div id="modal-tab-content-entries" class="modal-tab-content">
              <!-- 予想・オカルト誘導プレミアムバナー -->
              <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(16, 185, 129, 0.18)); border: 1px solid var(--gold); border-radius: 12px; padding: 14px 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.15);">
                <div>
                  <div style="font-size: 15px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 6px;">
                    🎯 <span>${race.name} 専用の「予想・攻略分析＆Xオカルト」公開中！</span>
                  </div>
                  <div style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                    netkeiba想定オッズ・調教評価・X話題オカルトサイン・印管理を完備
                  </div>
                </div>
                <button class="btn-jump-prediction" data-race-id="${id}" style="background: var(--gold); color: #111; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 800; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                  予想・オカルトを見る ➔
                </button>
              </div>

              <div class="detail-meta-grid">
                <div class="detail-meta-item">
                  <span class="detail-meta-label">開催日 / 発走時刻</span>
                  <span class="detail-meta-value">${formattedDate} 15:40</span>
                </div>
                <div class="detail-meta-item">
                  <span class="detail-meta-label">開催場 / コース</span>
                  <span class="detail-meta-value">${race.location}競馬場 | ${race.course}</span>
                </div>
                <div class="detail-meta-item">
                  <span class="detail-meta-label">条件 / 登録頭数</span>
                  <span class="detail-meta-value">${race.name.includes('女王杯') || race.name.includes('フィリーズ') ? '牝馬限定' : 'オープン'} / 全${entries.length}頭</span>
                </div>
                <div class="detail-meta-item">
                  <span class="detail-meta-label">枠順ステータス</span>
                  <span class="detail-meta-value" style="color: var(--primary); font-weight: 700;">
                    ${id === '17' ? '枠順確定済 (出走16頭)' : '出走登録馬・想定枠順'}
                  </span>
                </div>
              </div>

              <h3 class="detail-section-title">出走登録馬・想定出馬表一覧</h3>
              <div class="table-scroll-container">
                <table class="result-table">
                  <thead>
                    <tr>
                      <th style="width: 44px; text-align: center;">番</th>
                      <th style="width: 44px; text-align: center;">枠</th>
                      <th>馬名</th>
                      <th>性齢</th>
                      <th>斤量</th>
                      <th>想定騎手</th>
                      <th>所属厩舎</th>
                      <th>想定オッズ</th>
                      <th>馬体重</th>
                      <th>調教/状態</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${(() => {
                      const predStarters = (typeof PREDICTION_DATA !== 'undefined' && PREDICTION_DATA.races && PREDICTION_DATA.races[id]) 
                        ? PREDICTION_DATA.races[id].starters 
                        : null;
                      return entries.map(e => {
                        const pHorse = predStarters ? predStarters.find(s => s.gate === e.gate || s.horseName === e.horseName) : null;
                        const oddsVal = pHorse ? (pHorse.odds ? pHorse.odds + '倍' : '--') : '--';
                        const popVal = pHorse ? `(${pHorse.pop}人気)` : '';

                        let weightVal = '-';
                        if (pHorse) {
                          if (pHorse.confirmedWeight) {
                            weightVal = `${pHorse.confirmedWeight}kg`;
                          } else if (pHorse.lastRaceWeight || pHorse.prevWeight) {
                            weightVal = `${pHorse.lastRaceWeight || pHorse.prevWeight}kg <span class="weight-tag-prev" style="font-size:10px;">前走</span>`;
                          } else if (pHorse.trainingWeight) {
                            weightVal = `${pHorse.trainingWeight}kg <span class="weight-tag-pre" style="font-size:10px;">調教後</span>`;
                          }
                        }

                        let gradeVal = '-';
                        if (pHorse && pHorse.trainingGrade && pHorse.trainingGrade !== '-' && pHorse.trainingGrade !== 'null') {
                          gradeVal = `【${pHorse.trainingGrade}】`;
                        }

                        return `
                          <tr>
                            <td style="text-align: center; font-family: monospace; font-weight: 700;">
                              <span class="nh-gate-cell waku-${e.waku || 1}" style="width:24px;height:24px;font-size:12px;border-radius:4px;display:inline-flex;">${e.gate}</span>
                            </td>
                            <td style="text-align: center; font-weight: 700; color: var(--text-muted);">${e.waku || 1}枠</td>
                            <td style="font-weight: 700; color: #fff;">${e.horseName}</td>
                            <td>${e.sexAge}</td>
                            <td>${e.load}kg</td>
                            <td>${e.jockey}</td>
                            <td style="font-size: 12px; color: var(--text-muted);">${e.stable}</td>
                            <td style="font-family: monospace; font-weight: 700; color: var(--gold);">${oddsVal} <span style="font-size:11px;color:var(--text-muted);">${popVal}</span></td>
                            <td style="font-family: monospace; font-size: 12px;">${weightVal}</td>
                            <td style="font-size: 12px;">${gradeVal}</td>
                          </tr>
                        `;
                      }).join('');
                    })()}
                  </tbody>
                </table>
              </div>
            </div>

            <div id="modal-tab-content-history" class="modal-tab-content" style="display: none;">
              <h3 class="detail-section-title">過去10年の歴代優勝馬（傾向分析）</h3>
              <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">各年をクリックすると、該当年の全頭着順一覧が展開されます。</p>
              <div class="table-scroll-container">
                <table class="result-table" style="width: 100%;">
                  <thead>
                    <tr>
                      <th style="width: 80px; text-align: center;">開催年</th>
                      <th>優勝馬</th>
                      <th>騎手</th>
                      <th>タイム</th>
                      <th>人気</th>
                      <th>調教師</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${historyTableRows}
                  </tbody>
                </table>
              </div>
            </div>
          `;
        } else {
          innerHTML = `
            <div class="modal-tabs">
              <button class="modal-tab-btn active" data-tab="history">歴代優勝馬（過去10年）</button>
            </div>
            <div id="modal-tab-content-history" class="modal-tab-content">
              <div class="table-scroll-container">
                <table class="result-table" style="width: 100%;">
                  <thead>
                    <tr>
                      <th style="width: 80px; text-align: center;">開催年</th>
                      <th>優勝馬</th>
                      <th>騎手</th>
                      <th>タイム</th>
                      <th>人気</th>
                      <th>調教師</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${historyTableRows}
                  </tbody>
                </table>
              </div>
            </div>
          `;
        }

        body.innerHTML = innerHTML;

        // タブ切替バインド
        const modalTabBtns = modal.querySelectorAll('.modal-tab-btn');
        modalTabBtns.forEach(btn => {
          btn.addEventListener('click', () => {
            modalTabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const tabName = btn.getAttribute('data-tab');
            modal.querySelectorAll('.modal-tab-content').forEach(c => c.style.display = 'none');
            const targetContent = document.getElementById(`modal-tab-content-${tabName}`);
            if (targetContent) targetContent.style.display = 'block';
          });
        });

        // 過去年度の全頭展開アコーディオン
        modal.querySelectorAll('.history-year-row').forEach(row => {
          row.addEventListener('click', () => {
            const y = row.getAttribute('data-year');
            const rId = row.getAttribute('data-race-id');
            const detailRow = document.getElementById(`history-detail-${rId}-${y}`);
            const icon = row.querySelector('.toggle-icon');
            if (!detailRow) return;
            const isHidden = detailRow.style.display === 'none';
            detailRow.style.display = isHidden ? 'table-row' : 'none';
            if (icon) {
              icon.style.transform = isHidden ? 'rotate(90deg)' : 'none';
            }
          });
        });

        // 予想ページへのジャンプボタン
        modal.querySelectorAll('.btn-jump-prediction').forEach(btn => {
          btn.addEventListener('click', (e) => {
            const targetRaceId = btn.getAttribute('data-race-id');
            closeModal();
            if (typeof setPredictionRace === 'function') {
              setPredictionRace(targetRaceId);
            }
            navigateTo('#prediction-' + targetRaceId);
          });
        });

        // モーダル表示
        modal.classList.add('open', 'active');
        document.body.style.overflow = 'hidden';
        refreshIcons();
      }
"""

# Update initEventListeners
event_listeners_js = """
      function initEventListeners() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
          btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.getAttribute('data-filter');
            if (typeof localStorage !== 'undefined') {
              localStorage.setItem('keiba_calendar_filter', currentFilter);
            }
            renderRaces();
          });
        });

        const searchInput = document.getElementById('race-search');
        if (searchInput) {
          searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value;
            renderRaces();
          });
        }

        const gridContainer = document.getElementById('race-grid-container');
        if (gridContainer) {
          gridContainer.addEventListener('click', (e) => {
            const card = e.target.closest('.race-card');
            if (!card) return;
            const id = card.getAttribute('data-id');
            openRaceDetail(id);
          });
        }

        const modal = document.getElementById('modal-race-detail');
        if (modal) {
          const btnClose = document.getElementById('btn-close-modal');
          const backdrop = modal.querySelector('.modal-backdrop');
          
          if (btnClose) btnClose.addEventListener('click', closeModal);
          if (backdrop) backdrop.addEventListener('click', closeModal);
          modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('modal-backdrop')) {
              closeModal();
            }
          });
        }

        if (typeof window !== 'undefined') {
          window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
              closeModal();
              if (typeof closeMarkSheet === 'function') closeMarkSheet();
            }
          });
        }

        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(n => {
          n.addEventListener('click', () => {
            const target = n.getAttribute('data-target');
            if (target === 'prediction') {
              navigateTo('#prediction-' + currentPredictionRaceId);
            } else {
              navigateTo('#calendar');
            }
          });
        });

        const heroBanner = document.getElementById('hero-countdown-banner');
        if (heroBanner) {
          heroBanner.addEventListener('click', (e) => {
            const nextR = (typeof getNextUpcomingRace === 'function') ? getNextUpcomingRace() : { id: '17' };
            if (e.target.closest('#btn-hero-detail')) {
              e.stopPropagation();
              openRaceDetail(nextR.id);
              return;
            }
            if (typeof setPredictionRace === 'function') setPredictionRace(nextR.id);
            navigateTo('#prediction-' + nextR.id);
          });
        }

        const btnHeroPred = document.getElementById('btn-hero-prediction');
        if (btnHeroPred) {
          btnHeroPred.addEventListener('click', (e) => {
            e.stopPropagation();
            const nextR = (typeof getNextUpcomingRace === 'function') ? getNextUpcomingRace() : { id: '17' };
            if (typeof setPredictionRace === 'function') setPredictionRace(nextR.id);
            navigateTo('#prediction-' + nextR.id);
          });
        }
      }
"""

# Update countdown in helpers
helpers_clean = re.sub(
    r'function startNextRaceCountdown\(\)[\s\S]*?(?=// -+\s*// レースグリッド|function renderRaces)',

    """function startNextRaceCountdown() {
        const timerDays = document.getElementById('timer-days');
        const timerHours = document.getElementById('timer-hours');
        const timerMinutes = document.getElementById('timer-minutes');
        const timerSeconds = document.getElementById('timer-seconds');
        
        const nextRaceName = document.getElementById('next-race-name');
        const nextRaceMeta = document.getElementById('next-race-meta');
        const btnHeroPred = document.getElementById('btn-hero-prediction');
        
        function updateCountdown() {
          const now = new Date();
          const upcomingRaces = G1_RACES
            .filter(r => new Date(r.date) > now)
            .sort((a, b) => new Date(a.date) - new Date(b.date));
            
          if (upcomingRaces.length === 0) {
            if (nextRaceName) nextRaceName.innerText = '2026年 G1レース全日程終了';
            if (nextRaceMeta) nextRaceMeta.innerText = '全レースのご声援ありがとうございました';
            if (timerDays) timerDays.innerText = '00';
            if (timerHours) timerHours.innerText = '00';
            if (timerMinutes) timerMinutes.innerText = '00';
            if (timerSeconds) timerSeconds.innerText = '00';
            if (countdownInterval) clearInterval(countdownInterval);
            return;
          }
          
          const nextRace = upcomingRaces[0];
          const raceTime = new Date(nextRace.date);
          const diffMs = raceTime - now;
          
          if (nextRaceName) nextRaceName.innerText = nextRace.name;
          if (btnHeroPred) btnHeroPred.innerHTML = `🎯 ${nextRace.name} 予想・攻略を見る`;
          
          const formattedDate = new Date(nextRace.date).toLocaleDateString('ja-JP', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'short'
          });
          if (nextRaceMeta) {
            nextRaceMeta.innerText = `開催日: ${formattedDate} 15:40発走 | ${nextRace.location}競馬場 (${nextRace.course})`;
          }
          
          const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
          const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);
          
          if (timerDays) timerDays.innerText = String(days).padStart(2, '0');
          if (timerHours) timerHours.innerText = String(hours).padStart(2, '0');
          if (timerMinutes) timerMinutes.innerText = String(minutes).padStart(2, '0');
          if (timerSeconds) timerSeconds.innerText = String(seconds).padStart(2, '0');
        }
        
        updateCountdown();
        if (countdownInterval) clearInterval(countdownInterval);
        countdownInterval = setInterval(updateCountdown, 1000);
      }""",
    existing_helpers
)

format_time_func = """
      function formatSecondsToTime(seconds) {
        if (isNaN(seconds)) return '-';
        const m = Math.floor(seconds / 60);
        const s = (seconds % 60).toFixed(1);
        return m > 0 ? `${m}:${s.padStart(4, '0')}` : `${s}`;
      }
"""

init_app_block = """
      function initApp() {
        if (typeof localStorage !== 'undefined') {
          const savedFilter = localStorage.getItem('keiba_calendar_filter');
          if (savedFilter) {
            currentFilter = savedFilter;
            const targetBtn = document.querySelector(`.tab-btn[data-filter="${savedFilter}"]`);
            if (targetBtn) {
              const tabBtns = document.querySelectorAll('.tab-btn');
              tabBtns.forEach(b => b.classList.remove('active'));
              targetBtn.classList.add('active');
            }
          }
        }

        initEventListeners();
        initPredictionEventListeners();

        if (typeof autoLifecycleEngine === 'function') autoLifecycleEngine();
        renderRaces();
        updateTabCounts();
        startNextRaceCountdown();

        handleRoute(false);

        if (typeof window !== 'undefined') {
          window.addEventListener('hashchange', () => {
            handleRoute(false);
          });
        }

        if (typeof setInterval !== 'undefined') {
          if (typeof autoLifecycleEngine === 'function') setInterval(autoLifecycleEngine, 60000);
          if (typeof startOddsAutoRefresh === 'function') startOddsAutoRefresh();
        }
      }

      if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initApp);
        } else {
          initApp();
        }
      }
"""

# Assemble full script block
full_script_content = (
    "      // 2026年 JRA G1レースデータセット\n"
    + "      " + g1_races_str + "\n\n"
    + "      " + new_results_data_str + "\n\n"
    + "      " + historical_data_str + "\n\n"
    + "      " + entries_data_str + "\n\n"
    + "      " + payouts_data_str + "\n\n"
    + "      " + hist_full_str + "\n\n"
    + "      " + pred_data_str + "\n\n"
    + helpers_clean + "\n\n"
    + format_time_func + "\n\n"
    + event_listeners_js + "\n\n"
    + prediction_js_logic + "\n\n"
    + open_race_detail_func + "\n\n"
    + init_app_block
)

final_index_html = new_main_content + full_script_content + "    </script>\n  </body>\n</html>\n"

with open(index_html_path, 'w', encoding='utf-8') as f:
    f.write(final_index_html)
print(f"Generated clean index.html v10: {len(final_index_html)} bytes")

# Update src/main.js
main_js_content = (
    "import { HISTORICAL_FULL_RESULTS } from './historical_results.js';\n"
    + "import { ENTRIES_DATA } from './entries_data.js';\n"
    + "import { PREDICTION_DATA } from './prediction_data.js';\n"
    + "import './style.css';\n\n"
    + g1_races_str + "\n\n"
    + new_results_data_str + "\n\n"
    + historical_data_str + "\n\n"
    + payouts_data_str + "\n\n"
    + helpers_clean + "\n\n"
    + format_time_func + "\n\n"
    + event_listeners_js + "\n\n"
    + prediction_js_logic + "\n\n"
    + open_race_detail_func + "\n\n"
    + init_app_block
)

with open(main_js_path, 'w', encoding='utf-8') as f:
    f.write(main_js_content)
print(f"Generated clean src/main.js v10: {len(main_js_content)} bytes")
