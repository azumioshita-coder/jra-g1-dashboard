import json
import os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(APP_DIR, 'src')

ENTRIES_JSON = os.path.join(SRC_DIR, 'entries_data.json')
ENTRIES_JS = os.path.join(SRC_DIR, 'entries_data.js')
PRED_JSON = os.path.join(SRC_DIR, 'prediction_data.json')
PRED_JS = os.path.join(SRC_DIR, 'prediction_data.js')

GATE_DRAW = [
    {"gate": 1, "waku": 1, "horseName": "ヘデントール", "jockey": "T.マーカンド", "load": 58, "sexAge": "牡5", "stable": "木村哲也 (美浦)"},
    {"gate": 2, "waku": 1, "horseName": "コスモキュランダ", "jockey": "丹内祐次", "load": 58, "sexAge": "牡5", "stable": "加藤士津八 (美浦)"},
    {"gate": 3, "waku": 2, "horseName": "メイショウタバル", "jockey": "武豊", "load": 58, "sexAge": "牡5", "stable": "石橋守 (栗東)"},
    {"gate": 4, "waku": 2, "horseName": "クロワデュノール", "jockey": "C.デムーロ", "load": 58, "sexAge": "牡4", "stable": "斉藤崇史 (栗東)"},
    {"gate": 5, "waku": 3, "horseName": "シェイクユアハート", "jockey": "古川吉洋", "load": 58, "sexAge": "牡6", "stable": "宮徹 (栗東)"},
    {"gate": 6, "waku": 3, "horseName": "マスカレードボール", "jockey": "C.ルメール", "load": 58, "sexAge": "牡4", "stable": "手塚貴久 (美浦)"},
    {"gate": 7, "waku": 4, "horseName": "ファイアンクランツ", "jockey": "J.モレイラ", "load": 58, "sexAge": "牡4", "stable": "堀宣行 (美浦)"},
    {"gate": 8, "waku": 4, "horseName": "オンブズマン", "jockey": "W.ビュイック", "load": 58, "sexAge": "牡5", "stable": "J&T.ゴスデン (英)"},
    {"gate": 9, "waku": 5, "horseName": "カランダガン", "jockey": "M.バルザローナ", "load": 58, "sexAge": "セ5", "stable": "F.グラファール (仏)"},
    {"gate": 10, "waku": 5, "horseName": "ミニーホーク", "jockey": "R.ムーア", "load": 56, "sexAge": "牝4", "stable": "A.オブライエン (愛)"},
    {"gate": 11, "waku": 6, "horseName": "ヴェルテンベルク", "jockey": "横山典弘", "load": 58, "sexAge": "牡6", "stable": "宮本博 (栗東)"},
    {"gate": 12, "waku": 6, "horseName": "テアオ", "jockey": "L.トーレス", "load": 58, "sexAge": "牡4", "stable": "J.サドラー (米)"},
    {"gate": 13, "waku": 7, "horseName": "アーバンシック", "jockey": "A.プーシャン", "load": 58, "sexAge": "牡5", "stable": "武井亮 (美浦)"},
    {"gate": 14, "waku": 7, "horseName": "タガノデュード", "jockey": "M.デムーロ", "load": 58, "sexAge": "牡5", "stable": "宮徹 (栗東)"},
    {"gate": 15, "waku": 7, "horseName": "エキサイトバイオ", "jockey": "荻野極", "load": 58, "sexAge": "牡4", "stable": "今野貞一 (栗東)"},
    {"gate": 16, "waku": 8, "horseName": "ダノンデサイル", "jockey": "戸崎圭太", "load": 58, "sexAge": "牡5", "stable": "安田翔伍 (栗東)"},
    {"gate": 17, "waku": 8, "horseName": "ゴリアット", "jockey": "C.スミヨン", "load": 58, "sexAge": "セ6", "stable": "F.グラファール (仏)"},
    {"gate": 18, "waku": 8, "horseName": "エシカルダイヤモンド", "jockey": "坂井瑠星", "load": 58, "sexAge": "セ6", "stable": "W.マリンズ (愛)"}
]

GATE_MAP = {item["horseName"]: item for item in GATE_DRAW}

CONCERNS_UPDATE = {
    "ダノンデサイル": "大外8枠16番に入ったため、1コーナーまでのポジション取りと終始外々を回らされる距離ロス。",
    "ヘデントール": "最内1枠1番に入ったため、出遅れた際に包まれて後方に置かれるリスクと、超高速決着での時計勝負。",
    "ゴリアット": "外枠8枠17番からの発走。欧州のタフな重馬場で真価を発揮するタイプで、外を回る距離ロスと府中の超高速芝への適応力。"
}

def apply_gates():
    # 1. Update entries_data
    with open(ENTRIES_JSON, 'r', encoding='utf-8') as f:
        entries_data = json.load(f)

    entries_data["19"] = GATE_DRAW

    with open(ENTRIES_JSON, 'w', encoding='utf-8') as f:
        json.dump(entries_data, f, ensure_ascii=False, indent=2)
    with open(ENTRIES_JS, 'w', encoding='utf-8') as f:
        f.write("export const ENTRIES_DATA = " + json.dumps(entries_data, ensure_ascii=False, indent=2) + ";\n")

    print("Updated entries_data.json and entries_data.js with confirmed gate draw!")

    # 2. Update prediction_data
    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        pred_data = json.load(f)

    # Update Race 19 entryStatus
    if "races" in pred_data and "19" in pred_data["races"]:
        jc = pred_data["races"]["19"]
        jc["entryStatus"] = "gate_confirmed"

        # Update starters
        starters = jc.get("starters", [])
        for s in starters:
            name = s.get("horseName")
            if name in GATE_MAP:
                gm = GATE_MAP[name]
                s["waku"] = gm["waku"]
                s["gate"] = gm["gate"]
                s["jockey"] = gm["jockey"]
                s["load"] = gm["load"]
                s["stable"] = gm["stable"]
                s["sexAge"] = gm["sexAge"]

        # Sort starters by gate
        jc["starters"] = sorted(starters, key=lambda x: (x.get("gate") or 99))

        # Update contenderRanking
        ranking = jc.get("contenderRanking", [])
        for c in ranking:
            name = c.get("horseName")
            if name in GATE_MAP:
                gm = GATE_MAP[name]
                c["waku"] = gm["waku"]
                c["gate"] = gm["gate"]
                c["jockey"] = gm["jockey"]
                c["load"] = gm["load"]
                c["stable"] = gm["stable"]
                c["sexAge"] = gm["sexAge"]
            if name in CONCERNS_UPDATE:
                c["concerns"] = CONCERNS_UPDATE[name]

    # Update top-level if activeRaceId == 19
    if pred_data.get("activeRaceId") == "19" or pred_data.get("activeRaceId") == 19:
        pred_data["entryStatus"] = "gate_confirmed"
        pred_data["starters"] = pred_data["races"]["19"]["starters"]
        pred_data["contenderRanking"] = pred_data["races"]["19"]["contenderRanking"]

    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(pred_data, f, ensure_ascii=False, indent=2)
    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write("export const PREDICTION_DATA = " + json.dumps(pred_data, ensure_ascii=False, indent=2) + ";\n")

    print("Updated prediction_data.json and prediction_data.js with confirmed gate draw!")

if __name__ == "__main__":
    apply_gates()
