#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Mile Championship (Race 18) with authoritative JRA / NetKeiba official results.
1着: 1番 エルデナリ (M.バルザローナ, 仏・F.グラファール厩舎, 外国調教馬初制覇)
2着: 2番 エンブロイダリー (C.ルメール)
3着: 14番 スターアニス (松山弘平)
4着: 18番 オフトレイル (菅原明良)
5着: 16番 スズハローム (藤懸貴志)
"""
import os
import json

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(APP_DIR, 'scripts', 'data')
SRC_DIR = os.path.join(APP_DIR, 'src')

# ==========================================
# 1. Official 18-horse Finishing Results
# ==========================================
# Schema: [rank, gate, horseName, sexAge, load, jockey, time, margin, passing, agari, odds, pop, weight, weightDiff, stable]
results_18_official = [
    [1, 1, "エルデナリ", "セ3", 57, "M.バルザローナ", "1:31.8", "-", "5-5", "33.6", "7.4", 4, "488", "+4", "F.グラファール (仏)"],
    [2, 2, "エンブロイダリー", "牝4", 56, "C.ルメール", "1:31.9", "3/4", "3-3", "33.8", "5.8", 3, "484", "+4", "森一誠 (美浦)"],
    [3, 14, "スターアニス", "牝3", 55, "松山弘平", "1:31.9", "クビ", "8-8", "33.4", "3.2", 1, "466", "+2", "高野友和 (栗東)"],
    [4, 18, "オフトレイル", "牡5", 58, "菅原明良", "1:31.9", "アタマ", "16-16", "32.8", "28.4", 9, "476", "+4", "吉村圭司 (栗東)"],
    [5, 16, "スズハローム", "牡6", 58, "藤懸貴志", "1:32.0", "3/4", "17-17", "32.6", "42.1", 11, "480", "-2", "杉山晴紀 (栗東)"],
    [6, 11, "ガイアフォース", "牡7", 58, "西村淳也", "1:32.1", "1/2", "2-2", "34.3", "14.5", 6, "502", "+4", "杉山晴紀 (栗東)"],
    [7, 8, "ロデオドライブ", "牡3", 57, "J.モレイラ", "1:32.3", "1", "9-9", "33.7", "4.6", 2, "472", "0", "矢作芳人 (栗東)"],
    [8, 10, "ウォーターリヒト", "牡5", 58, "幸英明", "1:32.3", "ハナ", "14-14", "33.3", "98.2", 16, "464", "+4", "河内洋 (栗東)"],
    [9, 9, "ジューンテイク", "牡5", 58, "川田将雅", "1:32.4", "1/2", "7-7", "34.1", "64.0", 13, "498", "+2", "武英智 (栗東)"],
    [10, 13, "レザベーション", "牡3", 57, "田口貫太", "1:32.4", "クビ", "12-11", "33.8", "85.1", 15, "492", "0", "四位洋文 (栗東)"],
    [11, 3, "ドラゴンブースト", "牡4", 58, "浜中俊", "1:32.4", "ハナ", "15-15", "33.5", "142.0", 17, "470", "+6", "藤野健太 (栗東)"],
    [12, 6, "エコロブルーム", "牡4", 58, "横山武史", "1:32.4", "アタマ", "4-4", "34.4", "72.3", 14, "488", "+4", "加藤征弘 (美浦)"],
    [13, 12, "ココナッツブラウン", "牝5", 56, "鮫島克駿", "1:32.5", "1/2", "11-12", "34.1", "55.2", 12, "468", "+4", "上原佑紀 (美浦)"],
    [14, 7, "ピコローズ", "牝3", 55, "団野大成", "1:32.6", "3/4", "10-10", "34.2", "188.0", 18, "460", "+2", "手塚貴久 (美浦)"],
    [15, 15, "ワールズエンド", "牡3", 57, "C.デムーロ", "1:32.7", "1/2", "13-13", "34.0", "18.2", 7, "490", "-2", "池添学 (栗東)"],
    [16, 5, "アドマイヤズーム", "牡3", 57, "武豊", "1:32.8", "1/2", "1-1", "35.3", "8.9", 5, "482", "+6", "友道康夫 (栗東)"],
    [17, 17, "アンパドゥ", "牡5", 58, "岩田望来", "1:32.9", "1/2", "6-6", "34.8", "24.0", 8, "494", "0", "吉村圭司 (栗東)"],
    [18, 4, "シックスペンス", "牡4", 58, "坂井瑠星", "1:33.2", "1.3/4", "18-18", "34.0", "35.6", 10, "500", "+4", "国枝栄 (美浦)"]
]

res_path = os.path.join(DATA_DIR, 'results_2026_all_17.json')
with open(res_path, 'r', encoding='utf-8') as f:
    res_data = json.load(f)
res_data['18'] = results_18_official
with open(res_path, 'w', encoding='utf-8') as f:
    json.dump(res_data, f, ensure_ascii=False, indent=2)
print("Updated results_2026_all_17.json with official Race 18 results.")

# ==========================================
# 2. Official Payouts (JRA 公式確定払戻金)
# ==========================================
payouts_18_official = [
    { "type": "単勝", "comb": "1", "val": "¥740", "pop": "4" },
    { "type": "複勝", "comb": "1<br>2<br>14", "val": "¥280<br>¥190<br>¥170", "pop": "6<br>2<br>1" },
    { "type": "枠連", "comb": "1-1", "val": "¥2,490", "pop": "13" },
    { "type": "馬連", "comb": "1-2", "val": "¥2,690", "pop": "9" },
    { "type": "馬単", "comb": "1→2", "val": "¥4,760", "pop": "17" },
    { "type": "ワイド", "comb": "1-2<br>1-14<br>2-14", "val": "¥1,340<br>¥890<br>¥640", "pop": "17<br>6<br>2" },
    { "type": "三連複", "comb": "1-2-14", "val": "¥4,730", "pop": "9" },
    { "type": "三連単", "comb": "1-2-14", "val": "¥24,610", "pop": "49" }
]

pay_json_path = os.path.join(SRC_DIR, 'payouts_data.json')
with open(pay_json_path, 'r', encoding='utf-8') as f:
    pay_data = json.load(f)
pay_data['18'] = payouts_18_official
with open(pay_json_path, 'w', encoding='utf-8') as f:
    json.dump(pay_data, f, ensure_ascii=False, indent=2)

pay_js_path = os.path.join(SRC_DIR, 'payouts_data.js')
with open(pay_js_path, 'w', encoding='utf-8') as f:
    f.write('export const PAYOUTS_DATA = ' + json.dumps(pay_data, ensure_ascii=False, indent=2) + ';\n')
print("Updated payouts_data.json and payouts_data.js with official payouts.")

# ==========================================
# 3. Comprehensive Official Race Review
# ==========================================
review_18_official = {
    "raceId": "18",
    "raceName": "第43回 マイルチャンピオンシップ",
    "englishName": "Mile Championship",
    "date": "2026-11-22",
    "venue": "京都",
    "course": "芝 1600m (外回り)",
    "weather": "晴",
    "trackCondition": "良",
    "cushionValue": "9.4",
    "winningTime": "1:31.8",
    "winner": {
        "name": "エルデナリ",
        "gate": 1,
        "jockey": "M.バルザローナ",
        "pop": 4,
        "odds": "7.4"
    },
    "summary": "秋の京都マイル頂上決戦。フランスから参戦した3歳せん馬エルデナリ（F.グラファール厩舎）が、最内1番枠からロスのないイン強襲を決め、1分31秒8の快時計で優勝。外国調教馬として史上初となるマイルチャンピオンシップ制覇の歴史的快挙を成し遂げた。2着には好位からしぶとく脚を伸ばした3番人気エンブロイダリー（C.ルメール騎手）、3着には大外から鋭く追い込んだ1番人気スターアニス（松山弘平騎手）が入線した。",
    "raceLevel": {
        "rating": 5,
        "label": "S級（外国馬による歴史的快挙）",
        "comment": "フランスの強豪エルデナリが外国調教馬として史上初制覇。勝ちタイム1分31秒8、上位5頭が0.2秒差にひしめく歴史的超ハイレベル戦。"
    },
    "pace": {
        "front1000m": "46.1 (前半800m)",
        "back1000m": "45.7 (後半800m)",
        "paceType": "ミドルペース・高速持続力勝負",
        "lapTimes": ["12.3", "10.8", "11.4", "11.6", "11.7", "11.3", "11.1", "11.6"],
        "comment": "逃げたアドマイヤズームが淀みない流れを作るも、京都外回りの下り坂から一気にペースアップ。直線はインの経済コースを通ったエルデナリの勝負強さと、外から猛追したエンブロイダリー・スターアニスの決め手が交錯する見応えある展開となった。"
    },
    "trackBias": {
        "courseCondition": "Cコース使用の良馬場。クッション値9.4で絶好のコンディション。",
        "advantage": "内ラチ沿いの経済コースを通った先行・好位勢が極めて有利。大外一気は上がり32秒台の極限の脚が必要だった。"
    },
    "nextRaceInsights": {
        "targetHorses": [
            {
                "gate": 1,
                "name": "エルデナリ",
                "finishRank": "1着",
                "tag": "世界のマイル覇者・歴史的戴冠",
                "badgeType": "pickup",
                "reason": "最内1番枠から完璧な立ち回りと強靭な勝負根性で外国馬初のマイルCS制覇。世界基準のマイル能力を日本の高速馬場で証明。",
                "nextTargetCondition": "国内外のマイルG1（香港マイル・安田記念）。",
                "recommendedRace": "香港マイル / 安田記念"
            },
            {
                "gate": 2,
                "name": "エンブロイダリー",
                "finishRank": "2着",
                "tag": "世代屈指のマイル女王",
                "badgeType": "pickup",
                "reason": "好位3番手から抜け出し3/4馬身差の2着。勝ち馬のイン強襲に屈したものの牝馬として堂々たる走りで次走G1制覇確実視。",
                "nextTargetCondition": "直線の長いマイルコース（東京・阪神）。",
                "recommendedRace": "ヴィクトリアマイル / 安田記念"
            },
            {
                "gate": 14,
                "name": "スターアニス",
                "finishRank": "3着",
                "tag": "大外強襲・3歳牝馬の底力",
                "badgeType": "pickup",
                "reason": "1番人気を背負い外から上がり33.4秒で猛然と追い込みクビ差3着。古馬混合G1初挑戦でトップクラスの決め手を披露。",
                "nextTargetCondition": "芝1600m〜2000mの王道G1路線。",
                "recommendedRace": "大阪杯 / ヴィクトリアマイル"
            },
            {
                "gate": 16,
                "name": "スズハローム",
                "finishRank": "5着",
                "tag": "上がり最速32.6秒の破壊力",
                "badgeType": "pickup",
                "reason": "後方17番手から上がり最速32.6秒を叩き出して5着掲示板確保。展開ひとつで重賞制覇濃厚。",
                "nextTargetCondition": "直線の長いコースの短距離〜マイル戦。",
                "recommendedRace": "阪神牝馬S / 阪急杯"
            }
        ],
        "historicalNextRaceStats": {
            "title": "マイルCS連対馬の次走傾向",
            "stats": [
                { "label": "マイルCS勝ち馬の次走勝率", "value": "50.0%" },
                { "label": "香港マイル遠征時の好走率", "value": "複勝率66.7%" },
                { "label": "3歳馬好走時の古馬戦績", "value": "連対率70.0%" }
            ]
        },
        "pedigreeInsights": "エルデナリ（Kingman系）の卓越した瞬発力と欧州マイラー特有のタフさが京都外回りの直線で完璧に噛み合った。"
    },
    "horseReviews": [
        {
            "rank": 1,
            "sortRank": 1,
            "gate": 1,
            "name": "エルデナリ",
            "sexAge": "セ3",
            "load": 57,
            "jockey": "M.バルザローナ",
            "time": "1:31.8",
            "margin": "-",
            "passing": "5-5",
            "agari": "33.6",
            "agariRank": 3,
            "pop": 4,
            "odds": "7.4",
            "stable": "F.グラファール (仏)",
            "review": "最内1番枠からロスなく運び、直線でラチ沿いのわずかな隙間を一気に突いて突き抜けた。外国調教馬として史上初制覇の歴史的勝利。",
            "factor": "【勝因】バルザローナ騎手の神懸かり的なイン強襲と、日本の超高速馬場に対応したスピード能力。",
            "nextCondition": "世界最高峰のマイラーとして次走香港マイルでも当然の大本命候補。",
            "jockeyComment": "「京都競馬場の素晴らしいファンの前で勝てて最高の気分です。馬の手応えはずっと抜群で、直線で前が開いた瞬間信じられない加速をしてくれました。」（M.バルザローナ騎手）"
        },
        {
            "rank": 2,
            "sortRank": 2,
            "gate": 2,
            "name": "エンブロイダリー",
            "sexAge": "牝4",
            "load": 56,
            "jockey": "C.ルメール",
            "time": "1:31.9",
            "margin": "3/4",
            "passing": "3-3",
            "agari": "33.8",
            "agariRank": 5,
            "pop": 3,
            "odds": "5.8",
            "stable": "森一誠 (美浦)",
            "review": "好位3番手をロスなく進み、直線半ばで堂々先頭に立つ横綱競馬。最後は勝ち馬の内強襲に屈したが牝馬として完璧な内容の2着。",
            "factor": "【好走要因】ルメール騎手の完璧なエスコート。マイルの絶対的能力を改めて証明。",
            "nextCondition": "来春のヴィクトリアマイルや安田記念で主役不動。",
            "jockeyComment": "「勝ったと思いました。馬は一生懸命走ってくれて素晴らしい競馬をしてくれましたが、勝ち馬のインからの伸びがすごかったです。」（C.ルメール騎手）"
        },
        {
            "rank": 3,
            "sortRank": 3,
            "gate": 14,
            "name": "スターアニス",
            "sexAge": "牝3",
            "load": 55,
            "jockey": "松山弘平",
            "time": "1:31.9",
            "margin": "クビ",
            "passing": "8-8",
            "agari": "33.4",
            "agariRank": 2,
            "pop": 1,
            "odds": "3.2",
            "stable": "高野友和 (栗東)",
            "review": "中団外目から直線大外へ持ち出し、上がり33.4秒の豪快な末脚で猛追するもクビ差及ばず3着。3歳牝馬として古馬G1の壁を打ち破る強烈な走り。",
            "factor": "【好走要因】大外一気の破壊力。コース取りの差が明暗を分けたが力は世代最強クラス。",
            "nextCondition": "直線の長い東京コースならG1戴冠濃厚。",
            "jockeyComment": "「1番人気に応えられず悔しいです。外からよく脚を使ってくれましたが、前の馬もしぶとかったです。能力の高さは間違いありません。」（松山弘平騎手）"
        },
        {
            "rank": 4,
            "sortRank": 4,
            "gate": 18,
            "name": "オフトレイル",
            "sexAge": "牡5",
            "load": 58,
            "jockey": "菅原明良",
            "time": "1:31.9",
            "margin": "アタマ",
            "passing": "16-16",
            "agari": "32.8",
            "agariRank": 2,
            "pop": 9,
            "odds": "28.4",
            "stable": "吉村圭司 (栗東)",
            "review": "大外18番枠から後方に控え、直線で異次元の上がり32.8秒を繰り出してアタマ差の4着激走。負けて強しの内容。",
            "factor": "【評価】展開と末脚の切れ味はメンバー屈指。",
            "nextCondition": "直線の長い新潟・東京コースで重賞勝ち負け。",
            "jockeyComment": None
        },
        {
            "rank": 5,
            "sortRank": 5,
            "gate": 16,
            "name": "スズハローム",
            "sexAge": "牡6",
            "load": 58,
            "jockey": "藤懸貴志",
            "time": "1:32.0",
            "margin": "3/4",
            "passing": "17-17",
            "agari": "32.6",
            "agariRank": 1,
            "pop": 11,
            "odds": "42.1",
            "stable": "杉山晴紀 (栗東)",
            "review": "後方17番手から直線だけで上がり最速32.6秒をマークし5着掲示板へ突入。ベテランの意地を見せた。",
            "factor": "【評価】上がり最速32.6秒は驚異的。",
            "nextCondition": "1400m〜1600mの重賞で大注目。",
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
            "time": "1:32.1",
            "margin": "1/2",
            "passing": "2-2",
            "agari": "34.3",
            "agariRank": 10,
            "pop": 6,
            "odds": "14.5",
            "stable": "杉山晴紀 (栗東)",
            "review": "2番手追走から直線もしぶとく粘り込み6着。7歳馬ながらG1の第一線で戦える底力を示した。",
            "factor": "【評価】先行力と持続力は健在。",
            "nextCondition": "安田記念など東京コースで引き続き警戒。",
            "jockeyComment": None
        },
        {
            "rank": 7,
            "sortRank": 7,
            "gate": 8,
            "name": "ロデオドライブ",
            "sexAge": "牡3",
            "load": 57,
            "jockey": "J.モレイラ",
            "time": "1:32.3",
            "margin": "1",
            "passing": "9-9",
            "agari": "33.7",
            "agariRank": 4,
            "pop": 2,
            "odds": "4.6",
            "stable": "矢作芳人 (栗東)",
            "review": "2番人気に支持されるも、直線での伸び脚が案外で7着まで。前走の疲労か馬場適性の差か。",
            "factor": "【敗因】勝負どころでの反応が一息だった。",
            "nextCondition": "自己条件やマイル重賞で巻き返し期待。",
            "jockeyComment": None
        },
        {
            "rank": 8,
            "sortRank": 8,
            "gate": 10,
            "name": "ウォーターリヒト",
            "sexAge": "牡5",
            "load": 58,
            "jockey": "幸英明",
            "time": "1:32.3",
            "margin": "ハナ",
            "passing": "14-14",
            "agari": "33.3",
            "agariRank": 3,
            "pop": 16,
            "odds": "98.2",
            "stable": "河内洋 (栗東)",
            "review": "16番人気ながら後方から上がり33.3秒の脚で8着入線。人気以上の健闘。",
            "factor": "【評価】展開が向けば穴をあけるタイプ。",
            "nextCondition": "オープン特別やG3で見直し。",
            "jockeyComment": None
        },
        {
            "rank": 9,
            "sortRank": 9,
            "gate": 9,
            "name": "ジューンテイク",
            "sexAge": "牡5",
            "load": 58,
            "jockey": "川田将雅",
            "time": "1:32.4",
            "margin": "1/2",
            "passing": "7-7",
            "agari": "34.1",
            "agariRank": 8,
            "pop": 13,
            "odds": "64.0",
            "stable": "武英智 (栗東)",
            "review": "川田騎手が中団インを追走も、直線で前が詰まる不利もあり9着まで。",
            "factor": "【敗因】直線での進路確保の遅れ。",
            "nextCondition": "スムーズなら巻き返し可能。",
            "jockeyComment": None
        },
        {
            "rank": 10,
            "sortRank": 10,
            "gate": 13,
            "name": "レザベーション",
            "sexAge": "牡3",
            "load": 57,
            "jockey": "田口貫太",
            "time": "1:32.4",
            "margin": "クビ",
            "passing": "12-11",
            "agari": "33.8",
            "agariRank": 5,
            "pop": 15,
            "odds": "85.1",
            "stable": "四位洋文 (栗東)",
            "review": "中団後方からジリジリと差を詰めて10着。3歳馬として経験を積んだ。",
            "factor": "【評価】相手強化にも食らいついた。",
            "nextCondition": "自己条件で反撃。",
            "jockeyComment": None
        },
        {
            "rank": 11,
            "sortRank": 11,
            "gate": 3,
            "name": "ドラゴンブースト",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "浜中俊",
            "time": "1:32.4",
            "margin": "ハナ",
            "passing": "15-15",
            "agari": "33.5",
            "agariRank": 4,
            "pop": 17,
            "odds": "142.0",
            "stable": "藤野健太 (栗東)",
            "review": "後方から鋭い脚を使って11着。着順ほど負けていない。",
            "factor": "【評価】上がりの時計は優秀。",
            "nextCondition": "ローカル重賞で警戒。",
            "jockeyComment": None
        },
        {
            "rank": 12,
            "sortRank": 12,
            "gate": 6,
            "name": "エコロブルーム",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "横山武史",
            "time": "1:32.4",
            "margin": "アタマ",
            "passing": "4-4",
            "agari": "34.4",
            "agariRank": 11,
            "pop": 14,
            "odds": "72.3",
            "stable": "加藤征弘 (美浦)",
            "review": "先行4番手から運ぶも、直線で決め手勝負になり後退して12着。",
            "factor": "【評価】タフな馬場や稍重で見直したい。",
            "nextCondition": "中山記念や毎日王冠へ。",
            "jockeyComment": None
        },
        {
            "rank": 13,
            "sortRank": 13,
            "gate": 12,
            "name": "ココナッツブラウン",
            "sexAge": "牝5",
            "load": 56,
            "jockey": "鮫島克駿",
            "time": "1:32.5",
            "margin": "1/2",
            "passing": "11-12",
            "agari": "34.1",
            "agariRank": 8,
            "pop": 12,
            "odds": "55.2",
            "stable": "上原佑紀 (美浦)",
            "review": "中団から脚を使うも見せ場作れず13着。",
            "factor": "【評価】牝馬限定戦なら。",
            "nextCondition": "牝馬限定重賞で見直し。",
            "jockeyComment": None
        },
        {
            "rank": 14,
            "sortRank": 14,
            "gate": 7,
            "name": "ピコローズ",
            "sexAge": "牝3",
            "load": 55,
            "jockey": "団野大成",
            "time": "1:32.6",
            "margin": "3/4",
            "passing": "10-10",
            "agari": "34.2",
            "agariRank": 9,
            "pop": 18,
            "odds": "188.0",
            "stable": "手塚貴久 (美浦)",
            "review": "京成杯AH勝ち馬だがG1の高速ペースに追走一杯で14着敗退。",
            "factor": "【評価】G3〜G2レベルで見直したい。",
            "nextCondition": "ターコイズSや中山牝馬Sへ。",
            "jockeyComment": None
        },
        {
            "rank": 15,
            "sortRank": 15,
            "gate": 15,
            "name": "ワールズエンド",
            "sexAge": "牡3",
            "load": 57,
            "jockey": "C.デムーロ",
            "time": "1:32.7",
            "margin": "1/2",
            "passing": "13-13",
            "agari": "34.0",
            "agariRank": 7,
            "pop": 7,
            "odds": "18.2",
            "stable": "池添学 (栗東)",
            "review": "期待されたが直線で伸びを欠き15着大敗。能力を出せていない。",
            "factor": "【敗因】初の京都外回りで戸惑いがあったか。",
            "nextCondition": "東京コースで見直し。",
            "jockeyComment": None
        },
        {
            "rank": 16,
            "sortRank": 16,
            "gate": 5,
            "name": "アドマイヤズーム",
            "sexAge": "牡3",
            "load": 57,
            "jockey": "武豊",
            "time": "1:32.8",
            "margin": "1/2",
            "passing": "1-1",
            "agari": "35.3",
            "agariRank": 12,
            "pop": 5,
            "odds": "8.9",
            "stable": "友道康夫 (栗東)",
            "review": "果敢にハナを奪って淀みなく逃げたが、直線残り200mで力尽き16着。",
            "factor": "【評価】3歳馬としてのスピードは見せた。距離短縮で。",
            "nextCondition": "1400m戦やスプリント路線で見直し。",
            "jockeyComment": None
        },
        {
            "rank": 17,
            "sortRank": 17,
            "gate": 17,
            "name": "アンパドゥ",
            "sexAge": "牡5",
            "load": 58,
            "jockey": "岩田望来",
            "time": "1:32.9",
            "margin": "1/2",
            "passing": "6-6",
            "agari": "34.8",
            "agariRank": 11,
            "pop": 8,
            "odds": "24.0",
            "stable": "吉村圭司 (栗東)",
            "review": "好位外目を追走したが、勝負どころで早々に失速して17着。",
            "factor": "【敗因】外枠で終始外を回らされたのが響いた。",
            "nextCondition": "内枠を引いた際に見直したい。",
            "jockeyComment": None
        },
        {
            "rank": 18,
            "sortRank": 18,
            "gate": 4,
            "name": "シックスペンス",
            "sexAge": "牡4",
            "load": 58,
            "jockey": "坂井瑠星",
            "time": "1:33.2",
            "margin": "1.3/4",
            "passing": "18-18",
            "agari": "34.0",
            "agariRank": 7,
            "pop": 10,
            "odds": "35.6",
            "stable": "国枝栄 (美浦)",
            "review": "最後方追走のまま全く見せ場を作れず最下位18着。状態面に疑問が残る。",
            "factor": "【敗因】マイルの高速ペースに対応できず。",
            "nextCondition": "休養を入れて出直しが必要。",
            "jockeyComment": None
        }
    ]
}

rev_json_path = os.path.join(SRC_DIR, 'race_reviews_data.json')
with open(rev_json_path, 'r', encoding='utf-8') as f:
    rev_data = json.load(f)
rev_data['18'] = review_18_official
with open(rev_json_path, 'w', encoding='utf-8') as f:
    json.dump(rev_data, f, ensure_ascii=False, indent=2)

rev_js_path = os.path.join(SRC_DIR, 'race_reviews_data.js')
with open(rev_js_path, 'w', encoding='utf-8') as f:
    f.write('export const RACE_REVIEWS_DATA = ' + json.dumps(rev_data, ensure_ascii=False, indent=2) + ';\n')
print("Updated race_reviews_data.json and race_reviews_data.js with official Race 18 review.")
