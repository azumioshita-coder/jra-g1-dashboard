import json
import os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(APP_DIR, 'src')

PRED_JSON = os.path.join(SRC_DIR, 'prediction_data.json')
PRED_JS = os.path.join(SRC_DIR, 'prediction_data.js')

JC_OFFICIAL_WEIGHTS = {
    # 1枠1番 ヘデントール (前走京都大賞典 488kg +6)
    "ヘデントール": {
        "lastRaceWeight": 488,
        "trainingWeight": 494,
        "trainingWeightDiff": "+6"
    },
    # 1枠2番 コスモキュランダ (前走天皇賞秋 524kg +10)
    "コスモキュランダ": {
        "lastRaceWeight": 524,
        "trainingWeight": 528,
        "trainingWeightDiff": "+4"
    },
    # 2枠3番 メイショウタバル (国内前走・神戸新聞杯 500kg +6, 宝塚記念 502kg)
    "メイショウタバル": {
        "lastRaceWeight": 502,
        "trainingWeight": 508,
        "trainingWeightDiff": "+6"
    },
    # 2枠4番 クロワデュノール (前走天皇賞秋 512kg -2)
    "クロワデュノール": {
        "lastRaceWeight": 512,
        "trainingWeight": 518,
        "trainingWeightDiff": "+6"
    },
    # 3枠5番 シェイクユアハート (前走天皇賞秋 452kg +2)
    "シェイクユアハート": {
        "lastRaceWeight": 452,
        "trainingWeight": 456,
        "trainingWeightDiff": "+4"
    },
    # 3枠6番 マスカレードボール (前走天皇賞秋 474kg ±0)
    "マスカレードボール": {
        "lastRaceWeight": 474,
        "trainingWeight": 480,
        "trainingWeightDiff": "+6"
    },
    # 4枠7番 ファイアンクランツ (前走アルゼンチン共和国杯 480kg +4)
    "ファイアンクランツ": {
        "lastRaceWeight": 480,
        "trainingWeight": 486,
        "trainingWeightDiff": "+6"
    },
    # 4枠8番 オンブズマン (英国馬・ゴスデン厩舎 / 検疫計測482kg)
    "オンブズマン": {
        "lastRaceWeight": None,
        "trainingWeight": 482,
        "trainingWeightDiff": None
    },
    # 5枠9番 カランダガン (仏国馬・グラファール厩舎 / 来日計測469kg -> 調教後468kg)
    "カランダガン": {
        "lastRaceWeight": None,
        "trainingWeight": 468,
        "trainingWeightDiff": None
    },
    # 5枠10番 ミニーホーク (愛国馬・オブライエン厩舎・4歳牝馬 / 来日計測462kg)
    "ミニーホーク": {
        "lastRaceWeight": None,
        "trainingWeight": 462,
        "trainingWeightDiff": None
    },
    # 6枠11番 ヴェルテンベルク (前走京都大賞典 484kg ±0)
    "ヴェルテンベルク": {
        "lastRaceWeight": 484,
        "trainingWeight": 488,
        "trainingWeightDiff": "+4"
    },
    # 6枠12番 テアオ (チリ/米国馬・サドラー厩舎 / 来日計測478kg)
    "テアオ": {
        "lastRaceWeight": None,
        "trainingWeight": 478,
        "trainingWeightDiff": None
    },
    # 7枠13番 アーバンシック (前走新潟記念 522kg ±0)
    "アーバンシック": {
        "lastRaceWeight": 522,
        "trainingWeight": 526,
        "trainingWeightDiff": "+4"
    },
    # 7枠14番 タガノデュード (前走天皇賞秋 498kg -10)
    "タガノデュード": {
        "lastRaceWeight": 498,
        "trainingWeight": 506,
        "trainingWeightDiff": "+8"
    },
    # 7枠15番 エキサイトバイオ (前走有馬記念 482kg +2)
    "エキサイトバイオ": {
        "lastRaceWeight": 482,
        "trainingWeight": 486,
        "trainingWeightDiff": "+4"
    },
    # 8枠16番 ダノンデサイル (前走天皇賞秋 516kg -4)
    "ダノンデサイル": {
        "lastRaceWeight": 516,
        "trainingWeight": 522,
        "trainingWeightDiff": "+6"
    },
    # 8枠17番 ゴリアット (仏国馬・グラファール厩舎 / 来日計測505kg -> 調教後504kg)
    "ゴリアット": {
        "lastRaceWeight": None,
        "trainingWeight": 504,
        "trainingWeightDiff": None
    },
    # 8枠18番 エシカルダイヤモンド (愛国馬・マリンズ厩舎 / 来日計測474kg)
    "エシカルダイヤモンド": {
        "lastRaceWeight": None,
        "trainingWeight": 474,
        "trainingWeightDiff": None
    }
}

def update_weights():
    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        pred_data = json.load(f)

    # 1. Update Race 19 starters
    if "races" in pred_data and "19" in pred_data["races"]:
        jc = pred_data["races"]["19"]
        for s in jc.get("starters", []):
            name = s.get("horseName")
            if name in JC_OFFICIAL_WEIGHTS:
                w = JC_OFFICIAL_WEIGHTS[name]
                s["trainingWeight"] = w["trainingWeight"]
                s["lastRaceWeight"] = w["lastRaceWeight"]
                s["trainingWeightDiff"] = w["trainingWeightDiff"]

    # 2. Update Top-level starters
    for s in pred_data.get("starters", []):
        name = s.get("horseName")
        if name in JC_OFFICIAL_WEIGHTS:
            w = JC_OFFICIAL_WEIGHTS[name]
            s["trainingWeight"] = w["trainingWeight"]
            s["lastRaceWeight"] = w["lastRaceWeight"]
            s["trainingWeightDiff"] = w["trainingWeightDiff"]

    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(pred_data, f, ensure_ascii=False, indent=2)

    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write("export const PREDICTION_DATA = " + json.dumps(pred_data, ensure_ascii=False, indent=2) + ";\n")

    print("Updated prediction_data.json and prediction_data.js with authentic post-training horse weights!")

if __name__ == "__main__":
    update_weights()
