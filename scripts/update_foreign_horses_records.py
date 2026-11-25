import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
PRED_JSON = os.path.join(BASE_DIR, 'src', 'prediction_data.json')
PRED_JS = os.path.join(BASE_DIR, 'src', 'prediction_data.js')

def update_foreign_horses():
    with open(HORSE_JSON, 'r', encoding='utf-8') as f:
        hd = json.load(f)

    # 1. オーギュストロダン (Auguste Rodin)
    if 'オーギュストロダン' in hd:
        h = hd['オーギュストロダン']
        h['record'] = '17戦8勝 [8-3-0-6]'
        h['earnings'] = '14億2,450万円 (換算)'
        # prepend Japan Cup 2024 if not present
        if not any(r.get('date') == '2024-11-24' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2024-11-24",
                "venue": "5東京8",
                "weather": "晴",
                "raceNum": "12",
                "race": "ジャパンC(GI)",
                "starters": "14",
                "bracket": "6",
                "gate": "8",
                "odds": "4.5",
                "pop": "2",
                "rank": "8",
                "jockey": "R.ムーア",
                "load": "58",
                "course": "芝2400",
                "track": "良",
                "time": "2:26.1",
                "margin": "0.6",
                "passing": "6-6-6-6",
                "pace": "37.6-34.1",
                "agari": "34.1",
                "weight": "478(-)",
                "rival": "ドウデュース"
            })
        print("Updated オーギュストロダン")

    # 2. ファンタスティックムーン (Fantastic Moon)
    if 'ファンタスティックムーン' in hd:
        h = hd['ファンタスティックムーン']
        h['record'] = '16戦7勝 [7-3-1-5]'
        if not any(r.get('date') == '2024-11-24' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2024-11-24",
                "venue": "5東京8",
                "weather": "晴",
                "raceNum": "12",
                "race": "ジャパンC(GI)",
                "starters": "14",
                "bracket": "7",
                "gate": "11",
                "odds": "29.8",
                "pop": "8",
                "rank": "11",
                "jockey": "R.ピーヒュレク",
                "load": "58",
                "course": "芝2400",
                "track": "良",
                "time": "2:26.6",
                "margin": "1.1",
                "passing": "13-13-13-13",
                "pace": "37.6-34.1",
                "agari": "34.1",
                "weight": "460(-)",
                "rival": "ドウデュース"
            })
        print("Updated ファンタスティックムーン")

    # 3. チャリン (Charyn)
    if 'チャリン' in hd:
        h = hd['チャリン']
        h['record'] = '20戦7勝 [7-4-4-5]'
        if not any(r.get('date') == '2024-11-17' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2024-11-17",
                "venue": "6京都6",
                "weather": "晴",
                "raceNum": "11",
                "race": "マイルCS(GI)",
                "starters": "17",
                "bracket": "6",
                "gate": "11",
                "odds": "6.0",
                "pop": "3",
                "rank": "5",
                "jockey": "R.ムーア",
                "load": "58",
                "course": "芝1600",
                "track": "良",
                "time": "1:32.4",
                "margin": "0.4",
                "passing": "15-15",
                "pace": "33.8-34.2",
                "agari": "33.5",
                "weight": "494(-)",
                "rival": "ソウルラッシュ"
            })
        print("Updated チャリン")

    # 4. レモンポップ (Lemon Pop)
    if 'レモンポップ' in hd:
        h = hd['レモンポップ']
        h['record'] = '18戦12勝 [12-3-0-3]'
        h['earnings'] = '6億8,950万円'
        if "24'チャンピオンズC(G1)" not in h.get('titles', []):
            h['titles'].insert(0, "24'チャンピオンズC(G1)")
        if not any(r.get('date') == '2024-12-01' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2024-12-01",
                "venue": "4中京2",
                "weather": "晴",
                "raceNum": "11",
                "race": "チャンピオンズC(GI)",
                "starters": "16",
                "bracket": "1",
                "gate": "2",
                "odds": "2.4",
                "pop": "1",
                "rank": "1",
                "jockey": "坂井瑠星",
                "load": "58",
                "course": "ダ1800",
                "track": "良",
                "time": "1:50.1",
                "margin": "-0.0",
                "passing": "1-1-1-1",
                "pace": "36.4-36.8",
                "agari": "36.8",
                "weight": "514(0)",
                "rival": "ウィルソンテソーロ"
            })
        print("Updated レモンポップ")

    # 5. ゴリアット (Goliath)
    if 'ゴリアット' in hd:
        h = hd['ゴリアット']
        h['record'] = '24戦11勝 [11-4-2-7]'
        if "26'オイロパ賞(G1)" not in h.get('titles', []):
            h['titles'].insert(0, "26'オイロパ賞(G1)")
        if not any(r.get('date') == '2026-09-27' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-09-27",
                "venue": "ケルン",
                "weather": "晴",
                "raceNum": "6",
                "race": "オイロパ賞(GI)",
                "starters": "8",
                "bracket": "",
                "gate": "4",
                "odds": "1.9",
                "pop": "1",
                "rank": "1",
                "jockey": "C.スミヨン",
                "load": "59",
                "course": "芝2400",
                "track": "良",
                "time": "2:28.40",
                "margin": "-0.2",
                "passing": "2-2-1",
                "pace": "",
                "agari": "",
                "weight": "計不",
                "rival": "ドバイオナー"
            })
        print("Updated ゴリアット")

    # 6. カランダガン (Calandagan)
    if 'カランダガン' in hd:
        h = hd['カランダガン']
        h['record'] = '20戦10勝 [10-8-1-1]'
        if not any(r.get('date') == '2026-10-17' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-10-17",
                "venue": "アスコット",
                "weather": "稍",
                "raceNum": "4",
                "race": "英チャンピオンS(GI)",
                "starters": "10",
                "bracket": "",
                "gate": "6",
                "odds": "2.6",
                "pop": "1",
                "rank": "2",
                "jockey": "M.バルザローナ",
                "load": "58.5",
                "course": "芝1990",
                "track": "稍",
                "time": "2:03.1",
                "margin": "0.3",
                "passing": "7-5-2",
                "pace": "",
                "agari": "",
                "weight": "計不",
                "rival": "オンブズマン"
            })
        print("Updated カランダガン")

    # 7. オンブズマン (Ombudsman)
    if 'オンブズマン' in hd:
        h = hd['オンブズマン']
        h['record'] = '14戦10勝 [10-3-0-1]'
        if "26'英チャンピオンS(G1)" not in h.get('titles', []):
            h['titles'].insert(0, "26'英チャンピオンS(G1)")
        if not any(r.get('date') == '2026-10-17' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-10-17",
                "venue": "アスコット",
                "weather": "稍",
                "raceNum": "4",
                "race": "英チャンピオンS(GI)",
                "starters": "10",
                "bracket": "",
                "gate": "3",
                "odds": "3.5",
                "pop": "2",
                "rank": "1",
                "jockey": "W.ビュイック",
                "load": "58.5",
                "course": "芝1990",
                "track": "稍",
                "time": "2:02.8",
                "margin": "-0.3",
                "passing": "4-4-1",
                "pace": "",
                "agari": "",
                "weight": "計不",
                "rival": "カランダガン"
            })
        print("Updated オンブズマン")

    # 8. ミニーホーク (Minnie Hauk)
    if 'ミニーホーク' in hd:
        h = hd['ミニーホーク']
        h['record'] = '16戦8勝 [8-3-1-4]'
        if "26'英チャンピオンズF&MS(G1)" not in h.get('titles', []):
            h['titles'].insert(0, "26'英チャンピオンズF&MS(G1)")
        if not any(r.get('date') == '2026-10-17' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-10-17",
                "venue": "アスコット",
                "weather": "稍",
                "raceNum": "3",
                "race": "英チャンピオンズF&M(GI)",
                "starters": "12",
                "bracket": "",
                "gate": "5",
                "odds": "6.0",
                "pop": "3",
                "rank": "1",
                "jockey": "R.ムーア",
                "load": "57.5",
                "course": "芝2390",
                "track": "稍",
                "time": "2:31.2",
                "margin": "-0.3",
                "passing": "3-3-1",
                "pace": "",
                "agari": "",
                "weight": "計不",
                "rival": "ビリーブド"
            })
        print("Updated ミニーホーク")

    # 9. エシカルダイヤモンド (Ethical Diamond)
    if 'エシカルダイヤモンド' in hd:
        h = hd['エシカルダイヤモンド']
        h['record'] = '15戦5勝 [5-2-0-8]'
        if not any(r.get('date') == '2026-11-07' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-11-07",
                "venue": "デルマー",
                "weather": "晴",
                "raceNum": "9",
                "race": "BCターフ(GI)",
                "starters": "12",
                "bracket": "",
                "gate": "8",
                "odds": "16.5",
                "pop": "6",
                "rank": "4",
                "jockey": "R.ムーア",
                "load": "57.5",
                "course": "芝2400",
                "track": "良",
                "time": "2:24.8",
                "margin": "0.4",
                "passing": "9-8-5-4",
                "pace": "",
                "agari": "",
                "weight": "計不",
                "rival": "レベルスロマンス"
            })
        print("Updated エシカルダイヤモンド")

    # 10. テアオ (Teao)
    if 'テアオ' in hd:
        h = hd['テアオ']
        h['record'] = '10戦7勝 [7-2-1-0]'
        if "26'ラテンアメリカ大賞(G1)" not in h.get('titles', []):
            h['titles'].insert(0, "26'ラテンアメリカ大賞(G1)")
        if not any(r.get('date') == '2026-04-14' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-04-14",
                "venue": "モンテリコ",
                "weather": "晴",
                "raceNum": "10",
                "race": "ラテンアメリカ大賞(G1)",
                "starters": "14",
                "bracket": "3",
                "gate": "4",
                "odds": "2.2",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "57",
                "course": "芝2000",
                "track": "良",
                "time": "1:59.4",
                "margin": "-0.6",
                "passing": "3-3-1",
                "pace": "35.4-35.0",
                "agari": "34.6",
                "weight": "490(+2)",
                "rival": "ドンフィエロ"
            })
        print("Updated テアオ")

    # 11. エルデナリ (Erdenali)
    if 'エルデナリ' in hd:
        h = hd['エルデナリ']
        h['record'] = '7戦6勝 [6-0-1-0]'
        if "26'マイルCS(G1)" not in h.get('titles', []):
            h['titles'].insert(0, "26'マイルCS(G1)")
        if not any(r.get('date') == '2026-11-22' for r in h.get('career', [])):
            h['career'].insert(0, {
                "date": "2026-11-22",
                "venue": "6京都6",
                "weather": "晴",
                "raceNum": "11",
                "race": "マイルCS(GI)",
                "starters": "18",
                "bracket": "1",
                "gate": "1",
                "odds": "8.5",
                "pop": "4",
                "rank": "1",
                "jockey": "M.バルザローナ",
                "load": "57",
                "course": "芝1600",
                "track": "良",
                "time": "1:31.9",
                "margin": "-0.1",
                "passing": "5-4",
                "pace": "34.1-33.8",
                "agari": "33.6",
                "weight": "488(-)",
                "rival": "エンブロイダリー"
            })
        print("Updated エルデナリ")

    # Save to JSON and JS
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(hd, f, ensure_ascii=False, indent=2)
    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(hd, ensure_ascii=False, indent=2) + ";\n")

    # Update prediction_data contender ranking comments
    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        pd = json.load(f)

    foreign_updates = {
        "ゴリアット": {
            "comment": "前走の独G1オイロパ賞を快勝し充実一途。英キングジョージ覇者の地力は本物で、名手C.スミヨン騎手との名コンビで東京芝2400m攻略に挑む。",
            "strengths": "前走の独G1オイロパ賞を快勝し充実一途。英キングジョージ覇者の地力は本物で、名手C.スミヨン騎手との名コンビで東京芝2400m攻略に挑む。"
        },
        "カランダガン": {
            "comment": "前走の英チャンピオンS(GI)でもオンブズマンの2着と欧州最高峰で好走。前年のジャパンカップを衝撃的な走りで制したディフェンディングチャンピオンでコース適性は証明済み。",
            "strengths": "前走の英チャンピオンS(GI)でもオンブズマンの2着と欧州最高峰で好走。前年のジャパンカップを衝撃的な走りで制したディフェンディングチャンピオンでコース適性は証明済み。"
        },
        "オンブズマン": {
            "comment": "前走アスコットの英チャンピオンS(GI)でカランダガンを撃破して戴冠した欧州最強中距離馬。名門ゴスデン厩舎の看板を背負い、主戦W.ビュイック騎手の手綱でジャパンカップ初制覇を狙う。",
            "strengths": "前走アスコットの英チャンピオンS(GI)でカランダガンを撃破して戴冠した欧州最強中距離馬。名門ゴスデン厩舎の看板を背負い、主戦W.ビュイック騎手の手綱でジャパンカップ初制覇を狙う。"
        },
        "ミニーホーク": {
            "comment": "前走の英チャンピオンズF&Mステークス(GI)を鮮やかに差し切ってG1制覇。名将A.オブライエン調教師×名手R.ムーア騎手の黄金タッグで府中の直線を強襲する。",
            "strengths": "前走の英チャンピオンズF&Mステークス(GI)を鮮やかに差し切ってG1制覇。名将A.オブライエン調教師×名手R.ムーア騎手の黄金タッグで府中の直線を強襲する。"
        },
        "エシカルダイヤモンド": {
            "comment": "前走のBCターフ(GI)で4着と世界レベル相手に善戦。愛の名匠W.マリンズ厩舎が送り込むスタミナ自慢で、坂井瑠星騎手の手綱捌きに注目。",
            "strengths": "前走のBCターフ(GI)で4着と世界レベル相手に善戦。愛の名匠W.マリンズ厩舎が送り込むスタミナ自慢で、坂井瑠星騎手の手綱捌きに注目。"
        },
        "テアオ": {
            "comment": "南米G1・5勝に加え、春にはペルーのラテンアメリカ大賞(G1)を制覇したチリ年度代表馬。米J.サドラー厩舎を経て名手L.トーレス騎手とともに未知の魅力十分。",
            "strengths": "南米G1・5勝に加え、春にはペルーのラテンアメリカ大賞(G1)を制覇したチリ年度代表馬。米J.サドラー厩舎を経て名手L.トーレス騎手とともに未知の魅力十分。"
        }
    }

    # Update in pd['races']['19']['contenderRanking'] and pd['contenderRanking']
    for root_dict in [pd.get('races', {}).get('19', {}), pd]:
        for cr in root_dict.get('contenderRanking', []):
            name = cr.get('horseName')
            if name in foreign_updates:
                cr['comment'] = foreign_updates[name]['comment']
                cr['strengths'] = foreign_updates[name]['strengths']

    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(pd, f, ensure_ascii=False, indent=2)
    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write("export const PREDICTION_DATA = " + json.dumps(pd, ensure_ascii=False, indent=2) + ";\n")

    print("\nAll foreign horses successfully updated to the absolute latest authentic race results!")

if __name__ == '__main__':
    update_foreign_horses()
