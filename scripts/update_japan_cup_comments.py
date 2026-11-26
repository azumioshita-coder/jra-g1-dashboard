import json
import os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(APP_DIR, 'src')

PRED_JSON = os.path.join(SRC_DIR, 'prediction_data.json')
PRED_JS = os.path.join(SRC_DIR, 'prediction_data.js')
HORSE_JSON = os.path.join(SRC_DIR, 'horse_data.json')
HORSE_JS = os.path.join(SRC_DIR, 'horse_data.js')

JC_DATA_UPDATES = {
    "カランダガン": {
        "lastRace": "英チャンピオンS(G1) 2着",
        "strengths": "前走・英チャンピオンS2着。キングジョージ2着、英インターナショナルS2着と欧州中距離最高峰で連続好走。サンクルー大賞圧勝など世界屈指の実績を誇り、府中の高速芝にも対応できる抜群のフットワークを披露。",
        "trainingComment": "【調教S・抜群の伸び】本番で騎乗するバルザローナ騎手を背に芝単走。馬なりのままラスト11.2秒を計時。身のこなしは極めて柔軟で、海外遠征馬としては近年屈指の仕上がり。",
        "concerns": "初来日による長距離輸送の疲労と、日本の独特なゲート発走環境への適応。"
    },
    "ダノンデサイル": {
        "lastRace": "天皇賞(秋)(G1) 1着",
        "strengths": "日本ダービー圧勝馬にして前走・天皇賞(秋)の覇者！2400mへの延長は世代の頂点に立った絶好の舞台。叩き2戦目の上積みも大きく、天皇賞(秋)・ジャパンカップの秋古馬連冠へ視界良好。",
        "trainingComment": "【調教S・文句なしの気配】1週前にCWでラスト11.0秒の猛時計を叩き出し、最終追いも馬なりで鋭い伸び。ダービー制覇時を上回る充実期で、秋古馬2冠へ仕上がり万全。",
        "concerns": "馬群の内に入った際の進路確保と、直線で包まれるリスク。"
    },
    "オンブズマン": {
        "lastRace": "英チャンピオンS(G1) 1着",
        "strengths": "前走・英チャンピオンSで欧州強豪を一蹴しG1制覇。名門ゴスデン厩舎が送り込む超一流の刺客で、主戦W.ビュイック騎手の手綱捌きとタフな持続力勝負なら勝機十分。",
        "trainingComment": "【調教A+・素軽さ上々】芝コースでビュイック騎手を背に軽快な加速。坂下から一気にトップスピードに乗りラスト11.5秒。検疫明けの疲れも見せず好調をキープ。",
        "concerns": "欧州の重いタフな芝での実績が中心で、東京の超高速レコード決着への対応力。"
    },
    "マスカレードボール": {
        "lastRace": "天皇賞(秋)(G1) 11着",
        "strengths": "春のQE2世C2着の実力馬。前走・天皇賞(秋)11着はスロー展開不向きで度外視可能。主戦C.ルメール騎手とのコンビ継続で、広い東京2400mでの巻き返しを期す。",
        "trainingComment": "【調教A・キレ味健在】美浦Wで僚馬を目標に折り合い重視の調整。直線追われてからの反応はシャープで、前走敗戦のダメージは一切感じさせない。",
        "concerns": "前走大敗からの精神面の立て直しと、古馬G1トップクラス相手の力関係。"
    },
    "クロワデュノール": {
        "lastRace": "天皇賞(秋)(G1) 5着",
        "strengths": "春の天皇賞(春)を制した長距離G1馬。前走・天皇賞(秋)5着を一叩きされ、東京2400mへの距離延長は絶好材料。キタサンブラック譲りの豊富なスタミナとC.デムーロ騎手の手綱で逆襲へ。",
        "trainingComment": "【調教A+・迫力のフットワーク】栗東CWで力強いストライドを披露。追われてからの脚勢は前走以上で、ひと叩きされた上積みは極めて大きい。",
        "concerns": "休み明け2戦目の反動と、極限の瞬発力・上がり33秒前半のキレ味勝負になった際の対応。"
    },
    "ヘデントール": {
        "lastRace": "京都大賞典(G2) 5着",
        "strengths": "菊花賞2着の実力派ステイヤー。前走・京都大賞典5着をステップに気配上昇。豊富なスタミナと持続力が武器で、T.マーカンド騎手の剛腕で直線の我慢比べに持ち込みたい。",
        "trainingComment": "【調教A・スタミナ満点】美浦坂路で終い重点に追われ力強い伸び。馬体の張りも良化しており、長い府中の直線でのスタミナ勝負なら台頭可能。",
        "concerns": "前半の追走スピード不足による道中の置かれと、超高速決着での時計勝負。"
    },
    "メイショウタバル": {
        "lastRace": "凱旋門賞(G1) 14着",
        "strengths": "神戸新聞杯を圧巻の逃げ切りで快勝。フランス凱旋門賞遠征から帰国し、武豊騎手の手綱で単騎マイペースの逃げに持ち込めば、府中の直線を後続に影をも踏ませず逃げ切る大金星も。",
        "trainingComment": "【調教A・活気十分】栗東坂路で軽快な行きっぷりを披露。帰国初戦ながら馬体はすっきりと仕上がっており、自分の形に持ち込めれば怖い存在。",
        "concerns": "海外遠征帰りの疲労回復具合と、他馬に競りかけられた際のペースコントロール・暴走のリスク。"
    },
    "ミニーホーク": {
        "lastRace": "英チャンピオンズF&MS(G1) 1着",
        "strengths": "愛オークス制覇に続き前走英チャンピオンズフィリーズ＆メアズSも勝利した欧州最強牝馬。A.オブライエン厩舎＆世界の名手R.ムーア騎手の強力タッグに加え、斤量56kgの恩恵も絶大。",
        "trainingComment": "【調教A+・しなやかな走り】東京競馬場での環境順応も早く、芝コースで弾むような動き。牝馬らしい軽快さがあり、日本の芝への適性は高そう。",
        "concerns": "日本特有の硬く速い野芝馬場への適性と、歴戦の古豪牡馬トップクラスとの力関係。"
    },
    "ヴェルテンベルク": {
        "lastRace": "京都大賞典(G2) 7着",
        "strengths": "百戦錬磨のベテラン横山典弘騎手とのコンビ。前走・京都大賞典7着から叩き2戦目で上昇。後方で脚を溜めてインを突く魔術的な騎乗で着順押し上げを狙う。",
        "trainingComment": "【調教B+・マイペース維持】栗東坂路で軽めの調整。気合乗りも程よく、ベテランの手綱で一発を狙う態勢は整っている。",
        "concerns": "近走の決め手不足と、超一線級相手のスピード決着で置かれてしまう懸念。"
    },
    "ファイアンクランツ": {
        "lastRace": "アルゼンチン共和国杯(G2) 8着",
        "strengths": "名手J.モレイラ騎手を配した堀厩舎の勝負気配。前走アルゼンチン共和国杯8着からの巻き返しを期し、東京2400mでの素軽さを活かした立ち回りに期待。",
        "trainingComment": "【調教B+・素軽い身のこなし】美浦Wで併せ馬。モレイラ騎手の感触も上々で、叩き2戦目の変わり身に警戒したい。",
        "concerns": "古馬重賞・G1一線級相手でのキャリア不足と、タフなスタミナ勝負での踏ん張り。"
    },
    "タガノデュード": {
        "lastRace": "天皇賞(秋)(G1) 4着",
        "strengths": "前走・天皇賞(秋)で上がり最速級の末脚を繰り出し4着と大健闘。M.デムーロ騎手との相性抜群で、東京2400mへの延長でも後方一気の末脚勝負にかける。",
        "trainingComment": "【調教A・追撃態勢万全】栗東CWで鋭い伸び脚を披露。前走好走の勢いをそのまま維持しており、展開ひとつで馬券圏内突入の気配。",
        "concerns": "後方待機一辺倒のため前残りのスロー展開に泣くリスクと、直線でのコース取り。"
    },
    "アーバンシック": {
        "lastRace": "新潟記念(G3) 5着",
        "strengths": "菊花賞馬としての地力は世代屈指。前走・新潟記念5着を経て調整され、新進気鋭のA.プーシャン騎手を鞍上に迎え、府中の直線の末脚勝負で復活の一撃を狙う。",
        "trainingComment": "【調教A・豪快なストライド】美浦Wで迫力ある動きを披露。菊花賞馬らしいスケールの大きな走りで、直線の長い東京コースなら末脚爆発の予感。",
        "concerns": "ゲート出遅れ癖と道中追走でのズブさ、不器用さ。"
    },
    "シェイクユアハート": {
        "lastRace": "天皇賞(秋)(G1) 6着",
        "strengths": "前走・天皇賞(秋)では果敢に先行して6着と見せ場十分。古川吉洋騎手の手綱で最経済コースを立ち回り、粘り強さを活かして掲示板争いに食い込みたい。",
        "trainingComment": "【調教B+・粘り強さ健在】栗東坂路で一定のラップを刻み力強く登坂。先行して渋太さを発揮できる仕上がり。",
        "concerns": "超一流G1馬相手での絶対的なトップスピード・キレ味の差。"
    },
    "コスモキュランダ": {
        "lastRace": "天皇賞(秋)(G1) 9着",
        "strengths": "弥生賞1着、皐月賞2着の実績馬。前走・天皇賞(秋)9着も東京2400mへの距離延長は好材料。丹内騎手との息の合ったロングスパートが決まれば大駆け警戒。",
        "trainingComment": "【調教A・トモの張り上々】美浦Wで力強い動き。トモの張りが戻り状態は確実に上向き。3〜4コーナーからの積極的な捲り脚に期待。",
        "concerns": "東京の長い直線での決め手比べで見劣る点と、コーナリングからの進路確保。"
    },
    "エキサイトバイオ": {
        "lastRace": "有馬記念(G1) 8着",
        "strengths": "荻野極騎手とのコンビで堅実にキャリアを重ねる。叩き良化型で状態はキープ。ロスなく内々を立ち回ってどこまで粘れるか。",
        "trainingComment": "【調教B・順調な仕上がり】栗東坂路で軽快なフットワーク。大舞台に向けて状態面に不安はなく、持てる力を出し切る態勢。",
        "concerns": "最高峰G1の超高速ペースに対するスピード能力の絶対的な差。"
    },
    "テアオ": {
        "lastRace": "ラテンアメリカ大賞(G1) 1着",
        "strengths": "南米チリの年度代表馬でラテンアメリカ大賞などG1を制覇した名馬。米国J.サドラー厩舎の手腕と主戦L.トーレス騎手とともに堂々来日。未知のスピードを秘める。",
        "trainingComment": "【調教A・力強い掻き込み】東京ダートで入念に調整後、芝コースでの走りに移行。筋肉質な芦毛の馬体が目立ち、気合も十分。",
        "concerns": "南米・北米と全く質の異なる日本の超高速・硬い芝への適性と、長距離空輸の疲労。"
    },
    "ゴリアット": {
        "lastRace": "オイロパ賞(G1) 1着",
        "strengths": "英キングジョージを圧勝し前走・独オイロパ賞も完勝した欧州屈指の中長距離実力馬。名手O.スミヨン騎手との名コンビで、2400mの持続力とパワーは世界最高レベル。",
        "trainingComment": "【調教A+・雄大な馬格】東京芝コースで堂々たるキャンター。キングジョージ覇者の風格を漂わせ、雄大なフットワークで東京の芝を踏みしめる。",
        "concerns": "欧州のタフな重馬場で真価を発揮するタイプで、東京の超高速芝・瞬発力勝負への対応力。"
    },
    "エシカルダイヤモンド": {
        "lastRace": "BCターフ(G1) 9着",
        "strengths": "アイルランド屈指のステイヤーで米BCターフにも挑戦。日本の名手・坂井瑠星騎手を鞍上に迎え、豊富なスタミナを活かした積極的なレース運びで前進を図る。",
        "trainingComment": "【調教B+・長丁場向きの走り】芝コースで長い距離をじっくり乗り込み。折り合いがスムーズで、直線の長いコースでの持久力戦なら見せ場も。",
        "concerns": "中距離のスピード勝負に対する適性と、海外転戦による連戦の疲労。"
    }
}

OTHER_RACE_CONCERNS = {
    "20": "中京ダート特有の急坂とタイトなコーナーでの立ち回り、砂被りの影響。",
    "21": "マイル戦の速いペースへの追走力と、若駒特有の気性面の課題。",
    "22": "前半のハイペース追走と、外枠に入った際の距離ロス。",
    "23": "中山2000mの小回り4コーナーでの進路取りと急坂の克服。",
    "24": "中山2500m特有のトリッキーなコース形態とスタミナ消耗戦への適応。"
}

def update_prediction_data():
    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        pred_data = json.load(f)

    # 1. Update Race 19 starters and contenderRanking
    if "races" in pred_data and "19" in pred_data["races"]:
        jc = pred_data["races"]["19"]
        
        # starters
        for s in jc.get("starters", []):
            name = s.get("horseName")
            if name in JC_DATA_UPDATES:
                upd = JC_DATA_UPDATES[name]
                s["lastRace"] = upd["lastRace"]
                s["trainingComment"] = upd["trainingComment"]
                s["comment"] = upd["trainingComment"]
                if name == "ダノンデサイル":
                    if "workoutOneWeek" in s and isinstance(s["workoutOneWeek"], dict):
                        s["workoutOneWeek"]["comment"] = "戸崎騎手を背にCWで古馬OPと併せ馬。内から鋭く突き抜け0.4秒先着。ラスト11.0秒の鬼気迫る加速で、前走・天皇賞(秋)制覇からの更なる上昇・充実ぶりを証明。"

        # contenderRanking
        for c in jc.get("contenderRanking", []):
            name = c.get("horseName")
            if name in JC_DATA_UPDATES:
                upd = JC_DATA_UPDATES[name]
                c["strengths"] = upd["strengths"]
                c["comment"] = upd["strengths"]
                c["concerns"] = upd["concerns"]
                if name == "ダノンデサイル":
                    if "workoutOneWeek" in c and isinstance(c["workoutOneWeek"], dict):
                        c["workoutOneWeek"]["comment"] = "戸崎騎手を背にCWで古馬OPと併せ馬。内から鋭く突き抜け0.4秒先着。ラスト11.0秒の鬼気迫る加速で、前走・天皇賞(秋)制覇からの更なる上昇・充実ぶりを証明。"

    # 2. Update Top-level starters and contenderRanking
    for s in pred_data.get("starters", []):
        name = s.get("horseName")
        if name in JC_DATA_UPDATES:
            upd = JC_DATA_UPDATES[name]
            s["lastRace"] = upd["lastRace"]
            s["trainingComment"] = upd["trainingComment"]
            s["comment"] = upd["trainingComment"]
            if name == "ダノンデサイル":
                if "workoutOneWeek" in s and isinstance(s["workoutOneWeek"], dict):
                    s["workoutOneWeek"]["comment"] = "戸崎騎手を背にCWで古馬OPと併せ馬。内から鋭く突き抜け0.4秒先着。ラスト11.0秒の鬼気迫る加速で、前走・天皇賞(秋)制覇からの更なる上昇・充実ぶりを証明。"

    for c in pred_data.get("contenderRanking", []):
        name = c.get("horseName")
        if name in JC_DATA_UPDATES:
            upd = JC_DATA_UPDATES[name]
            c["strengths"] = upd["strengths"]
            c["comment"] = upd["strengths"]
            c["concerns"] = upd["concerns"]
            if name == "ダノンデサイル":
                if "workoutOneWeek" in c and isinstance(c["workoutOneWeek"], dict):
                    c["workoutOneWeek"]["comment"] = "戸崎騎手を背にCWで古馬OPと併せ馬。内から鋭く突き抜け0.4秒先着。ラスト11.0秒の鬼気迫る加速で、前走・天皇賞(秋)制覇からの更なる上昇・充実ぶりを証明。"

    # 3. Clean placeholder concerns in other races
    for rid, default_concern in OTHER_RACE_CONCERNS.items():
        if "races" in pred_data and rid in pred_data["races"]:
            r = pred_data["races"][rid]
            for c in r.get("contenderRanking", []):
                cur_concern = c.get("concerns", "")
                if "府中の長い直線" in cur_concern or not cur_concern:
                    c["concerns"] = default_concern

    # Save prediction_data.json
    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(pred_data, f, ensure_ascii=False, indent=2)

    # Save prediction_data.js
    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write("export const PREDICTION_DATA = " + json.dumps(pred_data, ensure_ascii=False, indent=2) + ";\n")

    print("prediction_data.json and prediction_data.js updated successfully!")

def update_horse_data():
    with open(HORSE_JSON, 'r', encoding='utf-8') as f:
        horse_data = json.load(f)

    # Update Danon Decile titles
    if "ダノンデサイル" in horse_data:
        d = horse_data["ダノンデサイル"]
        titles = d.get("titles", [])
        if "26'天皇賞(秋)(G1)" not in titles:
            d["titles"] = ["26'天皇賞(秋)(G1)", "24'日本ダービー(G1)"]

    # Update Ombudsman titles
    if "オンブズマン" in horse_data:
        o = horse_data["オンブズマン"]
        titles = o.get("titles", [])
        if "26'英チャンピオンS(G1)" not in titles:
            d_titles = ["26'英チャンピオンS(G1)"]
            for t in titles:
                if t not in d_titles:
                    d_titles.append(t)
            o["titles"] = d_titles

    # Update Calandagan titles
    if "カランダガン" in horse_data:
        c = horse_data["カランダガン"]
        titles = c.get("titles", [])
        if "26'サンクルー大賞(G1)" not in titles:
            c_titles = ["26'サンクルー大賞(G1)"]
            for t in titles:
                if t not in c_titles:
                    c_titles.append(t)
            c["titles"] = c_titles

    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(horse_data, f, ensure_ascii=False, indent=2)

    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(horse_data, ensure_ascii=False, indent=2) + ";\n")

    print("horse_data.json and horse_data.js updated successfully!")

if __name__ == "__main__":
    update_prediction_data()
    update_horse_data()
