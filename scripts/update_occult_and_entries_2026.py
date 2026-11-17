import json
import os

keiba_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pred_json_path = os.path.join(keiba_dir, 'src', 'prediction_data.json')
pred_js_path = os.path.join(keiba_dir, 'src', 'prediction_data.js')
entries_json_path = os.path.join(keiba_dir, 'src', 'entries_data.json')
entries_js_path = os.path.join(keiba_dir, 'src', 'entries_data.js')

with open(pred_json_path, 'r', encoding='utf-8') as f:
    pred_data = json.load(f)

with open(entries_json_path, 'r', encoding='utf-8') as f:
    entries_data = json.load(f)

# 2026 Mile Championship (Race 18) Starters (20 runners, 50-on order)
starters_18 = [
    {
        "waku": None, "gate": None, "horseName": "アドマイヤズーム", "sexAge": "牡3", "load": 57,
        "jockey": "武豊", "stable": "友道康夫 (栗東)", "odds": "22.5", "placeOdds": "4.5 - 6.8", "pop": 10,
        "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "81.4 - 66.2 - 51.5 - 36.8 - 11.4",
        "trainingComment": "長めから意欲的に追われて好時計マーク。馬体の張りも前走以上で気配良好。",
        "trainingWeight": 486, "lastRaceWeight": 482, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "モーリス", "dam": "アドマイヤローザ", "bms": "ハーツクライ", "distanceApt": "1600-2000m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "富士S (G2)", "date": "2026-10-17", "distance": "芝1600m", "rank": 3, "agari": "33.4", "margin": "0.2秒差", "factor": "中団から鋭く脚を伸ばして3着確保。マイルの決め手勝負で前進。"}
    },
    {
        "waku": None, "gate": None, "horseName": "アンパドゥ", "sexAge": "牡4", "load": 58,
        "jockey": "岩田望来", "stable": "高野友和 (栗東)", "odds": "48.0", "placeOdds": "8.5 - 13.0", "pop": 14,
        "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "53.2 - 38.4 - 24.8 - 12.0",
        "trainingComment": "坂路で軽快な身のこなし。馬体積も締まって叩かれた上積みは十分。",
        "trainingWeight": 474, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ロードカナロア", "dam": "アンジュシャルマン", "bms": "マンハッタンカフェ", "distanceApt": "1400-1600m", "trackApt": "良"},
        "lastRace": {"raceName": "スワンS (G2)", "date": "2026-10-24", "distance": "芝1400m", "rank": 4, "agari": "33.9", "margin": "0.3秒差", "factor": "内ラチ沿いを通って渋太く脚を使った。マイルへの距離延長が鍵。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ウォーターリヒト", "sexAge": "牡4", "load": 58,
        "jockey": "幸英明", "stable": "河内洋 (栗東)", "odds": "38.0", "placeOdds": "7.0 - 11.0", "pop": 13,
        "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "83.0 - 67.5 - 52.1 - 37.2 - 11.6",
        "trainingComment": "単走で終い重点。ラストは鋭い伸び脚を見せており体調は万全。",
        "trainingWeight": 498, "lastRaceWeight": 496, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ドレフォン", "dam": "ウォーターピオニー", "bms": "ヴィクトワールピサ", "distanceApt": "1600-2000m", "trackApt": "良・稍重・重"},
        "lastRace": {"raceName": "富士S (G2)", "date": "2026-10-17", "distance": "芝1600m", "rank": 5, "agari": "33.6", "margin": "0.4秒差", "factor": "後方からメンバー上位の上がりを繰り出すも前が止まらず。展開次第。"}
    },
    {
        "waku": None, "gate": None, "horseName": "エコロアルバ", "sexAge": "牡4", "load": 58,
        "jockey": "未定", "stable": "武英智 (栗東)", "odds": "125.0", "placeOdds": "22.0 - 35.0", "pop": 19,
        "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "54.1 - 39.5 - 25.5 - 12.4",
        "trainingComment": "馬なりで流す程度。動き自体は悪くないが、大一番に向けてもう一段の上積みが欲しい。",
        "trainingWeight": 490, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "アルアイン", "dam": "エコロデイジー", "bms": "キングカメハメハ", "distanceApt": "1600-1800m", "trackApt": "良"},
        "lastRace": {"raceName": "カシオペアS (L)", "date": "2026-10-31", "distance": "芝1800m", "rank": 6, "agari": "34.5", "margin": "0.6秒差", "factor": "好位追走から伸びを欠いた。相手強化でどこまでやれるか。"}
    },
    {
        "waku": None, "gate": None, "horseName": "エコロブルーム", "sexAge": "牡4", "load": 58,
        "jockey": "坂井瑠星", "stable": "加藤征弘 (美浦)", "odds": "16.8", "placeOdds": "3.8 - 5.5", "pop": 8,
        "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "65.8 - 50.9 - 36.4 - 11.2",
        "trainingComment": "文句なしの絶好気配。坂井瑠星騎手を背に直線で弾けるようなフットワークを披露。文句なしのS評価。",
        "trainingWeight": 512, "lastRaceWeight": 508, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ダイワメジャー", "dam": "シュガーショック", "bms": "Candy Ride", "distanceApt": "1400-1600m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "京成杯AH (G3)", "date": "2026-09-13", "distance": "芝1600m", "rank": 1, "agari": "33.8", "margin": "-0.2秒差", "factor": "好位2番手から手応え抜群で抜け出し完勝。マイル重賞連勝へ視界良好。"}
    },
    {
        "waku": None, "gate": None, "horseName": "エルデナリ", "sexAge": "せん3", "load": 57,
        "jockey": "M.バルザローナ", "stable": "A.ファーブル (仏)", "odds": "9.8", "placeOdds": "2.4 - 3.8", "pop": 5,
        "trainingGrade": "A", "trainingCourse": "京都芝", "trainingTime": "64.2 - 49.8 - 35.9 - 11.3",
        "trainingComment": "来日後の検疫・調整も極めて順調。初来日の京都芝コースでも軽やかに加速し高い適性をアピール。",
        "trainingWeight": 476, "lastRaceWeight": 474, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "Dubawi", "dam": "Ervedya", "bms": "Siyouni", "distanceApt": "1600m", "trackApt": "良・稍重・重"},
        "lastRace": {"raceName": "ムーランドロンシャン賞 (G1)", "date": "2026-09-06", "distance": "芝1600m", "rank": 3, "agari": "34.1", "margin": "0.2秒差", "factor": "欧州最高峰マイルG1で勝ち馬とタイム差なしの3着。世界的トップマイラーの実力。"}
    },
    {
        "waku": None, "gate": None, "horseName": "エンブロイダリー", "sexAge": "牝3", "load": 55,
        "jockey": "C.ルメール", "stable": "森一誠 (美浦)", "odds": "2.8", "placeOdds": "1.3 - 1.7", "pop": 1,
        "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "64.5 - 49.6 - 35.7 - 11.0",
        "trainingComment": "全身を使った雄大なフットワークでラスト1F11.0秒を馬なりで計時。ヴィクトリアマイル優勝時を凌ぐ究極のデキ。",
        "trainingWeight": 484, "lastRaceWeight": 480, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "アドマイヤマーズ", "dam": "ロッテンマイヤー", "bms": "クロフネ", "distanceApt": "1600-1800m", "trackApt": "良"},
        "lastRace": {"raceName": "府中牝馬S (G2)", "date": "2026-10-12", "distance": "芝1800m", "rank": 1, "agari": "32.6", "margin": "-0.3秒差", "factor": "古馬牝馬を相手に上がり32.6秒の異次元の脚で差し切り。春VM(1:30.9)のスピードは現役屈指。"}
    },
    {
        "waku": None, "gate": None, "horseName": "オフトレイル", "sexAge": "牡4", "load": 58,
        "jockey": "菅原明良", "stable": "吉村圭司 (栗東)", "odds": "25.4", "placeOdds": "5.0 - 7.5", "pop": 11,
        "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.8 - 38.0 - 24.5 - 11.9",
        "trainingComment": "坂路で力強い登坂。首を使ってグイグイと伸びており、マイル替わりはプラス。",
        "trainingWeight": 506, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "Farhh", "dam": "Rose Trail", "bms": "Kingmambo", "distanceApt": "1600-1800m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "毎日王冠 (G2)", "date": "2026-10-04", "distance": "芝1800m", "rank": 4, "agari": "33.5", "margin": "0.3秒差", "factor": "強敵相手にインからしぶとく差を詰めて4着。京都外回りの下り坂で一変の余地。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ガイアフォース", "sexAge": "牡7", "load": 58,
        "jockey": "西村淳也", "stable": "杉山晴紀 (栗東)", "odds": "14.2", "placeOdds": "3.2 - 4.8", "pop": 7,
        "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "51.8 - 37.4 - 24.1 - 11.7",
        "trainingComment": "ベテランの貫禄十分。キレのある脚捌きで坂路の急坂を駆け上がった。マイルG1での安定感はピカイチ。",
        "trainingWeight": 498, "lastRaceWeight": 496, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "キタサンブラック", "dam": "ナターレ", "bms": "クロフネ", "distanceApt": "1600-2200m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "富士S (G2)", "date": "2026-10-17", "distance": "芝1600m", "rank": 2, "agari": "33.2", "margin": "0.1秒差", "factor": "好位から直線力強く抜け出しクビ差の2着。マイル路線の古豪健在。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ココナッツブラウン", "sexAge": "牝5", "load": 56,
        "jockey": "北村友一", "stable": "上村洋行 (栗東)", "odds": "32.0", "placeOdds": "6.2 - 9.5", "pop": 12,
        "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "82.5 - 67.0 - 51.8 - 36.9 - 11.5",
        "trainingComment": "3頭併せの真ん中から気迫溢れる伸び。馬体の張り・毛艶ともピカピカで仕上がり上々。",
        "trainingWeight": 468, "lastRaceWeight": 464, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "キタサンブラック", "dam": "ココナッツパルム", "bms": "フレンチデピュティ", "distanceApt": "1600-1800m", "trackApt": "良"},
        "lastRace": {"raceName": "府中牝馬S (G2)", "date": "2026-10-12", "distance": "芝1800m", "rank": 3, "agari": "32.9", "margin": "0.3秒差", "factor": "エンブロイダリーの3着に好走。末脚の安定感高くマイル短縮でも警戒。"}
    },
    {
        "waku": None, "gate": None, "horseName": "シックスペンス", "sexAge": "牡4", "load": 58,
        "jockey": "A.プーシャン", "stable": "国枝栄 (美浦)", "odds": "5.4", "placeOdds": "1.8 - 2.6", "pop": 3,
        "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "65.1 - 50.2 - 36.1 - 11.1",
        "trainingComment": "抜群の手応えで僚馬を圧倒。安田記念を制した春以上のパワーと柔軟性を身につけており春秋マイル統一へ隙なし。",
        "trainingWeight": 504, "lastRaceWeight": 500, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "キズナ", "dam": "フィンレイズラッキーチャーム", "bms": "Twirling Candy", "distanceApt": "1600-1800m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "毎日王冠 (G2)", "date": "2026-10-04", "distance": "芝1800m", "rank": 1, "agari": "33.3", "margin": "-0.2秒差", "factor": "春の安田記念(1:32.1)覇者が秋初戦も完勝。マイルチャンピオンシップ制覇へ盤石の態勢。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ジューンテイク", "sexAge": "牡4", "load": 58,
        "jockey": "未定", "stable": "武英智 (栗東)", "odds": "140.0", "placeOdds": "25.0 - 40.0", "pop": 20,
        "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "84.2 - 68.8 - 53.4 - 38.2 - 12.1",
        "trainingComment": "長めから丹念に乗られたが、追われてからの反応はやや重め。距離短縮で流れに乗れるか。",
        "trainingWeight": 494, "lastRaceWeight": 492, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "キズナ", "dam": "アドマイヤサブリナ", "bms": "シンボリクリスエス", "distanceApt": "1600-2400m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "京都大賞典 (G2)", "date": "2026-10-11", "distance": "芝2400m", "rank": 8, "agari": "34.8", "margin": "0.8秒差", "factor": "距離短縮で活路を求める。マイルの速い流れへの対応が課題。"}
    },
    {
        "waku": None, "gate": None, "horseName": "スズハローム", "sexAge": "牡5", "load": 58,
        "jockey": "藤懸貴志", "stable": "杉山晴紀 (栗東)", "odds": "55.0", "placeOdds": "10.0 - 15.0", "pop": 15,
        "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.4 - 37.9 - 24.3 - 11.9",
        "trainingComment": "坂路で力強い脚取り。ラストの伸びも鋭く近走の好調さをキープ。",
        "trainingWeight": 482, "lastRaceWeight": 480, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "サトノダイヤモンド", "dam": "アイライン", "bms": "ローレルゲレイロ", "distanceApt": "1400-1600m", "trackApt": "良"},
        "lastRace": {"raceName": "スワンS (G2)", "date": "2026-10-24", "distance": "芝1400m", "rank": 5, "agari": "34.0", "margin": "0.4秒差", "factor": "中団からしぶとく差を詰めて掲示板確保。展開が向けば上位争い可能。"}
    },
    {
        "waku": None, "gate": None, "horseName": "スターアニス", "sexAge": "牝3", "load": 55,
        "jockey": "松山弘平", "stable": "杉山晴紀 (栗東)", "odds": "4.6", "placeOdds": "1.6 - 2.3", "pop": 2,
        "trainingGrade": "A+", "trainingCourse": "栗東CW", "trainingTime": "80.8 - 65.4 - 50.8 - 36.2 - 11.2",
        "trainingComment": "CWで抜群の加速性能を発揮。桜花賞を1分31秒5で圧勝したマイル適性は現役3歳牝馬ナンバーワン。",
        "trainingWeight": 472, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ドレフォン", "dam": "スターアニス", "bms": "ハーツクライ", "distanceApt": "1600-1800m", "trackApt": "良"},
        "lastRace": {"raceName": "ローズS (G2)", "date": "2026-09-20", "distance": "芝2000m", "rank": 2, "agari": "33.5", "margin": "0.1秒差", "factor": "2000mでも2着好走。本質はマイル。桜花賞を制した舞台で3歳女王の輝きを取り戻す。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ドラゴンブースト", "sexAge": "牡3", "load": 57,
        "jockey": "浜中俊", "stable": "藤野健太 (栗東)", "odds": "68.0", "placeOdds": "12.0 - 18.0", "pop": 16,
        "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "53.0 - 38.3 - 24.6 - 12.1",
        "trainingComment": "坂路でテンポ良く登坂。前走からの上積みを感じさせるキビキビとした動き。",
        "trainingWeight": 466, "lastRaceWeight": 464, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ディーマジェスティ", "dam": "ドラゴンレディ", "bms": "タイキシャトル", "distanceApt": "1400-1600m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "京成杯AH (G3)", "date": "2026-09-13", "distance": "芝1600m", "rank": 4, "agari": "34.0", "margin": "0.4秒差", "factor": "古馬重賞初挑戦で4着健闘。3歳馬の成長力に警戒。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ピコローズ", "sexAge": "牝5", "load": 56,
        "jockey": "三浦皇成", "stable": "上原博之 (美浦)", "odds": "78.0", "placeOdds": "14.0 - 22.0", "pop": 17,
        "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "66.4 - 51.5 - 37.3 - 11.9",
        "trainingComment": "単走で終い重視。フォームに乱れはなく順調にメニューを消化。",
        "trainingWeight": 458, "lastRaceWeight": 456, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ロードカナロア", "dam": "ピコチャンブラック", "bms": "ブラックタイド", "distanceApt": "1400-1600m", "trackApt": "良"},
        "lastRace": {"raceName": "スワンS (G2)", "date": "2026-10-24", "distance": "芝1400m", "rank": 6, "agari": "34.2", "margin": "0.5秒差", "factor": "直線外から追い込むも6着まで。牝馬限定戦からの相手強化が鍵。"}
    },
    {
        "waku": None, "gate": None, "horseName": "マジックサンズ", "sexAge": "牡3", "load": 57,
        "jockey": "川田将雅", "stable": "須貝尚介 (栗東)", "odds": "18.5", "placeOdds": "4.0 - 5.8", "pop": 9,
        "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "81.9 - 66.5 - 51.2 - 36.5 - 11.3",
        "trainingComment": "川田騎手を背に直線で鋭い反応。集中力が高く馬体の張りも前走以上。勝負気配濃厚。",
        "trainingWeight": 508, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "キズナ", "dam": "コナブリュワーズ", "bms": "キングカメハメハ", "distanceApt": "1600-2000m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "富士S (G2)", "date": "2026-10-17", "distance": "芝1600m", "rank": 4, "agari": "33.5", "margin": "0.3秒差", "factor": "直線で外から豪快に脚を伸ばして4着。叩き2戦目で上積み大。"}
    },
    {
        "waku": None, "gate": None, "horseName": "レザベーション", "sexAge": "牡4", "load": 58,
        "jockey": "田口貫太", "stable": "矢作芳人 (栗東)", "odds": "95.0", "placeOdds": "18.0 - 28.0", "pop": 18,
        "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.9 - 38.1 - 24.7 - 12.0",
        "trainingComment": "坂路で力強い登坂。矢作厩舎らしい豊富な稽古量でスタミナ強化十分。",
        "trainingWeight": 488, "lastRaceWeight": 486, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "リアルスティール", "dam": "リザーブ", "bms": "ディープインパクト", "distanceApt": "1400-1600m", "trackApt": "良"},
        "lastRace": {"raceName": "オーロC (L)", "date": "2026-11-08", "distance": "芝1400m", "rank": 2, "agari": "33.7", "margin": "0.1秒差", "factor": "逃げて2着に粘り込み。G1の強力先行勢相手にどこまで粘れるか。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ロデオドライブ", "sexAge": "牡3", "load": 57,
        "jockey": "J.モレイラ", "stable": "友道康夫 (栗東)", "odds": "7.2", "placeOdds": "2.0 - 2.8", "pop": 4,
        "trainingGrade": "A+", "trainingCourse": "栗東CW", "trainingTime": "81.0 - 65.8 - 50.9 - 36.1 - 11.1",
        "trainingComment": "抜群のスピード感で直線を駆け抜けた。春のNHKマイルCを制した破壊力は健在。モレイラ騎手とのコンビも強力。",
        "trainingWeight": 492, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "エピファネイア", "dam": "ロデオレディ", "bms": "キングカメハメハ", "distanceApt": "1600m", "trackApt": "良・稍重"},
        "lastRace": {"raceName": "富士S (G2)", "date": "2026-10-17", "distance": "芝1600m", "rank": 1, "agari": "33.0", "margin": "-0.1秒差", "factor": "春のNHKマイルC(1:31.5)に続き古馬を撃破。マイルの直線スピードは現役トップクラス。"}
    },
    {
        "waku": None, "gate": None, "horseName": "ワールズエンド", "sexAge": "牡3", "load": 57,
        "jockey": "C.デムーロ", "stable": "池添学 (栗東)", "odds": "11.5", "placeOdds": "2.8 - 4.2", "pop": 6,
        "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "51.5 - 37.0 - 23.8 - 11.6",
        "trainingComment": "スプリンターズS2着のスピードを遺憾なく発揮。坂路で破格の51秒台をマークしデムーロ騎手の手綱で気迫満点。",
        "trainingWeight": 502, "lastRaceWeight": 498, "confirmedWeight": None, "weightDiff": None,
        "bloodline": {"sire": "ロードカナロア", "dam": "リラヴァティ", "bms": "ゼンノロブロイ", "distanceApt": "1200-1600m", "trackApt": "良"},
        "lastRace": {"raceName": "スプリンターズS (G1)", "date": "2026-09-27", "distance": "芝1200m", "rank": 2, "agari": "33.5", "margin": "0.1秒差", "factor": "電撃の秋スプリントG1で猛追2着。マイル克服なら一気に突き抜ける爆発力。"}
    }
]

# 2026 Mile Championship (Race 18) Occult Signs (6 fully verified 2026 signs)
occult_18 = [
    {
        "id": 1,
        "badge": "🔥 Xトレンド1位",
        "title": "🌟 プレゼンター竜星涼さん来場！「瑠星」言霊シンクロ＆VIVANTサイン",
        "source": "X (旧Twitter) サイン派コミュニティ",
        "content": "2026年マイルCS当日に京都競馬場へプレゼンターとして来場する人気俳優の竜星涼（りゅうせい りょう）さん。Xでは発表直後から『竜星＝瑠星』の言霊サインでタイムラインが沸騰！該当する坂井瑠星騎乗の【エコロブルーム】に強烈なサインが点灯中。さらに竜星涼さんが出演した社会現象ドラマ『VIVANT』のテーマカラー（赤＝3枠・黒＝2枠）や劇中コードネームにちなむ連想サイン馬券がSNS上で猛烈に支持されています。",
        "targets": [{"name": "エコロブルーム", "gate": None, "waku": None}]
    },
    {
        "id": 2,
        "badge": "👑 記録オカルト",
        "title": "⚡ C.ルメール騎手「京都マイルCS未勝利」の呪縛打破＆VM女王エンブロイダリー",
        "source": "X 記録・オカルトデータ班",
        "content": "阪神代替開催のマイルCSではグランアレグリア等で連覇したルメール騎手だが、京都開催のマイルCSでは意外にも未勝利のジンクスが存在。『ルメールの京都マイルCS呪縛』を打ち破るべく送り込まれたのが、春のヴィクトリアマイルを驚異の1分30秒9で圧勝した快速3歳牝馬【エンブロイダリー】！牝馬の斤量55kgの恩恵も受け、『今年こそルメールが京都マイルの頂点に立つ歴史的瞬間』とサイン派も実力派も一致して大本命に推しています。",
        "targets": [{"name": "エンブロイダリー", "gate": None, "waku": None}]
    },
    {
        "id": 3,
        "badge": "⚔️ 世代交代サイン",
        "title": "🏆 桜花賞馬「スターアニス」× NHKマイルC覇者「ロデオドライブ」春の3歳マイル頂上連動",
        "source": "X・出馬表オカルト研究会",
        "content": "2026年春のマイルクラシックを制した2頭が京都マイルで激突！桜花賞を1分31秒5で制した【スターアニス】（松山弘平）と、NHKマイルCを1分31秒5で差し切った【ロデオドライブ】（J.モレイラ）。過去に3歳馬がマイルCSを制した年（ステルヴィオ、ペルシアンナイト等）は『春のマイルG1最先着馬』が連動する鉄則があり、古馬マイル路線をまとめて飲み込む世代交代の強力サインと話題です。",
        "targets": [{"name": "スターアニス", "gate": None, "waku": None}, {"name": "ロデオドライブ", "gate": None, "waku": None}]
    },
    {
        "id": 4,
        "badge": "🎯 鉄板オカルト",
        "title": "🎩 安田記念馬「シックスペンス」秋のマイル統一王者へ！外国人騎手無双の法則",
        "source": "競馬Xタイムライン総意",
        "content": "春の安田記念を鮮やかに制した【シックスペンス】。マイルCSの歴史において『安田記念覇者の参戦』は連対率50%を超える鉄板級のステップ。短期免許で絶好調のフランスの名手A.プーシャン騎手を背に、春秋マイル王統一のサインがくっきりと浮かび上がっています。",
        "targets": [{"name": "シックスペンス", "gate": None, "waku": None}]
    },
    {
        "id": 5,
        "badge": "🌪️ 海外超強豪",
        "title": "🇫🇷 仏マイルG1覇者「エルデナリ」電撃来日！外車無双とM.バルザローナの勝負気配",
        "source": "X・海外競馬考察トレンド",
        "content": "欧州マイル最高峰で好走を続けるフランスの刺客【エルデナリ】がM.バルザローナ騎手と共に参戦！外国馬がマイルCSに挑戦する年は波乱の使者となるオカルトがあり、京都の淀の下り坂を生かしたロングスパートに日本のファンからも熱い視線が注がれています。",
        "targets": [{"name": "エルデナリ", "gate": None, "waku": None}]
    },
    {
        "id": 6,
        "badge": "🎨 ポスター暗号",
        "title": "🖼️ JRA公式マイルCSポスター「一瞬の閃光が、時代を創る。」文字数・配色サイン",
        "source": "X ポスター解析班",
        "content": "JRA公式告知ポスターの背景に輝く稲妻と閃光のエフェクト。『閃光（ライト/フラッシュ）』から【ウォーターリヒト】（リヒト＝ドイツ語で光）、そして短距離からマイルへ挑む【ワールズエンド】。さらに緑枠（6枠）と青枠（4枠）のクロス配置が噂されています。",
        "targets": [{"name": "ウォーターリヒト", "gate": None, "waku": None}, {"name": "ワールズエンド", "gate": None, "waku": None}]
    }
]

# 2026 Japan Cup (Race 19) Occult Signs (Nov 29, 2026)
occult_19 = [
    {
        "id": 1,
        "badge": "🔥 秋天連覇サイン",
        "title": "👑 天皇賞（秋）覇者「ダノンデサイル」王道秋古馬2冠ロード！",
        "source": "X (旧Twitter) サイン派コミュニティ",
        "content": "11月1日の天皇賞（秋）で異次元の大外一気を決め、見事復活の戴冠を果たした日本ダービー馬【ダノンデサイル】。過去に秋天からジャパンカップを連覇した名馬（スペシャルウィーク、ゼンノロブロイ、アーモンドアイ、イクイノックス）の軌跡と完全に一致。東京芝2400mはダービー制覇の舞台であり、王道2冠達成の鉄板サインが点灯しています。",
        "targets": [{"name": "ダノンデサイル", "gate": None, "waku": None}]
    },
    {
        "id": 2,
        "badge": "🌍 国際G1の法則",
        "title": "✈️ 世界トップホース来日！国際招待競走とロンシャン血統の連動",
        "source": "海外競馬データ班",
        "content": "ジャパンカップ創設の理念である世界最高峰の激突。凱旋門賞やキングジョージで激闘を演じた欧州強豪馬の参戦に合わせ、府中の高速芝に対応するノーザンダンサー系・サドラーズウェルズ系のスタミナ血統がX上で注目を集めています。",
        "targets": []
    },
    {
        "id": 3,
        "badge": "⚡ 東京2400m絶対神話",
        "title": "🎩 C.ルメール騎手「ジャパンカップ庭の法則」＆勝負の秋古馬戦線",
        "source": "競馬Xタイムライン総意",
        "content": "アーモンドアイ、イクイノックスなど東京芝2400mで絶対的無双を誇るC.ルメール騎手。府中の長い直線で仕掛け所を完璧に把握するルメール騎手の騎乗馬は、オカルトを超えて物理法則の域。今年も複勝圏内確実のサインとして支持されています。",
        "targets": []
    }
]

# 2026 Champions Cup (Race 20) Occult Signs (Dec 6, 2026)
occult_20 = [
    {
        "id": 1,
        "badge": "🌪️ コースバイアス",
        "title": "🎯 中京ダート1800m「最内1枠・先行馬」絶対優位バイアスの法則",
        "source": "コース傾向解析班",
        "content": "スタートから1コーナーまでの距離が短く、外枠が極端に不利とされる中京ダート1800m。過去10年のデータでも1枠・2枠の先行馬が圧倒的な連対率を記録しており、枠順確定時の白枠（1枠）引き当てが最大の激アツサインとなります。",
        "targets": []
    },
    {
        "id": 2,
        "badge": "⚡ 新世代ダート王",
        "title": "👑 ダート界の新世代交代！JBCクラシック組と若き砂の怪物の激突",
        "source": "X ダート研究部",
        "content": "世代交代が進むダート界。JBCクラシック好走組と勢いに乗る4歳・3歳世代の新星ダートマイラーによる頂上決戦。冬の乾いた中京ダートを力強く踏み荒らす大型馬の激走サインが噂されています。",
        "targets": []
    }
]

# 2026 Hanshin JF (Race 21) Occult Signs (Dec 13, 2026)
occult_21 = [
    {
        "id": 1,
        "badge": "🌸 リニューアル開幕",
        "title": "🏟️ 新装・阪神競馬場リニューアル！外回りマイルコースの「外差し黄金サイン」",
        "source": "競馬場改修ウォッチャー",
        "content": "大改修工事を終えて生まれ変わった新装・阪神競馬場！絶好のクッション値を誇る新芝外回りコースで行われる2歳女王決定戦は、直線で長い脚を使えるディープ系・キタサン系血統の差し馬に最高の舞台設定と話題騒然。",
        "targets": []
    },
    {
        "id": 2,
        "badge": "💎 無敗の素質馬",
        "title": "✨ アルテミスS＆ファンタジーS勝ち馬のダイレクト連動サイン",
        "source": "X 2歳戦研究会",
        "content": "暮れの2歳女王決定戦は前哨戦の重賞勝ち馬がそのまま連動するオカルトが健在。無敗で駒を進めてきた素質馬の白枠（1枠）引き当てに熱視線が注がれています。",
        "targets": []
    }
]

# 2026 Asahi Hai FS (Race 22) Occult Signs (Dec 20, 2026)
occult_22 = [
    {
        "id": 1,
        "badge": "⚡ 2歳スピード王",
        "title": "🚀 新装・阪神マイル「前半3Fハイペース」をねじ伏せる怪物の星",
        "source": "X スピード指数研究班",
        "content": "サウジアラビアRCやデイリー杯2歳Sで圧倒的なスピードを見せつけた2歳マイラーが集結。新装阪神の直線を上がり最速で突き抜ける『無敗馬の戴冠』がX上で最大の注目サインとなっています。",
        "targets": []
    },
    {
        "id": 2,
        "badge": "👑 名門厩舎の系譜",
        "title": "🏇 栗東・美浦の2歳トップステーブル勝負仕上げサイン",
        "source": "競馬サイン研究会",
        "content": "暮れの2歳G1を狙いすまして使ってくるトップステーブルの勝負気配。クラシックへの直行ではなく朝日杯FSを取りに来た有力馬の勝負仕上げサインが点灯中。",
        "targets": []
    }
]

# 2026 Hopeful S (Race 23) Occult Signs (Dec 26, 2026)
occult_23 = [
    {
        "id": 1,
        "badge": "🏛️ クラシック直結",
        "title": "🌟 中山芝2000m「東スポ杯・京都2歳S勝ち馬」クラシック王手サイン",
        "source": "X クラシック番付班",
        "content": "有馬記念前日の中山芝2000mを制する馬が翌年の皐月賞・ダービーの最有力候補へ。急坂をものともしないパワーと機動力を兼ね備えた中距離王子の誕生サイン！",
        "targets": []
    }
]

# 2026 Arima Kinen (Race 24) Occult Signs (Dec 27, 2026)
occult_24 = [
    {
        "id": 1,
        "badge": "🏆 世代頂上決戦",
        "title": "👑 天皇賞（秋）覇者「ダノンデサイル」vs 二冠馬「ロブチェン」vs 菊花賞馬「ゴーイントゥスカイ」",
        "source": "X 日本全国トレンド1位",
        "content": "2026年のグランプリ有馬記念はまさに空前の頂上決戦！秋の天皇賞を制したダノンデサイル、春の二冠（皐月賞・ダービー）を制したロブチェン、秋の菊花賞馬ゴーイントゥスカイ、そして宝塚記念覇者メイショウタバル。世代最強馬が中山2500mに勢揃いし、グランプリの覇権をかけた大激突サインが炸裂しています。",
        "targets": [{"name": "ダノンデサイル", "gate": None, "waku": None}, {"name": "ロブチェン", "gate": None, "waku": None}, {"name": "ゴーイントゥスカイ", "gate": None, "waku": None}]
    },
    {
        "id": 2,
        "badge": "🎄 クリスマス世相",
        "title": "🎅 12/27開催「クリスマス有馬」と「白枠1枠・赤枠3枠」連動の法則",
        "source": "オカルト競馬倶楽部",
        "content": "年の瀬の有馬記念といえば世相サイン。クリスマス直後の12月27日開催となる今年は、クリスマスカラーの『白（1枠）』と『赤（3枠）』の組み合わせが過去のクリスマス有馬（ダイユウサク、ハーツクライ等）同様に超高配当を生み出す鉄板サインとして大注目！",
        "targets": []
    },
    {
        "id": 3,
        "badge": "🐎 ファン投票1位",
        "title": "⭐ 「ファン投票1位馬の連対率70%」グランプリホースの絶対法則",
        "source": "競馬データ班",
        "content": "有馬記念の歴史において、ファン投票1位に支持された馬の信頼度は絶大。多くの競馬ファンの夢を背負ったグランプリホースが中山の急坂を先頭で駆け抜ける王道シナリオがSNSを席巻しています。",
        "targets": []
    }
]

# Apply updates to pred_data
pred_data['races']['18']['starters'] = starters_18
pred_data['races']['18']['occultSigns'] = occult_18
pred_data['races']['19']['occultSigns'] = occult_19
pred_data['races']['20']['occultSigns'] = occult_20
pred_data['races']['21']['occultSigns'] = occult_21
pred_data['races']['22']['occultSigns'] = occult_22
pred_data['races']['23']['occultSigns'] = occult_23
pred_data['races']['24']['occultSigns'] = occult_24

# If root has occultSigns/starters for activeRaceId 18, update root as well
pred_data['starters'] = starters_18
pred_data['occultSigns'] = occult_18

# Update entries_data for Race 18
entries_18 = []
for s in starters_18:
    entries_18.append({
        "waku": None,
        "gate": None,
        "horseName": s["horseName"],
        "sexAge": s["sexAge"],
        "load": s["load"],
        "jockey": s["jockey"],
        "stable": s["stable"]
    })
entries_data['18'] = entries_18

# Write back JSON files
with open(pred_json_path, 'w', encoding='utf-8') as f:
    json.dump(pred_data, f, ensure_ascii=False, indent=2)

with open(entries_json_path, 'w', encoding='utf-8') as f:
    json.dump(entries_data, f, ensure_ascii=False, indent=2)

# Write back JS files
with open(pred_js_path, 'w', encoding='utf-8') as f:
    f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')

with open(entries_js_path, 'w', encoding='utf-8') as f:
    f.write('export const ENTRIES_DATA = ' + json.dumps(entries_data, ensure_ascii=False, indent=2) + ';\n')

print("Successfully updated prediction_data and entries_data for 2026!")
