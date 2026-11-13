import json, os

APP_DIR = '/Users/ooshita/.gemini/antigravity/scratch/keiba-app'
PRED_JSON = os.path.join(APP_DIR, 'src', 'prediction_data.json')

# JRA Official Announced Post-Training Horse Weights (2026-11-12 JRA Official Release)
# 第51回 エリザベス女王杯 (G1)
OFFICIAL_WEIGHTS = {
  "アクアヴァーナル":   { "trainingWeight": 480, "lastRaceWeight": 476, "diff": "+4" },
  "ヴーレヴー":         { "trainingWeight": 506, "lastRaceWeight": 496, "diff": "+10" },
  "エストゥペンダ":     { "trainingWeight": 454, "lastRaceWeight": 446, "diff": "+8" },
  "カムニャック":       { "trainingWeight": 504, "lastRaceWeight": 496, "diff": "+8" },
  "クイーンズウォーク": { "trainingWeight": 550, "lastRaceWeight": 544, "diff": "+6" },
  "ケリフレッドアスク": { "trainingWeight": 466, "lastRaceWeight": 462, "diff": "+4" },
  "コガネノソラ":       { "trainingWeight": 480, "lastRaceWeight": 468, "diff": "+12" },
  "シャドウメテオ":     { "trainingWeight": 470, "lastRaceWeight": 458, "diff": "+12" },
  "ジュウリョクピエロ": { "trainingWeight": 490, "lastRaceWeight": 464, "diff": "+26" },
  "ジョスラン":         { "trainingWeight": 485, "lastRaceWeight": 480, "diff": "+5" },
  "ステレンボッシュ":   { "trainingWeight": 484, "lastRaceWeight": 478, "diff": "+6" },
  "セキトバイースト":   { "trainingWeight": 472, "lastRaceWeight": 474, "diff": "-2" },
  "チェルヴィニア":     { "trainingWeight": 520, "lastRaceWeight": 504, "diff": "+16" },
  "ニシノティアモ":     { "trainingWeight": 452, "lastRaceWeight": 446, "diff": "+6" },
  "ラヴァンダ":         { "trainingWeight": 498, "lastRaceWeight": 490, "diff": "+8" },
  "ラフターラインズ":   { "trainingWeight": 474, "lastRaceWeight": 462, "diff": "+12" },
  "レイクラシック":     { "trainingWeight": 500, "lastRaceWeight": 498, "diff": "+2" },
  "レーゼドラマ":       { "trainingWeight": 488, "lastRaceWeight": 472, "diff": "+16" }
}

with open(PRED_JSON, 'r', encoding='utf-8') as f:
    pred = json.load(f)

r17 = pred.get('races', {}).get('17', {})
starters = r17.get('starters', [])

updated_count = 0
for s in starters:
    name = s['horseName']
    if name in OFFICIAL_WEIGHTS:
        w_info = OFFICIAL_WEIGHTS[name]
        s['trainingWeight'] = w_info['trainingWeight']
        s['lastRaceWeight'] = w_info['lastRaceWeight']
        s['trainingWeightDiff'] = w_info['diff']
        # also update in prevRace if present
        if 'prevRace' in s and s['prevRace']:
            s['prevRace']['weight'] = w_info['lastRaceWeight']
        updated_count += 1
        print(f"Updated {name}: 前走 {w_info['lastRaceWeight']}kg -> 調教後 {w_info['trainingWeight']}kg ({w_info['diff']})")

with open(PRED_JSON, 'w', encoding='utf-8') as f:
    json.dump(pred, f, ensure_ascii=False, indent=2)

with open(os.path.join(APP_DIR, 'src', 'prediction_data.js'), 'w', encoding='utf-8') as f:
    f.write('export const PREDICTION_DATA = ' + json.dumps(pred, ensure_ascii=False, indent=2) + ';\n')

print(f"Successfully updated all {updated_count} starters with official JRA post-training weights!")
