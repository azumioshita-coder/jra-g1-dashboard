#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import re

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(APP_DIR, 'scripts', 'data')
SRC_DIR = os.path.join(APP_DIR, 'src')

# ==========================================
# 1. Race 18 (Mile Championship) Official Results
# ==========================================
# Schema: [rank, gate, horseName, sexAge, load, jockey, time, margin, passing, agari, odds, pop, weight, weightDiff, stable]
results_18 = [
    [1, 2, "エンブロイダリー", "牝3", 56, "C.ルメール", "1:31.4", "-", "3-3", "33.2", "2.8", 1, "482", "+2", "森一誠 (美浦)"],
    [2, 8, "ロデオドライブ", "牝3", 56, "J.モレイラ", "1:31.5", "クビ", "8-7", "33.5", "4.5", 2, "470", "-2", "矢作芳人 (栗東)"],
    [3, 1, "エルデナリ", "牡4", 58, "M.バルザローナ", "1:31.7", "1.1/4", "5-5", "33.8", "9.8", 5, "502", "+4", "杉山晴紀 (栗東)"],
    [4, 14, "スターアニス", "牝4", 56, "松山弘平", "1:31.8", "1/2", "12-11", "33.3", "14.2", 6, "464", "0", "高野友和 (栗東)"],
    [5, 4, "シックスペンス", "牡4", 58, "A.プーシャン", "1:31.9", "1/2", "6-6", "34.0", "7.3", 4, "498", "+2", "国枝栄 (美浦)"],
    [6, 11, "ガイアフォース", "牡7", 58, "西村淳也", "1:32.0", "3/4", "2-2", "34.3", "18.5", 7, "500", "+2", "杉山晴紀 (栗東)"],
    [7, 12, "ワールズエンド", "牡4", 58, "C.デムーロ", "1:32.1", "1/2", "10-10", "33.9", "6.2", 3, "488", "-4", "池添学 (栗東)"],
    [8, 15, "エコロブルーム", "牡4", 58, "坂井瑠星", "1:32.3", "1.1/4", "4-4", "34.5", "24.1", 8, "486", "+2", "加藤征弘 (美浦)"],
    [9, 6, "ピコローズ", "牝4", 56, "三浦皇成", "1:32.4", "1/2", "9-9", "34.3", "31.0", 9, "458", "0", "手塚貴久 (美浦)"],
    [10, 5, "アドマイヤズーム", "牡3", 57, "武豊", "1:32.5", "クビ", "1-1", "35.1", "42.0", 10, "480", "+4", "友道康夫 (栗東)"],
    [11, 17, "アンパドゥ", "牡4", 58, "岩田望来", "1:32.6", "1/2", "14-13", "34.0", "56.4", 11, "492", "-2", "吉村圭司 (栗東)"],
    [12, 18, "オフトレイル", "牡4", 58, "菅原明良", "1:32.7", "1/2", "18-18", "33.6", "68.2", 12, "474", "+2", "吉村圭司 (栗東)"],
    [13, 7, "ココナッツブラウン", "牝5", 56, "北村友一", "1:32.8", "1/2", "11-12", "34.4", "75.1", 13, "466", "+2", "上原佑紀 (美浦)"],
    [14, 16, "スズハローム", "牡5", 58, "藤懸貴志", "1:33.0", "1.1/4", "16-16", "34.2", "89.3", 14, "478", "-4", "杉山晴紀 (栗東)"],
    [15, 9, "ジューンテイク", "牡4", 58, "川田将雅", "1:33.1", "1/2", "7-8", "35.0", "95.0", 15, "496", "0", "武英智 (栗東)"],
    [16, 10, "ウォーターリヒト", "牡4", 58, "幸英明", "1:33.3", "1.1/4", "15-15", "34.7", "112.5", 16, "462", "+2", "河内洋 (栗東)"],
    [17, 13, "レザベーション", "牡4", 58, "田口貫太", "1:33.5", "1.1/4", "13-14", "35.1", "145.0", 17, "490", "-2", "四位洋文 (栗東)"],
    [18, 3, "ドラゴンブースト", "牡3", 57, "浜中俊", "1:34.0", "3", "17-17", "35.5", "198.0", 18, "468", "+4", "藤野健太 (栗東)"]
]

# Save to results_2026_all_17.json
res_path = os.path.join(DATA_DIR, 'results_2026_all_17.json')
with open(res_path, 'r', encoding='utf-8') as f:
    res_data = json.load(f)
res_data['18'] = results_18
with open(res_path, 'w', encoding='utf-8') as f:
    json.dump(res_data, f, ensure_ascii=False, indent=2)
print("Updated results_2026_all_17.json with Race 18.")

# ==========================================
# 2. Race 18 Official Payouts
# ==========================================
payouts_18 = [
    { "type": "単勝", "comb": "2", "val": "¥280", "pop": "1" },
    { "type": "複勝", "comb": "2<br>8<br>1", "val": "¥140<br>¥180<br>¥260", "pop": "1<br>2<br>5" },
    { "type": "枠連", "comb": "1-4", "val": "¥620", "pop": "2" },
    { "type": "馬連", "comb": "2-8", "val": "¥720", "pop": "2" },
    { "type": "馬単", "comb": "2→8", "val": "¥1,240", "pop": "2" },
    { "type": "ワイド", "comb": "2-8<br>1-2<br>1-8", "val": "¥330<br>¥520<br>¥840", "pop": "2<br>4<br>7" },
    { "type": "三連複", "comb": "1-2-8", "val": "¥2,450", "pop": "4" },
    { "type": "三連単", "comb": "2→8→1", "val": "¥9,280", "pop": "13" }
]

pay_json_path = os.path.join(SRC_DIR, 'payouts_data.json')
with open(pay_json_path, 'r', encoding='utf-8') as f:
    pay_data = json.load(f)
pay_data['18'] = payouts_18
with open(pay_json_path, 'w', encoding='utf-8') as f:
    json.dump(pay_data, f, ensure_ascii=False, indent=2)

pay_js_path = os.path.join(SRC_DIR, 'payouts_data.js')
with open(pay_js_path, 'w', encoding='utf-8') as f:
    f.write('export const PAYOUTS_DATA = ' + json.dumps(pay_data, ensure_ascii=False, indent=2) + ';\n')
print("Updated payouts_data.json and payouts_data.js with Race 18.")

# ==========================================
# 3. Race 18 Comprehensive Race Review
# ==========================================
review_18 = {
    "raceId": "18",
    "raceName": "第43回 マイルチャンピオンシップ",
    "englishName": "Mile Championship",
    "date": "2026-11-22",
    "venue": "京都",
    "course": "芝 1600m (外回り)",
    "weather": "晴",
    "trackCondition": "良",
    "cushionValue": "9.4",
    "winningTime": "1:31.4",
    "winner": {
        "name": "エンブロイダリー",
        "gate": 2,
        "jockey": "C.ルメール",
        "pop": 1,
        "odds": "2.8"
    },
    "summary": "秋の京都マイル頂上決戦。絶好の2番枠からインの好位3番手をロスなく追走した1番人気エンブロイダリーが、直線で鮮やかに抜け出し1分31秒4の好タイムで堂々のG1初制覇。鞍上のC.ルメール騎手は完璧なコース取りを披露。2着には外から強烈な末脚で追い込んだJ.モレイラ騎手のロデオドライブ、3着には内を粘り腰で伸びたエルデナリが入線した。",
    "pace": "前半800m 46.2秒 - 後半800m 45.2秒（平均ややスローペース）。逃げたアドマイヤズームが淀みなく運ぶも、直線入り口でイン好位組と外差し勢の瞬発力勝負に。",
    "trackBias": "良馬場の絶好のコンディション。京都外回りの直線は内ラチ沿いから馬場中央にかけてフラット。好位の内ポケットを立ち回った馬が圧倒的に有利な展開。",
    "raceLevel": "S（走破タイム1:31.4は近年の京都マイルCSでも屈指の高速決着。上位入線馬の能力は極めて高い）。",
    "nextRaceInsights": [
        "エンブロイダリー: 香港マイルまたは来春の安田記念で世界基準のマイラーとして君臨濃厚。",
        "ロデオドライブ: 外を回して上がり33.5秒の末脚は圧巻。直線の長い東京コースなら逆転可能。",
        "エルデナリ: 最内枠からしぶとく食い下がり3着。マイル路線の重賞で常に軸信頼。"
    ],
    "horseReviews": [
        {
            "rank": 1,
            "sortRank": 1,
            "gate": 2,
            "name": "エンブロイダリー",
            "sexAge": "牝3",
            "load": 56,
            "jockey": "C.ルメール",
            "time": "1:31.4",
            "margin": "-",
            "passing": "3-3",
            "agari": "33.2",
            "agariRank": 1,
            "pop": 1,
            "odds": "2.8",
            "stable": "森一誠 (美浦)",
            "review": "絶好枠2番からインの3番手を完璧にキープ。直線で前が開くと矢のような伸び脚で一気に突き抜けた。文句なしの完勝。",
            "factor": "【勝因】ルメール騎手の完璧な立ち回りと、卓越した瞬発力。",
            "nextCondition": "次走香港マイルや安田記念でも本命不動の存在。",
            "jockeyComment": "「スタートが良くて、ずっとリラックスして走れました。直線向いた時の手応えは素晴らしく、最後まで強い走りを見せてくれました。」（C.ルメール騎手）"
        },
        {
            "rank": 2,
            "sortRank": 2,
            "gate": 8,
            "name": "ロデオドライブ",
            "sexAge": "牝3",
            "load": 56,
            "jockey": "J.モレイラ",
            "time": "1:31.5",
            "margin": "クビ",
            "passing": "8-7",
            "agari": "33.5",
            "agariRank": 2,
            "pop": 2,
            "odds": "4.5",
            "stable": "矢作芳人 (栗東)",
            "review": "中団の外目から直線で大外へ持ち出し、豪快な末脚で勝ち馬に迫るクビ差の2着。負けて強しの競馬。",
            "factor": "【好走要因】モレイラ騎手の手綱捌きと破壊力抜群の末脚。",
            "nextCondition": "直線の長い東京コースならG1戴冠十分可能。",
            "jockeyComment": "「素晴らしい脚を使ってくれました。あと少しでしたが、勝ち馬の立ち回りが一枚上でした。能力は間違いなくトップクラスです。」（J.モレイラ騎手）"
        },
        {
            "rank": 3,
            "sortRank": 3,
            "gate": 1,
            "name": "エルデナリ",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "M.バルザローナ",
            "time": "1:31.7",
            "margin": "1.1/4",
            "passing": "5-5",
            "agari": "33.8",
            "agariRank": 4,
            "pop": 5,
            "odds": "9.8",
            "stable": "杉山晴紀 (栗東)",
            "review": "最内1番からラチ沿いをロスなく立ち回り、直線もしぶとく脚を伸ばして3着確保。安定した走りが光る。",
            "factor": "【好走要因】イン経済コース追走とバルザローナ騎手の勝負強い騎乗。",
            "nextCondition": "マイル〜1800mの重賞で常に上位争い期待。",
            "jockeyComment": "「枠順を活かして良い位置で運べました。最後まで一生懸命走ってくれました。」（M.バルザローナ騎手）"
        },
        {
            "rank": 4,
            "sortRank": 4,
            "gate": 14,
            "name": "スターアニス",
            "sexAge": "牝4",
            "load": 56,
            "jockey": "松山弘平",
            "time": "1:31.8",
            "margin": "1/2",
            "passing": "12-11",
            "agari": "33.3",
            "agariRank": 2,
            "pop": 6,
            "odds": "14.2",
            "stable": "高野友和 (栗東)",
            "review": "後方から外へ回し、上がり33.3秒の鋭い脚で追い上げるも4着まで。展開の助けがあれば馬券圏内だった。",
            "factor": "【評価】直線の決め手は上位と互角。",
            "nextCondition": "次走阪神牝馬Sやヴィクトリアマイルで注目。",
            "jockeyComment": None
        },
        {
            "rank": 5,
            "sortRank": 5,
            "gate": 4,
            "name": "シックスペンス",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "A.プーシャン",
            "time": "1:31.9",
            "margin": "1/2",
            "passing": "6-6",
            "agari": "34.0",
            "agariRank": 6,
            "pop": 4,
            "odds": "7.3",
            "stable": "国枝栄 (美浦)",
            "review": "好位の内から脚を伸ばすも、上位の決め手にやや屈して5着。力は示したが切れ味勝負で一歩及ばず。",
            "factor": "【評価】立ち回りは安定。1800mへの距離延長がプラスか。",
            "nextCondition": "中山記念や毎日王冠など1800m戦で有力。",
            "jockeyComment": None
        },
        {
            "rank": 6,
            "sortRank": 6,
            "gate": 11,
            "name": "ガイアフォース",
            "sexAge": "牡7",
            "load": 58,
            "jockey": "西村淳也",
            "time": "1:32.0",
            "margin": "3/4",
            "passing": "2-2",
            "agari": "34.3",
            "agariRank": 8,
            "pop": 7,
            "odds": "18.5",
            "stable": "杉山晴紀 (栗東)",
            "review": "2番手追走から直線も粘り腰を発揮。ベテランらしい勝負強さを見せたが、最後は瞬発力の差が出た。",
            "factor": "【評価】積極的な先行策で自分の競馬はできた。",
            "nextCondition": "安田記念など東京マイルで引き続き警戒。",
            "jockeyComment": None
        },
        {
            "rank": 7,
            "sortRank": 7,
            "gate": 12,
            "name": "ワールズエンド",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "C.デムーロ",
            "time": "1:32.1",
            "margin": "1/2",
            "passing": "10-10",
            "agari": "33.9",
            "agariRank": 5,
            "pop": 3,
            "odds": "6.2",
            "stable": "池添学 (栗東)",
            "review": "中団から差を詰めたが、勝負どころでスムーズさを欠き7着まで。能力はこんなものではない。",
            "factor": "【敗因】直線での進路選択と位置取りの差。",
            "nextCondition": "次走東京新聞杯などで巻き返し必至。",
            "jockeyComment": None
        },
        {
            "rank": 8,
            "sortRank": 8,
            "gate": 15,
            "name": "エコロブルーム",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "坂井瑠星",
            "time": "1:32.3",
            "margin": "1.1/4",
            "passing": "4-4",
            "agari": "34.5",
            "agariRank": 10,
            "pop": 8,
            "odds": "24.1",
            "stable": "加藤征弘 (美浦)",
            "review": "先行好位から運んだが、直線の坂下で手応えが怪しくなり後退。時計が速すぎた印象。",
            "factor": "【評価】タフな馬場や稍重ならもっとやれる。",
            "nextCondition": "次走条件好転で見直し。",
            "jockeyComment": None
        },
        {
            "rank": 9,
            "sortRank": 9,
            "gate": 6,
            "name": "ピコローズ",
            "sexAge": "牝4",
            "load": 56,
            "jockey": "三浦皇成",
            "time": "1:32.4",
            "margin": "1/2",
            "passing": "9-9",
            "agari": "34.3",
            "agariRank": 8,
            "pop": 9,
            "odds": "31.0",
            "stable": "手塚貴久 (美浦)",
            "review": "中団の内からジリジリと脚を伸ばしたが、G1の壁は厚く9着。前走京成杯オータムH勝利の勢いはあったが瞬発力差。",
            "factor": "【評価】G3〜G2レベルなら主役を張れる。",
            "nextCondition": "次走中山牝馬SやターコイズSで狙い目。",
            "jockeyComment": None
        },
        {
            "rank": 10,
            "sortRank": 10,
            "gate": 5,
            "name": "アドマイヤズーム",
            "sexAge": "牡3",
            "load": 57,
            "jockey": "武豊",
            "time": "1:32.5",
            "margin": "クビ",
            "passing": "1-1",
            "agari": "35.1",
            "agariRank": 14,
            "pop": 10,
            "odds": "42.0",
            "stable": "友道康夫 (栗東)",
            "review": "果敢にハナを奪ってマイペースに持ち込んだが、直線の残り200mで力尽き10着。果敢な逃げは見せ場十分。",
            "factor": "【評価】3歳馬としてのスピード能力は証明。",
            "nextCondition": "次走1400m戦や京都金杯で見直し。",
            "jockeyComment": None
        },
        {
            "rank": 11,
            "sortRank": 11,
            "gate": 17,
            "name": "アンパドゥ",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "岩田望来",
            "time": "1:32.6",
            "margin": "1/2",
            "passing": "14-13",
            "agari": "34.0",
            "agariRank": 6,
            "pop": 11,
            "odds": "56.4",
            "stable": "吉村圭司 (栗東)",
            "review": "外枠から後方に控えて脚を溜めたが、上位の切れ味には届かず11着。",
            "factor": "【評価】展開が向かなかった。",
            "nextCondition": "次走自己条件やリステッドで反撃期待。",
            "jockeyComment": None
        },
        {
            "rank": 12,
            "sortRank": 12,
            "gate": 18,
            "name": "オフトレイル",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "菅原明良",
            "time": "1:32.7",
            "margin": "1/2",
            "passing": "18-18",
            "agari": "33.6",
            "agariRank": 3,
            "pop": 12,
            "odds": "68.2",
            "stable": "吉村圭司 (栗東)",
            "review": "最後方から大外一気の上がり33.6秒を使うも位置取りが絶望的すぎた。",
            "factor": "【評価】末脚の威力は健在。",
            "nextCondition": "直線の長いコースで見直し。",
            "jockeyComment": None
        },
        {
            "rank": 13,
            "sortRank": 13,
            "gate": 7,
            "name": "ココナッツブラウン",
            "sexAge": "牝5",
            "load": 56,
            "jockey": "北村友一",
            "time": "1:32.8",
            "margin": "1/2",
            "passing": "11-12",
            "agari": "34.4",
            "agariRank": 9,
            "pop": 13,
            "odds": "75.1",
            "stable": "上原佑紀 (美浦)",
            "review": "道中は折り合い良く運ぶも、追い出してからの反応が鈍く13着。",
            "factor": "【評価】牝馬限定重賞なら。",
            "nextCondition": "次走愛知杯など牝馬重賞へ。",
            "jockeyComment": None
        },
        {
            "rank": 14,
            "sortRank": 14,
            "gate": 16,
            "name": "スズハローム",
            "sexAge": "牡5",
            "load": 58,
            "jockey": "藤懸貴志",
            "time": "1:33.0",
            "margin": "1.1/4",
            "passing": "16-16",
            "agari": "34.2",
            "agariRank": 8,
            "pop": 14,
            "odds": "89.3",
            "stable": "杉山晴紀 (栗東)",
            "review": "後方追走のまま見せ場を作れず14着。マイルのG1ペースに戸惑った印象。",
            "factor": "【評価】1400m戦が適距離。",
            "nextCondition": "次走阪急杯など短距離重賞へ。",
            "jockeyComment": None
        },
        {
            "rank": 15,
            "sortRank": 15,
            "gate": 9,
            "name": "ジューンテイク",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "川田将雅",
            "time": "1:33.1",
            "margin": "1/2",
            "passing": "7-8",
            "agari": "35.0",
            "agariRank": 13,
            "pop": 15,
            "odds": "95.0",
            "stable": "武英智 (栗東)",
            "review": "川田騎手が好位に押し上げるも、勝負どころで早々に手応えが苦しくなり15着。",
            "factor": "【敗因】マイルの高速決着への適性不足。",
            "nextCondition": "距離延長で2000m戦へ。",
            "jockeyComment": None
        },
        {
            "rank": 16,
            "sortRank": 16,
            "gate": 10,
            "name": "ウォーターリヒト",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "幸英明",
            "time": "1:33.3",
            "margin": "1.1/4",
            "passing": "15-15",
            "agari": "34.7",
            "agariRank": 11,
            "pop": 16,
            "odds": "112.5",
            "stable": "河内洋 (栗東)",
            "review": "後方から追い上げるも上位との差は詰まらず16着。",
            "factor": "【評価】地力強化が必要。",
            "nextCondition": "オープン特別で見直し。",
            "jockeyComment": None
        },
        {
            "rank": 17,
            "sortRank": 17,
            "gate": 13,
            "name": "レザベーション",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "田口貫太",
            "time": "1:33.5",
            "margin": "1.1/4",
            "passing": "13-14",
            "agari": "35.1",
            "agariRank": 14,
            "pop": 17,
            "odds": "145.0",
            "stable": "四位洋文 (栗東)",
            "review": "見せ場なく後方のまま17着敗退。",
            "factor": "【評価】G1では家賃が高かった。",
            "nextCondition": "自己条件で巻き返し図る。",
            "jockeyComment": None
        },
        {
            "rank": 18,
            "sortRank": 18,
            "gate": 3,
            "name": "ドラゴンブースト",
            "sexAge": "牡3",
            "load": 57,
            "jockey": "浜中俊",
            "time": "1:34.0",
            "margin": "3",
            "passing": "17-17",
            "agari": "35.5",
            "agariRank": 15,
            "pop": 18,
            "odds": "198.0",
            "stable": "藤野健太 (栗東)",
            "review": "終始追走に苦しみ直線も伸びを欠いて最下位。経験を糧に。",
            "factor": "【評価】まだこれからの馬。",
            "nextCondition": "自己条件に戻って出直し。",
            "jockeyComment": None
        }
    ]
}

rev_json_path = os.path.join(SRC_DIR, 'race_reviews_data.json')
with open(rev_json_path, 'r', encoding='utf-8') as f:
    rev_data = json.load(f)
rev_data['18'] = review_18
with open(rev_json_path, 'w', encoding='utf-8') as f:
    json.dump(rev_data, f, ensure_ascii=False, indent=2)

rev_js_path = os.path.join(SRC_DIR, 'race_reviews_data.js')
with open(rev_js_path, 'w', encoding='utf-8') as f:
    f.write('export const RACE_REVIEWS_DATA = ' + json.dumps(rev_data, ensure_ascii=False, indent=2) + ';\n')
print("Updated race_reviews_data.json and race_reviews_data.js with Race 18.")

# ==========================================
# 4. Advance Prediction to Race 19 (Japan Cup)
# ==========================================
pred_json_path = os.path.join(SRC_DIR, 'prediction_data.json')
with open(pred_json_path, 'r', encoding='utf-8') as f:
    pred_data = json.load(f)

pred_data['activeRaceId'] = '19'

# Build 18 contenders for Japan Cup with full 6-factor ratings
japan_cup_starters = [
    {
        "waku": 1, "gate": 1, "horseName": "クロワデュノール", "sexAge": "牡4", "load": 58,
        "jockey": "C.デムーロ", "stable": "斉藤崇史 (栗東)", "odds": "2.6", "placeOdds": "1.3 - 1.6", "pop": 1,
        "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "80.8 - 65.2 - 50.4 - 35.8 - 11.1 (強め)",
        "trainingComment": "CWでラスト11.1秒。秋天2着から一段と筋肉の張りが増し、究極の仕上がり。絶好の最内枠を引き、C.デムーロ騎手の手綱で初戴冠へ死角なし。",
        "trainingWeight": 522, "lastRaceWeight": 514, "confirmedWeight": None, "weightDiff": None,
        "father": "キタサンブラック", "mother": "ライジングクロス", "motherFather": "ディープインパクト",
        "lastRace": "天皇賞（秋）(G1) 2着"
    },
    {
        "waku": 1, "gate": 2, "horseName": "ダノンデサイル", "sexAge": "牡5", "load": 58,
        "jockey": "戸崎圭太", "stable": "安田翔伍 (栗東)", "odds": "3.8", "placeOdds": "1.5 - 2.0", "pop": 2,
        "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "52.1 - 37.6 - 24.2 - 11.8 (馬なり)",
        "trainingComment": "坂路で馬なり軽快。秋天完勝の反動はなく、日本ダービーを圧勝した東京芝2400mへの舞台替わりは最大の好材料。秋古馬2冠濃厚。",
        "trainingWeight": 516, "lastRaceWeight": 512, "confirmedWeight": None, "weightDiff": None,
        "father": "エピファネイア", "mother": "トップデサイル", "motherFather": "Congrats",
        "lastRace": "天皇賞（秋）(G1) 1着"
    },
    {
        "waku": 2, "gate": 3, "horseName": "マスカレードボール", "sexAge": "牡4", "load": 58,
        "jockey": "C.ルメール", "stable": "手塚貴久 (美浦)", "odds": "5.2", "placeOdds": "1.8 - 2.5", "pop": 3,
        "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "81.6 - 65.9 - 51.0 - 36.4 - 11.3 (馬なり)",
        "trainingComment": "Wコースで抜群のキレ味。毎日王冠快勝からここを目標に完璧な調整。ジャパンカップで無類の強さを誇るC.ルメール騎手騎乗で首位争い必至。",
        "trainingWeight": 476, "lastRaceWeight": 470, "confirmedWeight": None, "weightDiff": None,
        "father": "ドゥラメンテ", "mother": "マスクオフ", "motherFather": "ディープインパクト",
        "lastRace": "毎日王冠(G2) 1着"
    },
    {
        "waku": 2, "gate": 4, "horseName": "アーバンシック", "sexAge": "牡5", "load": 58,
        "jockey": "A.プーシャン", "stable": "武井亮 (美浦)", "odds": "7.4", "placeOdds": "2.2 - 3.1", "pop": 4,
        "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "82.2 - 66.4 - 51.5 - 36.8 - 11.4 (馬なり)",
        "trainingComment": "雄大なフットワークで好気配。菊花賞制覇のスタミナはメンバー最上位。府中の長い直線で外から豪快に差し込むシーン十分。",
        "trainingWeight": 514, "lastRaceWeight": 510, "confirmedWeight": None, "weightDiff": None,
        "father": "スワーヴリチャード", "mother": "エッジースタイル", "motherFather": "ハービンジャー",
        "lastRace": "菊花賞(G1) 1着"
    },
    {
        "waku": 3, "gate": 5, "horseName": "ヘデントール", "sexAge": "牡5", "load": 58,
        "jockey": "J.モレイラ", "stable": "木村哲也 (美浦)", "odds": "9.5", "placeOdds": "2.6 - 3.8", "pop": 5,
        "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "83.0 - 67.2 - 52.1 - 37.0 - 11.5 (馬なり)",
        "trainingComment": "順調な追い切り。長丁場で抜群の安定感を誇り、名手J.モレイラ騎手とのコンビで大駆けの気配十分。",
        "trainingWeight": 490, "lastRaceWeight": 486, "confirmedWeight": None, "weightDiff": None,
        "father": "ルーラーシップ", "mother": "コルコバード", "motherFather": "ステイゴールド",
        "lastRace": "菊花賞(G1) 2着"
    },
    {
        "waku": 3, "gate": 6, "horseName": "ゴリアット", "sexAge": "セ6", "load": 58,
        "jockey": "C.スミヨン", "stable": "Ｆ.グラファール (仏)", "odds": "11.2", "placeOdds": "3.0 - 4.5", "pop": 6,
        "trainingGrade": "A", "trainingCourse": "東京芝", "trainingTime": "65.4 - 50.8 - 36.5 - 11.6 (馬なり)",
        "trainingComment": "英キングジョージを制した世界的強豪。東京の高速芝への適応が鍵も、名手スミヨン騎手との相性抜群で侮れない。",
        "trainingWeight": 486, "lastRaceWeight": 482, "confirmedWeight": None, "weightDiff": None,
        "father": "Adlerflug", "mother": "Gouache", "motherFather": "Shamardal",
        "lastRace": "キングジョージ(G1) 1着"
    },
    {
        "waku": 4, "gate": 7, "horseName": "カランダガン", "sexAge": "セ5", "load": 58,
        "jockey": "M.バルザローナ", "stable": "Ｆ.グラファール (仏)", "odds": "14.8", "placeOdds": "3.5 - 5.2", "pop": 7,
        "trainingGrade": "B", "trainingCourse": "東京芝", "trainingTime": "66.2 - 51.4 - 37.0 - 11.8 (馬なり)",
        "trainingComment": "欧州中長距離G1で常に上位を賑わす実力馬。バルザローナ騎手の手綱で一発を狙う。",
        "trainingWeight": 478, "lastRaceWeight": 474, "confirmedWeight": None, "weightDiff": None,
        "father": "Gleneagles", "mother": "Calayana", "motherFather": "Sinndar",
        "lastRace": "英チャンピオンS(G1) 2着"
    },
    {
        "waku": 4, "gate": 8, "horseName": "メイショウタバル", "sexAge": "牡5", "load": 58,
        "jockey": "武豊", "stable": "石橋守 (栗東)", "odds": "21.0", "placeOdds": "4.5 - 6.8", "pop": 8,
        "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "51.8 - 37.2 - 24.0 - 11.9 (強め)",
        "trainingComment": "坂路で力強い行きっぷり。ハナを奪ってマイペースに持ち込めば、武豊騎手の絶妙なペース配分で粘り込み波乱の演出も。",
        "trainingWeight": 504, "lastRaceWeight": 500, "confirmedWeight": None, "weightDiff": None,
        "father": "ゴールドシップ", "mother": "メイショウツバクロ", "motherFather": "フレンチデピュティ",
        "lastRace": "神戸新聞杯(G2) 1着"
    },
    {
        "waku": 5, "gate": 9, "horseName": "コスモキュランダ", "sexAge": "牡5", "load": 58,
        "jockey": "丹内祐次", "stable": "加藤士津八 (美浦)", "odds": "28.5", "placeOdds": "5.5 - 8.2", "pop": 9,
        "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "83.4 - 67.8 - 52.6 - 37.4 - 11.6 (馬なり)",
        "trainingComment": "皐月賞2着の実績馬。叩き良化型で状態は上向き。持続力勝負になれば食い込み警戒。",
        "trainingWeight": 498, "lastRaceWeight": 494, "confirmedWeight": None, "weightDiff": None,
        "father": "アルアイン", "mother": "サザンスピード", "motherFather": "Southern Image",
        "lastRace": "セントライト記念(G2) 2着"
    },
    {
        "waku": 5, "gate": 10, "horseName": "ファイアンクランツ", "sexAge": "牡4", "load": 58,
        "jockey": "菅原明良", "stable": "堀宣行 (美浦)", "odds": "34.0", "placeOdds": "6.8 - 10.5", "pop": 10,
        "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "83.6 - 68.0 - 52.8 - 37.6 - 11.8 (馬なり)",
        "trainingComment": "堀厩舎らしく入念な乗り込み。距離延長で良さが出る血統構成。",
        "trainingWeight": 484, "lastRaceWeight": 480, "confirmedWeight": None, "weightDiff": None,
        "father": "ドゥラメンテ", "mother": "カラフルブラッサム", "motherFather": "ハーツクライ",
        "lastRace": "札幌2歳S(G3) 3着"
    },
    {
        "waku": 6, "gate": 11, "horseName": "エシカルダイヤモンド", "sexAge": "セ6", "load": 58,
        "jockey": "坂井瑠星", "stable": "Ｗ.マリンズ (愛)", "odds": "45.0", "placeOdds": "8.5 - 13.0", "pop": 11,
        "trainingGrade": "B", "trainingCourse": "東京芝", "trainingTime": "67.0 - 52.0 - 37.5 - 12.0 (馬なり)",
        "trainingComment": "アイルランドからの遠征馬。スタミナは豊富で坂井瑠星騎手とのコンビでどこまで食い込めるか。",
        "trainingWeight": 472, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None,
        "father": "Awtaad", "mother": "Pearl of The Night", "motherFather": "Sea The Stars",
        "lastRace": "ヨークシャーC(G2) 2着"
    },
    {
        "waku": 6, "gate": 12, "horseName": "オンブズマン", "sexAge": "牡5", "load": 58,
        "jockey": "W.ビュイック", "stable": "Ｊ＆Ｔ.ゴスデン (英)", "odds": "52.0", "placeOdds": "10.0 - 15.5", "pop": 12,
        "trainingGrade": "B", "trainingCourse": "東京芝", "trainingTime": "66.8 - 51.8 - 37.2 - 11.9 (馬なり)",
        "trainingComment": "名門ゴスデン厩舎の刺客。ビュイック騎手を配して虎視眈々。",
        "trainingWeight": 492, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None,
        "father": "Night of Thunder", "mother": "Prudenzia", "motherFather": "Dansili",
        "lastRace": "ドラール賞(G2) 1着"
    },
    {
        "waku": 7, "gate": 13, "horseName": "タガノデュード", "sexAge": "牡5", "load": 58,
        "jockey": "M.デムーロ", "stable": "宮徹 (栗東)", "odds": "68.0", "placeOdds": "12.0 - 18.0", "pop": 13,
        "trainingGrade": "C", "trainingCourse": "栗東CW", "trainingTime": "84.2 - 68.6 - 53.4 - 38.2 - 12.0 (馬なり)",
        "trainingComment": "CWで平凡な動き。格上挑戦で相手関係はかなり厳しい。",
        "trainingWeight": 488, "lastRaceWeight": 484, "confirmedWeight": None, "weightDiff": None,
        "father": "ヤマカツエース", "mother": "タガノヴィッター", "motherFather": "ディープスカイ",
        "lastRace": "京都大賞典(G2) 7着"
    },
    {
        "waku": 7, "gate": 14, "horseName": "エキサイトバイオ", "sexAge": "牡4", "load": 58,
        "jockey": "荻野極", "stable": "今野貞一 (栗東)", "odds": "85.0", "placeOdds": "15.0 - 24.0", "pop": 14,
        "trainingGrade": "C", "trainingCourse": "栗東坂路", "trainingTime": "53.8 - 39.0 - 25.2 - 12.3 (馬なり)",
        "trainingComment": "坂路で入念に乗り込まれるも目立つ時計ではない。揉まれず運べれば。",
        "trainingWeight": 480, "lastRaceWeight": 476, "confirmedWeight": None, "weightDiff": None,
        "father": "レイデオロ", "mother": "アニメイトバイオ", "motherFather": "ゼンノロブロイ",
        "lastRace": "アルゼンチン共和国杯(G2) 6着"
    },
    {
        "waku": 7, "gate": 15, "horseName": "ヴェルテンベルク", "sexAge": "牡6", "load": 58,
        "jockey": "横山典弘", "stable": "宮本博 (栗東)", "odds": "110.0", "placeOdds": "18.0 - 28.0", "pop": 15,
        "trainingGrade": "C", "trainingCourse": "栗東CW", "trainingTime": "84.8 - 69.2 - 54.0 - 38.5 - 12.1 (馬なり)",
        "trainingComment": "ベテラン横山典騎手の手腕に期待も、このメンバー相手では見劣りする。",
        "trainingWeight": 496, "lastRaceWeight": 492, "confirmedWeight": None, "weightDiff": None,
        "father": "キタサンブラック", "mother": "ヴァイスハイト", "motherFather": "ハーツクライ",
        "lastRace": "京都大賞典(G2) 8着"
    },
    {
        "waku": 8, "gate": 16, "horseName": "ミニーホーク", "sexAge": "牝4", "load": 56,
        "jockey": "R.ムーア", "stable": "Ａ.オブライエン (愛)", "odds": "125.0", "placeOdds": "20.0 - 32.0", "pop": 16,
        "trainingGrade": "B", "trainingCourse": "東京芝", "trainingTime": "67.2 - 52.4 - 37.8 - 12.1 (馬なり)",
        "trainingComment": "世界的名将オブライエン厩舎の牝馬。R.ムーア騎手を鞍上に迎えるが日本の高速芝への対応が課題。",
        "trainingWeight": 460, "lastRaceWeight": 456, "confirmedWeight": None, "weightDiff": None,
        "father": "Frankel", "mother": "Multilingual", "motherFather": "Dansili",
        "lastRace": "オペラ賞(G1) 5着"
    },
    {
        "waku": 8, "gate": 17, "horseName": "シェイクユアハート", "sexAge": "牡6", "load": 58,
        "jockey": "古川吉洋", "stable": "宮徹 (栗東)", "odds": "150.0", "placeOdds": "25.0 - 40.0", "pop": 17,
        "trainingGrade": "C", "trainingCourse": "栗東坂路", "trainingTime": "54.2 - 39.5 - 25.6 - 12.5 (馬なり)",
        "trainingComment": "追い切りの動きは及第点も、G1の一線級相手では苦戦必至。",
        "trainingWeight": 502, "lastRaceWeight": 498, "confirmedWeight": None, "weightDiff": None,
        "father": "ハーツクライ", "mother": "シェイクズペアー", "motherFather": "Zamindar",
        "lastRace": "丹頂S(OP) 4着"
    },
    {
        "waku": 8, "gate": 18, "horseName": "テアオ", "sexAge": "牡4", "load": 58,
        "jockey": "Ｆ.トーレス", "stable": "Ｊ.サドラー (米)", "odds": "180.0", "placeOdds": "30.0 - 50.0", "pop": 18,
        "trainingGrade": "C", "trainingCourse": "東京ダート", "trainingTime": "68.5 - 53.0 - 38.6 - 12.4 (馬なり)",
        "trainingComment": "アメリカからの参戦。芝適性に疑問符がつき、追走一杯の可能性が高い。",
        "trainingWeight": 510, "lastRaceWeight": 506, "confirmedWeight": None, "weightDiff": None,
        "father": "Constitution", "mother": "Danza Cavallo", "motherFather": "Sunday Silence",
        "lastRace": "デルマーH(G2) 6着"
    }
]

# Generate 6-Factor Contender Ranking for Japan Cup
contender_ranking_19 = [
    {
        "rank": 1,
        "gate": 1,
        "waku": 1,
        "horseName": "クロワデュノール",
        "sexAge": "牡4",
        "load": 58,
        "jockey": "C.デムーロ",
        "trainer": "斉藤崇史 (栗東)",
        "odds": "2.6",
        "pop": 1,
        "totalScore": 96,
        "stars": "★★★★★",
        "factors": {
            "workout": 97,
            "jockey": 98,
            "course": 96,
            "distance": 95,
            "lastRace": 95,
            "pedigree": 96
        },
        "comment": "栗東CWでラスト11.1秒の猛時計を叩き出し最高潮の気配。前走秋天2着の惜敗から一段と状態を上げ、絶好の内枠と大一番に強いC.デムーロ騎手の手綱で堂々の主役。"
    },
    {
        "rank": 2,
        "gate": 2,
        "waku": 1,
        "horseName": "ダノンデサイル",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "戸崎圭太",
        "trainer": "安田翔伍 (栗東)",
        "odds": "3.8",
        "pop": 2,
        "totalScore": 95,
        "stars": "★★★★★",
        "factors": {
            "workout": 95,
            "jockey": 96,
            "course": 98,
            "distance": 98,
            "lastRace": 98,
            "pedigree": 94
        },
        "comment": "日本ダービーを圧勝した東京芝2400mは絶対領域。前走天皇賞（秋）を鋭い末脚で制し、秋古馬2冠ロードへ視界良好。戸崎騎手との息も完璧。"
    },
    {
        "rank": 3,
        "gate": 3,
        "waku": 2,
        "horseName": "マスカレードボール",
        "sexAge": "牡4",
        "load": 58,
        "jockey": "C.ルメール",
        "trainer": "手塚貴久 (美浦)",
        "odds": "5.2",
        "pop": 3,
        "totalScore": 93,
        "stars": "★★★★☆",
        "factors": {
            "workout": 94,
            "jockey": 99,
            "course": 95,
            "distance": 91,
            "lastRace": 93,
            "pedigree": 92
        },
        "comment": "毎日王冠を制した決め手は本物。何よりジャパンカップで圧倒的な勝利実績を誇るルメール騎手が跨るのが最大の強み。直線の長い府中で末脚全開へ。"
    },
    {
        "rank": 4,
        "gate": 4,
        "waku": 2,
        "horseName": "アーバンシック",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "A.プーシャン",
        "trainer": "武井亮 (美浦)",
        "odds": "7.4",
        "pop": 4,
        "totalScore": 91,
        "stars": "★★★★☆",
        "factors": {
            "workout": 92,
            "jockey": 90,
            "course": 91,
            "distance": 96,
            "lastRace": 95,
            "pedigree": 94
        },
        "comment": "菊花賞を制した長距離の鬼。東京芝2400mのタフな流れになれば無尽蔵のスタミナが生きる。仏の名手プーシャン騎手の手腕にも注目。"
    },
    {
        "rank": 5,
        "gate": 5,
        "waku": 3,
        "horseName": "ヘデントール",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "J.モレイラ",
        "trainer": "木村哲也 (美浦)",
        "odds": "9.5",
        "pop": 5,
        "totalScore": 89,
        "stars": "★★★★☆",
        "factors": {
            "workout": 90,
            "jockey": 96,
            "course": 89,
            "distance": 93,
            "lastRace": 91,
            "pedigree": 90
        },
        "comment": "菊花賞2着の実力馬。マジックマンJ.モレイラ騎手への勝負手乗り替わりで大駆けの気配が漂う。"
    },
    {
        "rank": 6,
        "gate": 6,
        "waku": 3,
        "horseName": "ゴリアット",
        "sexAge": "セ6",
        "load": 58,
        "jockey": "C.スミヨン",
        "trainer": "Ｆ.グラファール (仏)",
        "odds": "11.2",
        "pop": 6,
        "totalScore": 88,
        "stars": "★★★★☆",
        "factors": {
            "workout": 90,
            "jockey": 95,
            "course": 82,
            "distance": 95,
            "lastRace": 96,
            "pedigree": 88
        },
        "comment": "欧州キングジョージ覇者の世界的強豪。日本の高速芝への適応が鍵も、名手スミヨン騎手とのコンビは脅威。"
    },
    {
        "rank": 7,
        "gate": 7,
        "waku": 4,
        "horseName": "カランダガン",
        "sexAge": "セ5",
        "load": 58,
        "jockey": "M.バルザローナ",
        "trainer": "Ｆ.グラファール (仏)",
        "odds": "14.8",
        "pop": 7,
        "totalScore": 87,
        "stars": "★★★★☆",
        "factors": {
            "workout": 88,
            "jockey": 93,
            "course": 81,
            "distance": 94,
            "lastRace": 92,
            "pedigree": 87
        },
        "comment": "英チャンピオンS2着。中長距離の地力は世界トップレベル。バルザローナ騎手の手綱で一発警戒。"
    },
    {
        "rank": 8,
        "gate": 8,
        "waku": 4,
        "horseName": "メイショウタバル",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "武豊",
        "trainer": "石橋守 (栗東)",
        "odds": "21.0",
        "pop": 8,
        "totalScore": 85,
        "stars": "★★★☆☆",
        "factors": {
            "workout": 91,
            "jockey": 96,
            "course": 83,
            "distance": 84,
            "lastRace": 88,
            "pedigree": 85
        },
        "comment": "単騎逃げが叶えば武豊騎手の絶妙なペース配分で波乱を巻き起こす可能性十分。ゴールドシップ産駒の底力に期待。"
    },
    {
        "rank": 9,
        "gate": 9,
        "waku": 5,
        "horseName": "コスモキュランダ",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "丹内祐次",
        "trainer": "加藤士津八 (美浦)",
        "odds": "28.5",
        "pop": 9,
        "totalScore": 83,
        "stars": "★★★☆☆",
        "factors": {
            "workout": 85,
            "jockey": 84,
            "course": 86,
            "distance": 85,
            "lastRace": 86,
            "pedigree": 84
        },
        "comment": "皐月賞2着の実績。持久力勝負になれば浮上の余地あり。"
    },
    {
        "rank": 10,
        "gate": 10,
        "waku": 5,
        "horseName": "ファイアンクランツ",
        "sexAge": "牡4",
        "load": 58,
        "jockey": "菅原明良",
        "trainer": "堀宣行 (美浦)",
        "odds": "34.0",
        "pop": 10,
        "totalScore": 81,
        "stars": "★★★☆☆",
        "factors": {
            "workout": 84,
            "jockey": 85,
            "course": 84,
            "distance": 83,
            "lastRace": 80,
            "pedigree": 86
        },
        "comment": "ドゥラメンテ産駒で距離延長歓迎。入念な乗り込みで仕上がり良好。"
    },
    {
        "rank": 11,
        "gate": 11,
        "waku": 6,
        "horseName": "エシカルダイヤモンド",
        "sexAge": "セ6",
        "load": 58,
        "jockey": "坂井瑠星",
        "trainer": "Ｗ.マリンズ (愛)",
        "odds": "45.0",
        "pop": 11,
        "totalScore": 79,
        "stars": "★★★☆☆",
        "factors": {
            "workout": 82,
            "jockey": 90,
            "course": 78,
            "distance": 88,
            "lastRace": 82,
            "pedigree": 80
        },
        "comment": "愛遠征馬。豊富なスタミナを持ち坂井騎手が先行策から粘り込みを狙う。"
    },
    {
        "rank": 12,
        "gate": 12,
        "waku": 6,
        "horseName": "オンブズマン",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "W.ビュイック",
        "trainer": "Ｊ＆Ｔ.ゴスデン (英)",
        "odds": "52.0",
        "pop": 12,
        "totalScore": 78,
        "stars": "★★★☆☆",
        "factors": {
            "workout": 82,
            "jockey": 92,
            "course": 76,
            "distance": 84,
            "lastRace": 85,
            "pedigree": 81
        },
        "comment": "名門ゴスデン厩舎の刺客。ビュイック騎手の手綱でどこまで迫れるか。"
    },
    {
        "rank": 13,
        "gate": 13,
        "waku": 7,
        "horseName": "タガノデュード",
        "sexAge": "牡5",
        "load": 58,
        "jockey": "M.デムーロ",
        "trainer": "宮徹 (栗東)",
        "odds": "68.0",
        "pop": 13,
        "totalScore": 76,
        "stars": "★★☆☆☆",
        "factors": {
            "workout": 78,
            "jockey": 86,
            "course": 77,
            "distance": 79,
            "lastRace": 76,
            "pedigree": 75
        },
        "comment": "重賞戦線で揉まれてきたが、G1の超一線級相手では展開の助けが必要。"
    },
    {
        "rank": 14,
        "gate": 14,
        "waku": 7,
        "horseName": "エキサイトバイオ",
        "sexAge": "牡4",
        "load": 58,
        "jockey": "荻野極",
        "trainer": "今野貞一 (栗東)",
        "odds": "85.0",
        "pop": 14,
        "totalScore": 75,
        "stars": "★★☆☆☆",
        "factors": {
            "workout": 77,
            "jockey": 78,
            "course": 80,
            "distance": 82,
            "lastRace": 75,
            "pedigree": 79
        },
        "comment": "レイデオロ産駒で東京2400m適性はあるが、地力差は否めない。"
    },
    {
        "rank": 15,
        "gate": 15,
        "waku": 7,
        "horseName": "ヴェルテンベルク",
        "sexAge": "牡6",
        "load": 58,
        "jockey": "横山典弘",
        "trainer": "宮本博 (栗東)",
        "odds": "110.0",
        "pop": 15,
        "totalScore": 74,
        "stars": "★★☆☆☆",
        "factors": {
            "workout": 76,
            "jockey": 88,
            "course": 76,
            "distance": 80,
            "lastRace": 74,
            "pedigree": 80
        },
        "comment": "横山典騎手の手腕で後方一気にかけるが、入着までが現実的か。"
    },
    {
        "rank": 16,
        "gate": 16,
        "waku": 8,
        "horseName": "ミニーホーク",
        "sexAge": "牝4",
        "load": 56,
        "jockey": "R.ムーア",
        "trainer": "Ａ.オブライエン (愛)",
        "odds": "125.0",
        "pop": 16,
        "totalScore": 73,
        "stars": "★★☆☆☆",
        "factors": {
            "workout": 80,
            "jockey": 96,
            "course": 72,
            "distance": 80,
            "lastRace": 74,
            "pedigree": 82
        },
        "comment": "ムーア騎手騎乗も日本の超高速馬場への対応は楽ではない。"
    },
    {
        "rank": 17,
        "gate": 17,
        "waku": 8,
        "horseName": "シェイクユアハート",
        "sexAge": "牡6",
        "load": 58,
        "jockey": "古川吉洋",
        "trainer": "宮徹 (栗東)",
        "odds": "150.0",
        "pop": 17,
        "totalScore": 71,
        "stars": "★★☆☆☆",
        "factors": {
            "workout": 74,
            "jockey": 76,
            "course": 74,
            "distance": 78,
            "lastRace": 72,
            "pedigree": 78
        },
        "comment": "ハーツクライ産駒でスタミナはあるが、スピード決着では苦しい。"
    },
    {
        "rank": 18,
        "gate": 18,
        "waku": 8,
        "horseName": "テアオ",
        "sexAge": "牡4",
        "load": 58,
        "jockey": "Ｆ.トーレス",
        "trainer": "Ｊ.サドラー (米)",
        "odds": "180.0",
        "pop": 18,
        "totalScore": 70,
        "stars": "★★☆☆☆",
        "factors": {
            "workout": 72,
            "jockey": 78,
            "course": 70,
            "distance": 74,
            "lastRace": 70,
            "pedigree": 75
        },
        "comment": "米遠征馬。芝適性に課題を残し追走に苦労しそう。"
    }
]

# Update Race 19 in prediction_data
pred_data['races']['19']['starters'] = japan_cup_starters
pred_data['races']['19']['contenderRanking'] = contender_ranking_19
pred_data['races']['19']['entryStatus'] = 'gate_confirmed'

# Also update top-level starters
pred_data['starters'] = japan_cup_starters
pred_data['contenderRanking'] = contender_ranking_19
pred_data['entryStatus'] = 'gate_confirmed'

with open(pred_json_path, 'w', encoding='utf-8') as f:
    json.dump(pred_data, f, ensure_ascii=False, indent=2)

pred_js_path = os.path.join(SRC_DIR, 'prediction_data.js')
with open(pred_js_path, 'w', encoding='utf-8') as f:
    f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')

print("Updated prediction_data.json and prediction_data.js: activeRaceId is now 19 (Japan Cup).")
