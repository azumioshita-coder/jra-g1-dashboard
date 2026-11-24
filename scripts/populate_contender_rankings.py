#!/usr/bin/env python3
import os
import json

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_JSON = os.path.join(APP_DIR, 'src', 'prediction_data.json')
PRED_JS = os.path.join(APP_DIR, 'src', 'prediction_data.js')

with open(PRED_JSON, 'r', encoding='utf-8') as f:
    pred_data = json.load(f)

# Race 16 (天皇賞・秋) Contender Ranking
r16_starters = pred_data.get('races', {}).get('16', {}).get('starters', [])
if r16_starters:
    # Sort by odds / pre-race expectations
    # 7番 マスカレードボール(1), 1番 クロワデュノール(2), 3番 レガレイラ(3), 17番 ダノンデサイル(4), 9番 ホウオウビスケッツ(5), 10番 ネブラディスク(6)...
    scores_16 = {
        'マスカレードボール': {'rank': 1, 'mark': '◎', 'score': 96.4, 'grade': 'SS', 'tag': '本命最有力',
                            's': {'training': 98, 'jockey': 98, 'course': 95, 'distance': 96, 'prevRace': 96, 'pedigree': 95},
                            'str': '【調教S・府中の申し子】美浦Wでラスト11.1秒。直線の長い東京2000mはベスト舞台。C.ルメール騎手の手綱で死角なし。',
                            'con': '多頭数のインで包まれた際のスムーズな進路確保。'},
        'クロワデュノール': {'rank': 2, 'mark': '○', 'score': 95.8, 'grade': 'S+', 'tag': '逆転筆頭',
                           's': {'training': 97, 'jockey': 96, 'course': 94, 'distance': 96, 'prevRace': 95, 'pedigree': 97},
                           'str': '【無敗の怪物】春の実績とCWでラスト11.2秒の超抜の動き。最内1番枠とC.デムーロ騎手で盤石。',
                           'con': '古馬G1のハイペースに初めて対峙する際の精神面。'},
        'レガレイラ': {'rank': 3, 'mark': '▲', 'score': 94.7, 'grade': 'S', 'tag': '単穴警戒',
                     's': {'training': 94, 'jockey': 94, 'course': 96, 'distance': 95, 'prevRace': 94, 'pedigree': 95},
                     'str': '【有馬記念覇者の決め手】東京2000mは直線の決め手が最大限活きる舞台。鋭い末脚はメンバー屈指。',
                     'con': '後方待機策での展開待ちになるリスク。'},
        'ダノンデサイル': {'rank': 4, 'mark': '△', 'score': 93.9, 'grade': 'S', 'tag': 'ダービー馬の威厳',
                         's': {'training': 93, 'jockey': 95, 'course': 95, 'distance': 94, 'prevRace': 93, 'pedigree': 93},
                         'str': '【ダービー馬の底力】東京2400mで見せた圧巻の二枚腰。戸崎圭太騎手とのコンビで2000mでも先行力を活かせる。',
                         'con': '大外8枠17番からのポジション取りと距離短縮への対応。'},
        'ホウオウビスケッツ': {'rank': 5, 'mark': '△', 'score': 92.5, 'grade': 'A+', 'tag': '先行粘り腰',
                           's': {'training': 92, 'jockey': 93, 'course': 92, 'distance': 93, 'prevRace': 93, 'pedigree': 91},
                           'str': '【重賞連勝の充実期】毎日王冠好走の勢いそのまま。岩田康誠騎手の絶妙なペース配分。',
                           'con': '同型の逃げ馬とのハナ争い。'},
        'ネブラディスク': {'rank': 6, 'mark': '☆', 'score': 91.8, 'grade': 'A+', 'tag': '川田の勝負手',
                         's': {'training': 91, 'jockey': 96, 'course': 90, 'distance': 92, 'prevRace': 91, 'pedigree': 91},
                         'str': '【本格化の兆し】中団好位から鋭く脚を使える成長力。川田将雅騎手の一撃に警戒。',
                         'con': '東京芝2000mの直線の坂での持久力。'},
        'セイウンハーデス': {'rank': 7, 'mark': '-', 'score': 90.5, 'grade': 'A', 'tag': '伏兵一考',
                           's': {'training': 90, 'jockey': 90, 'course': 90, 'distance': 91, 'prevRace': 91, 'pedigree': 90},
                           'str': '先行力としぶとさが武器。', 'con': '瞬発力勝負になると見劣り。'},
        'コスモキュランダ': {'rank': 8, 'mark': '-', 'score': 89.8, 'grade': 'A', 'tag': '捲り警戒',
                           's': {'training': 89, 'jockey': 89, 'course': 90, 'distance': 91, 'prevRace': 90, 'pedigree': 90},
                           'str': '皐月賞2着の実績。ロングスパートが持ち味。', 'con': '東京の瞬発力勝負への適性。'},
        'ジュンブロッサム': {'rank': 9, 'mark': '-', 'score': 89.2, 'grade': 'A', 'tag': '末脚一撃',
                           's': {'training': 90, 'jockey': 88, 'course': 89, 'distance': 88, 'prevRace': 91, 'pedigree': 89},
                           'str': '富士S勝ちの切れ味。', 'con': '2000mへの距離延長。'},
        'エルトンバローズ': {'rank': 10, 'mark': '-', 'score': 88.5, 'grade': 'B+', 'tag': 'イン差し警戒',
                           's': {'training': 89, 'jockey': 88, 'course': 88, 'distance': 88, 'prevRace': 88, 'pedigree': 89},
                           'str': '内枠を引いて好位インで運べる利点。', 'con': 'G1のトップスピード勝負でのパンチ不足。'},
        'レディネス': {'rank': 11, 'mark': '-', 'score': 87.8, 'grade': 'B+', 'tag': '展開待ち',
                     's': {'training': 87, 'jockey': 90, 'course': 87, 'distance': 88, 'prevRace': 87, 'pedigree': 88},
                     'str': '横山典弘騎手の一発。', 'con': '相手関係の大幅強化。'},
        'リアライズシリウス': {'rank': 12, 'mark': '-', 'score': 87.0, 'grade': 'B+', 'tag': '穴狙い',
                           's': {'training': 86, 'jockey': 88, 'course': 87, 'distance': 87, 'prevRace': 87, 'pedigree': 87},
                           'str': 'コース実績あり。', 'con': '決め手比べで見劣り。'},
        'シャンパンカラー': {'rank': 13, 'mark': '-', 'score': 86.2, 'grade': 'B', 'tag': 'マイルG1馬',
                           's': {'training': 86, 'jockey': 88, 'course': 88, 'distance': 84, 'prevRace': 85, 'pedigree': 86},
                           'str': 'NHKマイルC覇者。', 'con': '2000mの距離と近走の不振。'},
        'タガノデュード': {'rank': 14, 'mark': '-', 'score': 85.5, 'grade': 'B', 'tag': '大穴伏兵',
                         's': {'training': 85, 'jockey': 89, 'course': 85, 'distance': 86, 'prevRace': 85, 'pedigree': 85},
                         'str': 'M.デムーロ騎手の手綱。', 'con': '重賞での実績不足。'},
        'サクラファレル': {'rank': 15, 'mark': '-', 'score': 84.8, 'grade': 'B', 'tag': '大穴伏兵',
                         's': {'training': 85, 'jockey': 86, 'course': 85, 'distance': 85, 'prevRace': 84, 'pedigree': 85},
                         'str': '若手の佐々木大輔騎手。', 'con': '力不足否めず。'},
        'シェイクユアハート': {'rank': 16, 'mark': '-', 'score': 84.0, 'grade': 'B', 'tag': '大穴伏兵',
                           's': {'training': 84, 'jockey': 85, 'course': 84, 'distance': 84, 'prevRace': 84, 'pedigree': 83},
                           'str': 'ベテラン古川吉洋騎手。', 'con': 'スピード指数で見劣り。'},
        'ジョバンニ': {'rank': 17, 'mark': '-', 'score': 83.0, 'grade': 'B', 'tag': '大穴伏兵',
                     's': {'training': 83, 'jockey': 87, 'course': 83, 'distance': 83, 'prevRace': 82, 'pedigree': 82},
                     'str': '松山弘平騎手。', 'con': 'G1では厳しい。'}
    }

    cr16 = []
    for s in r16_starters:
        hname = s['horseName']
        info = scores_16.get(hname, {'rank': 99, 'mark': '-', 'score': 80.0, 'grade': 'B', 'tag': '-',
                                     's': {'training': 80, 'jockey': 80, 'course': 80, 'distance': 80, 'prevRace': 80, 'pedigree': 80},
                                     'str': '-', 'con': '-'})
        cr16.append({
            'gate': s['gate'],
            'waku': s['waku'],
            'horseName': hname,
            'jockey': s['jockey'],
            'load': s['load'],
            'sexAge': s['sexAge'],
            'stable': s['stable'],
            'odds': s['odds'],
            'pop': s['pop'],
            'grade': info['grade'],
            'gradeTag': info['tag'],
            'recommendedMark': info['mark'],
            'scores': info['s'],
            'strengths': info['str'],
            'concerns': info['con'],
            'compositeScore': info['score'],
            'rank': info['rank']
        })
    cr16.sort(key=lambda x: x['rank'])
    pred_data['races']['16']['contenderRanking'] = cr16
    print(f"Added contenderRanking for Race 16 ({len(cr16)} horses).")

# Race 17 (エリザベス女王杯) Contender Ranking
r17_starters = pred_data.get('races', {}).get('17', {}).get('starters', [])
if r17_starters:
    scores_17 = {
        'カムニャック': {'rank': 1, 'mark': '◎', 'score': 96.2, 'grade': 'SS', 'tag': '本命最有力',
                       's': {'training': 97, 'jockey': 98, 'course': 95, 'distance': 96, 'prevRace': 97, 'pedigree': 94},
                       'str': '【前哨戦圧勝・川田渾身】アイルランドTを圧巻の強さで制覇。京都2200mの持続力勝負に完璧にマッチ。',
                       'con': '直線の平坦下り坂での仕掛けのタイミング。'},
        'ステレンボッシュ': {'rank': 2, 'mark': '○', 'score': 95.1, 'grade': 'S+', 'tag': '桜花賞女王',
                         's': {'training': 95, 'jockey': 94, 'course': 94, 'distance': 95, 'prevRace': 96, 'pedigree': 96},
                         'str': '【世代屈指の底力】クラシック三冠すべて連対の絶対的能力。エピファネイア産駒のスタミナ。',
                         'con': '叩き良化型で秋初戦の仕上がり状態。'},
        'クイーンズウォーク': {'rank': 3, 'mark': '▲', 'score': 94.4, 'grade': 'S', 'tag': '調教S評価',
                           's': {'training': 98, 'jockey': 95, 'course': 94, 'distance': 94, 'prevRace': 93, 'pedigree': 93},
                           'str': '【栗東CW抜けた動き】キズナ産駒の好馬体。ローズSを完勝し、中内田厩舎の勝負仕上げ。',
                           'con': '2200mへの距離延長と折り合い。'},
        'ジョスラン': {'rank': 4, 'mark': '△', 'score': 93.6, 'grade': 'S', 'tag': 'ルメールの手綱',
                     's': {'training': 94, 'jockey': 98, 'course': 93, 'distance': 93, 'prevRace': 93, 'pedigree': 91},
                     'str': '【鞍上C.ルメール】中団から鋭く脚を使える自在性。勝負どころでの位置取りが抜群。',
                     'con': '古馬G1の厳しいペースでのスタミナ消耗。'},
        'チェルヴィニア': {'rank': 5, 'mark': '△', 'score': 92.8, 'grade': 'A+', 'tag': 'オークス馬',
                         's': {'training': 96, 'jockey': 93, 'course': 92, 'distance': 94, 'prevRace': 91, 'pedigree': 91},
                         'str': '【二冠牝馬の実績】東京優駿・オークスで見せた強烈な末脚。調教S評価で状態上向き。',
                         'con': '京都芝外回りの平坦コースへの適性。'},
        'ラヴァンダ': {'rank': 6, 'mark': '☆', 'score': 91.4, 'grade': 'A+', 'tag': '最内枠の利',
                     's': {'training': 92, 'jockey': 93, 'course': 92, 'distance': 91, 'prevRace': 92, 'pedigree': 90},
                     'str': '【1枠1番×岩田望来】前走3着と復調。インの好位をロスなく立ち回れる絶好枠。',
                     'con': '直線での瞬発力勝負でのキレ負け。'},
        'セキトバイースト': {'rank': 7, 'mark': '-', 'score': 90.5, 'grade': 'A', 'tag': '逃げ先行警戒',
                           's': {'training': 91, 'jockey': 91, 'course': 91, 'distance': 89, 'prevRace': 91, 'pedigree': 89},
                           'str': '積極策からの粘り腰。', 'con': '2200mの距離と道中のマーク。'},
        'レーゼドラマ': {'rank': 8, 'mark': '-', 'score': 89.8, 'grade': 'A', 'tag': '血統魅力',
                       's': {'training': 91, 'jockey': 90, 'course': 90, 'distance': 90, 'prevRace': 89, 'pedigree': 89},
                       'str': '調教A評価。田口貫太騎手。', 'con': 'G1の壁。'},
        'コガネノソラ': {'rank': 9, 'mark': '-', 'score': 89.2, 'grade': 'A', 'tag': 'クイーンS覇者',
                       's': {'training': 90, 'jockey': 89, 'course': 89, 'distance': 90, 'prevRace': 89, 'pedigree': 88},
                       'str': '洋芝重賞を勝ったスタミナ。', 'con': '京都の高速馬場への対応。'},
        'ラフターラインズ': {'rank': 10, 'mark': '-', 'score': 88.5, 'grade': 'B+', 'tag': '武豊の京都マジック',
                           's': {'training': 89, 'jockey': 97, 'course': 90, 'distance': 90, 'prevRace': 86, 'pedigree': 89},
                           'str': '【京都の神・武豊】道中じっくり脚を溜めての下り坂スパート。雨予報の重馬場もプラス。',
                           'con': '10番人気の低評価通り、近走のワンパンチ不足。'},
        'ニシノティアモ': {'rank': 11, 'mark': '-', 'score': 87.8, 'grade': 'B+', 'tag': '先行警戒',
                         's': {'training': 88, 'jockey': 86, 'course': 88, 'distance': 88, 'prevRace': 88, 'pedigree': 87},
                         'str': '立ち回りの巧さ。', 'con': '相手強化。'},
        'シャドウメテオ': {'rank': 12, 'mark': '-', 'score': 87.0, 'grade': 'B+', 'tag': 'ポツン一発',
                         's': {'training': 88, 'jockey': 90, 'course': 87, 'distance': 88, 'prevRace': 86, 'pedigree': 86},
                         'str': '横山典弘騎手。', 'con': '展開頼み。'},
        'エストゥペンダ': {'rank': 13, 'mark': '-', 'score': 86.2, 'grade': 'B', 'tag': '穴狙い',
                         's': {'training': 86, 'jockey': 87, 'course': 86, 'distance': 87, 'prevRace': 86, 'pedigree': 85},
                         'str': '大外枠から揉まれず運べる。', 'con': '力差あり。'},
        'ヴーレヴー': {'rank': 14, 'mark': '-', 'score': 85.5, 'grade': 'B', 'tag': '穴狙い',
                     's': {'training': 86, 'jockey': 87, 'course': 86, 'distance': 85, 'prevRace': 85, 'pedigree': 85},
                     'str': '末脚堅実。', 'con': '距離延長。'},
        'アクアヴァーナル': {'rank': 15, 'mark': '-', 'score': 85.0, 'grade': 'B', 'tag': '道悪の鬼・大穴',
                           's': {'training': 86, 'jockey': 92, 'course': 86, 'distance': 87, 'prevRace': 84, 'pedigree': 85},
                           'str': '【重馬場適性と松山弘平】タフな馬場での粘り強さ。消耗戦なら浮上。',
                           'con': '17番人気と下馬評は極めて低い。'},
        'レイクラシック': {'rank': 16, 'mark': '-', 'score': 84.5, 'grade': 'B', 'tag': '3歳斤量54kg',
                         's': {'training': 87, 'jockey': 90, 'course': 85, 'distance': 86, 'prevRace': 82, 'pedigree': 87},
                         'str': '【斤量54kg×西村淳也】坂路で活気ある動き。イン好位追走なら。',
                         'con': '前走ローズS10着大敗からの立て直し。'},
        'ケリフレッドアスク': {'rank': 17, 'mark': '-', 'score': 83.5, 'grade': 'B', 'tag': '大穴伏兵',
                           's': {'training': 85, 'jockey': 87, 'course': 84, 'distance': 85, 'prevRace': 83, 'pedigree': 83},
                           'str': '幸英明騎手。', 'con': '実績不足。'},
        'ジュウリョクピエロ': {'rank': 18, 'mark': '-', 'score': 82.5, 'grade': 'B', 'tag': '大穴伏兵',
                           's': {'training': 84, 'jockey': 85, 'course': 83, 'distance': 84, 'prevRace': 82, 'pedigree': 82},
                           'str': '今村聖奈騎手G1挑戦。', 'con': '力関係見劣り。'}
    }

    cr17 = []
    for s in r17_starters:
        hname = s['horseName']
        info = scores_17.get(hname, {'rank': 99, 'mark': '-', 'score': 80.0, 'grade': 'B', 'tag': '-',
                                     's': {'training': 80, 'jockey': 80, 'course': 80, 'distance': 80, 'prevRace': 80, 'pedigree': 80},
                                     'str': '-', 'con': '-'})
        cr17.append({
            'gate': s['gate'],
            'waku': s['waku'],
            'horseName': hname,
            'jockey': s['jockey'],
            'load': s['load'],
            'sexAge': s['sexAge'],
            'stable': s['stable'],
            'odds': s['odds'],
            'pop': s['pop'],
            'grade': info['grade'],
            'gradeTag': info['tag'],
            'recommendedMark': info['mark'],
            'scores': info['s'],
            'strengths': info['str'],
            'concerns': info['con'],
            'compositeScore': info['score'],
            'rank': info['rank']
        })
    cr17.sort(key=lambda x: x['rank'])
    pred_data['races']['17']['contenderRanking'] = cr17
    print(f"Added contenderRanking for Race 17 ({len(cr17)} horses).")

with open(PRED_JSON, 'w', encoding='utf-8') as f:
    json.dump(pred_data, f, ensure_ascii=False, indent=2)

with open(PRED_JS, 'w', encoding='utf-8') as f:
    f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')

print("Successfully updated prediction_data.json and prediction_data.js!")
