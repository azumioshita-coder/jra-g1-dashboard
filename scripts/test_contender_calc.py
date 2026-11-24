import json

with open('src/prediction_data.json') as f:
    pred = json.load(f)

with open('src/horse_data.json') as f:
    horse_db = json.load(f)

starters = pred['races']['19']['starters']

# JOCKEY_BASE_SCORES
JOCKEY_SCORES = {
    'ルメール': 98, 'C.ルメール': 98, '川田': 97, '川田将雅': 97,
    '武豊': 96, 'C.デムーロ': 96, 'Ｃデムー': 96, 'モレイラ': 97, 'J.モレイラ': 97,
    'ムーア': 96, 'レーン': 96, 'スミヨン': 96, 'プーシャ': 93, 'A.プーシャン': 93,
    '戸崎': 95, '戸崎圭太': 95, '坂井': 94, '坂井瑠星': 94, '松山': 94, '松山弘平': 94,
    'バルザローナ': 95, 'M.バルザローナ': 95, '横山武': 93, '横山武史': 93,
    '岩田望': 92, '岩田望来': 92, '西村淳': 91, '西村淳也': 91, '菅原明': 91, '菅原明良': 91,
    'ビュイック': 95, 'W.ビュイック': 95, 'マーカンド': 94, 'T.マーカンド': 94,
    '横山典': 91, '横山典弘': 91, '田口': 88, '田口貫太': 88, '三浦': 89, '三浦皇成': 89,
    '荻野極': 86, '古川吉': 85
}

TRAIN_SCORES = {'S': 97, 'A+': 95, 'A': 92, 'B+': 88, 'B': 84, 'C': 78}

def compute_contender_ranking(race_id, starters_list, horse_db_data):
    items = []
    for s in starters_list:
        hname = s['horseName']
        h_info = horse_db_data.get(hname, {})

        # 1. Training Score (20%)
        tr_grade = s.get('trainingGrade') or h_info.get('trainingGrade', 'B')
        tr_base = TRAIN_SCORES.get(tr_grade, 85)

        # Weight adjustment
        wt_diff = s.get('weightDiff')
        has_confirmed_wt = s.get('confirmedWeight') is not None
        if wt_diff is not None:
            try:
                diff_n = int(wt_diff)
                if 2 <= diff_n <= 4:
                    tr_base += 2.0  # ideal muscle gain
                elif -2 <= diff_n <= 1:
                    tr_base += 1.0  # steady
                elif diff_n >= 10:
                    tr_base -= 3.0  # too heavy
                elif diff_n <= -8:
                    tr_base -= 3.0  # lost weight
                elif 6 <= diff_n <= 8:
                    tr_base -= 1.0
            except ValueError:
                pass
        elif s.get('trainingWeightDiff'):
            try:
                diff_n = int(s['trainingWeightDiff'])
                if 2 <= diff_n <= 4:
                    tr_base += 1.5
                elif -2 <= diff_n <= 1:
                    tr_base += 1.0
            except ValueError:
                pass

        ttime = s.get('trainingTime', '')
        if any(f in ttime for f in ['11.0', '11.1', '11.2']):
            tr_base += 1.5
        elif any(f in ttime for f in ['11.3', '11.4']):
            tr_base += 0.5
        
        tr_score = min(99, max(70, round(tr_base)))

        # 2. Jockey Score (20%)
        j_name = s.get('jockey', '')
        j_base = 86
        for k, v in JOCKEY_SCORES.items():
            if k in j_name:
                j_base = v
                break
        
        load_val = float(s.get('load', 58))
        if load_val <= 54:
            j_base += 3.2
        elif load_val <= 55:
            j_base += 2.4
        elif load_val <= 56:
            j_base += 1.6
        elif load_val <= 57:
            j_base += 0.8
        
        j_score = min(99, max(70, round(j_base)))

        # 3. Course Score & Gate Bias (15%)
        c_base = 90
        waku = s.get('waku')
        gate = s.get('gate')
        has_gate = gate is not None and waku is not None

        if has_gate:
            # Tokyo 2400m gate bias
            if waku == 1:
                c_base += 3.5  # 1枠の絶大イン経済コース有利
            elif waku == 2:
                c_base += 2.5
            elif waku in [3, 4]:
                c_base += 1.2
            elif waku in [5, 6]:
                c_base += 0.0
            elif waku == 7:
                c_base -= 1.5
            elif waku == 8:
                c_base -= 3.0  # 大外枠不利

        c_score = min(99, max(70, round(c_base)))

        # 4. Distance Score (15%)
        d_base = 90
        # 5. Prev Race Score (15%)
        p_base = 88
        odds_f = float(s.get('odds', 99) or 99)
        if odds_f <= 3.5:
            p_base, d_base = 96, 96
        elif odds_f <= 7.5:
            p_base, d_base = 94, 94
        elif odds_f <= 15.0:
            p_base, d_base = 91, 92
        elif odds_f <= 35.0:
            p_base, d_base = 88, 88
        else:
            p_base, d_base = 84, 84
        
        # 6. Pedigree Score (15%)
        ped_base = 89
        father = s.get('father', '')
        if father in ['スワーヴリチャード', 'キズナ', 'エピファネイア', 'ハーツクライ', 'ドゥラメンテ', 'ディープインパクト', 'Kingman', 'Dubawi']:
            ped_base = 94
        elif father in ['キタサンブラック', 'モーリス', 'ロードカナロア', 'ルーラーシップ']:
            ped_base = 92

        # Composite
        comp = round(
            tr_score * 0.20 +
            j_score * 0.20 +
            c_score * 0.15 +
            d_base * 0.15 +
            p_base * 0.15 +
            ped_base * 0.15,
            1
        )

        # Dynamic strengths & concerns text
        str_parts = []
        if has_gate:
            if waku in [1, 2]:
                str_parts.append(f"【好枠{waku}枠{gate}番】最内経済コースをロスなく立ち回れる絶好条件。")
            elif waku in [3, 4]:
                str_parts.append(f"【好位自在の{waku}枠{gate}番】馬群を見ながらスムーズにポジションを取れる枠順。")
        
        if has_confirmed_wt:
            diff_str = f"({wt_diff}kg)" if wt_diff else ""
            str_parts.append(f"【当日馬体重{s['confirmedWeight']}kg{diff_str}】仕上がり良好。")
        elif s.get('trainingGrade') == 'S':
            str_parts.append(f"【調教S・抜けた動き】{s.get('trainingComment', '')}")
        else:
            str_parts.append(s.get('trainingComment', '順調な仕上がり。'))

        con_parts = []
        if has_gate and waku in [7, 8]:
            con_parts.append(f"外枠{waku}枠{gate}番から終始外々を回らされる距離ロス。")
        if wt_diff and int(wt_diff) >= 10:
            con_parts.append(f"馬体重+{wt_diff}kgとやや太め残りの懸念。")
        elif wt_diff and int(wt_diff) <= -8:
            con_parts.append(f"馬体重{wt_diff}kgと馬体減り・輸送の影響。")
        if not con_parts:
            con_parts.append("府中の長い直線での瞬発力勝負の隊列。")

        items.append({
            'gate': gate,
            'waku': waku,
            'horseName': hname,
            'jockey': s.get('jockey', ''),
            'load': s.get('load', 58),
            'sexAge': s.get('sexAge', ''),
            'stable': s.get('stable', ''),
            'odds': s.get('odds', ''),
            'pop': s.get('pop'),
            'scores': {
                'training': tr_score,
                'jockey': j_score,
                'course': c_score,
                'distance': d_base,
                'prevRace': p_base,
                'pedigree': ped_base
            },
            'compositeScore': comp,
            'strengths': " ".join(str_parts),
            'concerns': " ".join(con_parts)
        })

    # Sort by compositeScore descending
    items.sort(key=lambda x: (x['compositeScore'], -(float(x['odds']) if x['odds'] else 999)), reverse=True)

    # Assign ranks and marks
    for idx, item in enumerate(items):
        item['rank'] = idx + 1
        comp = item['compositeScore']
        if idx == 0:
            item['recommendedMark'] = '◎'
            item['grade'] = 'SS' if comp >= 95 else 'S+'
            item['gradeTag'] = '本命最有力'
        elif idx == 1:
            item['recommendedMark'] = '○'
            item['grade'] = 'S+' if comp >= 94 else 'S'
            item['gradeTag'] = '対抗筆頭'
        elif idx == 2:
            item['recommendedMark'] = '▲'
            item['grade'] = 'S'
            item['gradeTag'] = '単穴警戒'
        elif idx in [3, 4]:
            item['recommendedMark'] = '△'
            item['grade'] = 'S-' if comp >= 92 else 'A+'
            item['gradeTag'] = '連下候補'
        elif idx == 5:
            item['recommendedMark'] = '☆'
            item['grade'] = 'A+'
            item['gradeTag'] = '大穴警戒'
        else:
            item['recommendedMark'] = '-'
            item['grade'] = 'A' if comp >= 89 else ('B+' if comp >= 86 else 'B')
            item['gradeTag'] = '伏兵一考' if comp >= 87 else '連下候補'

    return items

ranked = compute_contender_ranking('19', starters, horse_db)
print("=== RANKING BEFORE GATE DRAW ===")
for r in ranked[:5]:
    print(f"{r['rank']}位: {r['horseName']} ({r['recommendedMark']}) {r['compositeScore']}点 [{r['grade']} {r['gradeTag']}] コース:{r['scores']['course']} 調教:{r['scores']['training']}")

# Now simulate: What if クロワデュノール draws gate 1 (waku 1) and gains ideal +2kg, while someone else draws gate 18 (waku 8)?
print("\n=== SIMULATE: AFTER GATE 1 & WEIGHT +2kg FOR クロワデュノール ===")
simulated_starters = [dict(s) for s in starters]
for s in simulated_starters:
    if s['horseName'] == 'クロワデュノール':
        s['gate'] = 1
        s['waku'] = 1
        s['confirmedWeight'] = 524
        s['weightDiff'] = '+2'
    elif s['horseName'] == 'マスカレードボール':
        s['gate'] = 18
        s['waku'] = 8

sim_ranked = compute_contender_ranking('19', simulated_starters, horse_db)
for r in sim_ranked[:5]:
    print(f"{r['rank']}位: {r['horseName']} ({r['recommendedMark']}) {r['compositeScore']}点 [{r['grade']} {r['gradeTag']}] コース:{r['scores']['course']} 調教:{r['scores']['training']}")
    if r['horseName'] in ['クロワデュノール', 'マスカレードボール']:
        print(f"  -> Strengths: {r['strengths'][:60]}...")
        print(f"  -> Concerns: {r['concerns'][:60]}...")
