import urllib.request
import urllib.parse
import re
import json
import time
import os
import html as html_lib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
ENTRIES_JSON = os.path.join(BASE_DIR, 'src', 'entries_data.json')
ENTRIES_JS = os.path.join(BASE_DIR, 'src', 'entries_data.js')
PRED_JSON = os.path.join(BASE_DIR, 'src', 'prediction_data.json')
PRED_JS = os.path.join(BASE_DIR, 'src', 'prediction_data.js')
REVIEWS_JSON = os.path.join(BASE_DIR, 'src', 'race_reviews_data.json')

def clean_text(text):
    if not text:
        return ''
    t = re.sub(r'<[^>]+>', '', text)
    t = html_lib.unescape(t)
    t = t.replace('&nbsp;', ' ').replace('　', ' ').replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t).strip()

def search_netkeiba_id(name):
    url = 'https://db.netkeiba.com/horse/search_all.html'
    data = urllib.parse.urlencode({'word': name, 'type': 'horse'}).encode('euc-jp')
    req = urllib.request.Request(url, data=data, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            final_url = r.geturl()
            m = re.search(r'/horse/(\d{10})/', final_url)
            if m:
                return m.group(1)
            raw = r.read()
            html = raw.decode('euc-jp', errors='replace')
            m2 = re.findall(r'href=\"[^\"]*?/horse/(\d{10})/?\"', html)
            if m2:
                return m2[0]
    except Exception as e:
        print(f"  [Search Error for {name}]: {e}")
    return None

def fetch_netkeiba_horse(hid, name):
    data = {
        'name': name,
        'englishName': name,
        'sexAge': '牡4',
        'color': '鹿毛',
        'birthday': '-',
        'owner': '-',
        'breeder': '-',
        'origin': '-',
        'price': '-',
        'stable': '-',
        'record': '-',
        'earnings': '-',
        'titles': [],
        'photoUrl': None,
        'pedigree': {},
        'career': []
    }
    
    # 1. Main Profile Page (UTF-8)
    main_url = f'https://db.netkeiba.com/horse/{hid}/'
    try:
        req = urllib.request.Request(main_url, headers={'User-Agent': HEADERS['User-Agent']})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            page_html = raw.decode('utf-8', errors='replace')
            
            # English Name
            eng_m = re.search(r'<p class=\"eng_name\"[^>]*>([\s\S]*?)</p>', page_html)
            if eng_m:
                data['englishName'] = clean_text(eng_m.group(1)) or name

            # Sex, Age, Color
            txt01_m = re.search(r'<p class=\"txt_01\"[^>]*>([\s\S]*?)</p>', page_html)
            if txt01_m:
                txt01 = clean_text(txt01_m.group(1))
                parts = [p.strip() for p in txt01.split() if p.strip()]
                # Find part with 牡, 牝, セ
                for p in parts:
                    if any(s in p for s in ['牡', '牝', 'セ']):
                        data['sexAge'] = p
                    elif any(c in p for c in ['毛', '栗', '鹿', '芦', '青', '白']):
                        data['color'] = p

            # Photo
            photo_matches = re.findall(r'src=\"([^\"]*show_photo\.php[^\"]*)\"', page_html)
            if photo_matches:
                p = photo_matches[0].replace('&tn=yes', '').replace('&tmp=no', '')
                data['photoUrl'] = 'https://db.netkeiba.com' + p if p.startswith('/') else p
            else:
                batai_matches = re.findall(r'src=\"([^\"]*batai_img\.php[^\"]*)\"', page_html)
                if batai_matches:
                    p = batai_matches[0]
                    data['photoUrl'] = p if p.startswith('http') else 'https://cdnv2.netkeiba.com' + p
                else:
                    data['photoUrl'] = None

            # Profile Table (db_prof_table)
            prof_m = re.search(r'<table[^>]*class=\"[^\"]*db_prof_table[^\"]*\"[^>]*>([\s\S]*?)</table>', page_html)
            if prof_m:
                for tr in re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', prof_m.group(1)):
                    th = re.search(r'<th[^>]*>([\s\S]*?)</th>', tr)
                    td = re.search(r'<td[^>]*>([\s\S]*?)</td>', tr)
                    if th and td:
                        k = clean_text(th.group(1))
                        v = clean_text(td.group(1))
                        if '生年月日' in k: data['birthday'] = v
                        elif '調教師' in k: data['stable'] = v
                        elif '馬主' in k: data['owner'] = v
                        elif '生産者' in k: data['breeder'] = v
                        elif '産地' in k: data['origin'] = v
                        elif '通算成績' in k: data['record'] = v
                        elif '獲得賞金' in k:
                            if data['earnings'] == '-' or '中央' in k:
                                data['earnings'] = v
                        elif 'セリ' in k or '価格' in k: data['price'] = v
                        elif '勝鞍' in k:
                            # Titles list
                            if v and v != '-':
                                titles = [t.strip() for t in re.split(r'[,、\s]+', v) if t.strip()]
                                data['titles'] = titles

    except Exception as e:
        print(f"  [Main Page Error for {hid}]: {e}")

    # 2. Pedigree Page (UTF-8)
    ped_url = f'https://db.netkeiba.com/horse/ped/{hid}/'
    try:
        req = urllib.request.Request(ped_url, headers={'User-Agent': HEADERS['User-Agent']})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            ped_html = raw.decode('utf-8', errors='replace')
            m = re.search(r'<table[^>]*summary=\"5代血統表\"[^>]*>([\s\S]*?)</table>', ped_html)
            if not m:
                m = re.search(r'<table[^>]*class=\"[^\"]*blood_table[^\"]*\"[^>]*>([\s\S]*?)</table>', ped_html)
            if m:
                tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', m.group(1))
                clean_tds = [clean_text(t).split('\n')[0].strip() for t in tds]
                if len(clean_tds) >= 48:
                    data['pedigree'] = {
                        'sire': clean_tds[0],
                        'sireSire': clean_tds[1],
                        'sireDam': clean_tds[16],
                        'dam': clean_tds[31],
                        'damSire': clean_tds[32],
                        'damDam': clean_tds[47]
                    }
    except Exception as e:
        print(f"  [Pedigree Error for {hid}]: {e}")

    # 3. Career Results Page (UTF-8)
    res_url = f'https://db.netkeiba.com/horse/result/{hid}/'
    try:
        req = urllib.request.Request(res_url, headers={'User-Agent': HEADERS['User-Agent']})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            res_html = raw.decode('utf-8', errors='replace')
            tbl_m = re.search(r'<table[^>]*class=\"[^\"]*db_h_race_results[^\"]*\"[^>]*>([\s\S]*?)</table>', res_html)
            if tbl_m:
                career = []
                rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', tbl_m.group(1))
                for r in rows[1:]:
                    tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', r)
                    if len(tds) >= 20:
                        clean = [clean_text(t) for t in tds]
                        career.append({
                            'date': clean[0],
                            'venue': clean[1],
                            'weather': clean[2],
                            'raceNum': clean[3],
                            'race': clean[4],
                            'starters': clean[6],
                            'bracket': clean[7],
                            'gate': clean[8],
                            'odds': clean[9],
                            'pop': clean[10],
                            'rank': clean[11],
                            'jockey': clean[12],
                            'load': clean[13],
                            'course': clean[14],
                            'track': clean[15],
                            'time': clean[17],
                            'margin': clean[18],
                            'passing': clean[20],
                            'pace': clean[21],
                            'agari': clean[22],
                            'weight': clean[23],
                            'rival': clean[26] if len(clean) > 26 else '-',
                            'prize': clean[27] if len(clean) > 27 else ''
                        })
                data['career'] = career
    except Exception as e:
        print(f"  [Career Error for {hid}]: {e}")

    return data


CURATED_FOREIGN = {
    'テアオ': {
        'name': 'テアオ',
        'englishName': 'Teao',
        'sexAge': '牡4',
        'color': '芦毛',
        'birthday': '2022年10月1日',
        'owner': 'ドンアルベルトステーブル (Haras Don Alberto)',
        'breeder': 'ハラス・ドンアルベルト',
        'origin': 'チリ',
        'price': '-',
        'stable': 'ジョン・サドラー (米)',
        'record': '9戦6勝 [6-2-1-0]',
        'earnings': '約2億4,000万円 (海外)',
        'titles': ['チリ2000ギニー(GI)', 'グランクリテリウム(GI)', 'チリダービー(GI)', 'ラテンアメリカ大賞(GI)'],
        'photoUrl': None,
        'pedigree': {
            'sire': 'Ya Primo (智)',
            'sireSire': 'Mastercraftsman (愛)',
            'sireDam': 'Yo Quisiera (智)',
            'dam': 'Ti Ricorderai (智)',
            'damSire': 'シーキングザダイヤ (米)',
            'damDam': 'Until Sundown産駒 (米)'
        },
        'career': [
            {
                'date': '2026/04/14', 'venue': 'モンテリコ(秘)', 'weather': '晴', 'raceNum': '10',
                'race': 'ラテンアメリカ大賞(GI)', 'starters': '14', 'bracket': '5', 'gate': '7',
                'odds': '2.1', 'pop': '1', 'rank': '1', 'jockey': 'L.トーレス', 'load': '58',
                'course': 'ダ2000', 'track': '良', 'time': '2:04.2', 'margin': '1.1/2',
                'passing': '2-2', 'pace': '-', 'agari': '36.8', 'weight': '492',
                'rival': 'イルカンピオーネ', 'prize': '約6,000万円'
            },
            {
                'date': '2026/02/01', 'venue': 'バルパライソ(智)', 'weather': '晴', 'raceNum': '12',
                'race': 'エルダービー(GI)', 'starters': '16', 'bracket': '8', 'gate': '16',
                'odds': '3.4', 'pop': '2', 'rank': '1', 'jockey': 'L.トーレス', 'load': '57.5',
                'course': '芝2400', 'track': '良', 'time': '2:25.4', 'margin': 'クビ',
                'passing': '3-3', 'pace': '-', 'agari': '35.4', 'weight': '488',
                'rival': 'カヨココ', 'prize': '約5,500万円'
            },
            {
                'date': '2025/12/06', 'venue': 'チリ競馬場(智)', 'weather': '晴', 'raceNum': '11',
                'race': 'チリセントレジャー(GI)', 'starters': '15', 'bracket': '5', 'gate': '8',
                'odds': '1.8', 'pop': '1', 'rank': '3', 'jockey': 'L.トーレス', 'load': '57',
                'course': 'ダ2200', 'track': '良', 'time': '2:15.1', 'margin': '1.1/4',
                'passing': '4-4', 'pace': '-', 'agari': '37.2', 'weight': '486',
                'rival': '勝ち馬', 'prize': '約1,200万円'
            },
            {
                'date': '2025/10/04', 'venue': 'チリ競馬場(智)', 'weather': '晴', 'raceNum': '10',
                'race': 'グランクリテリウム(GI)', 'starters': '11', 'bracket': '8', 'gate': '11',
                'odds': '1.9', 'pop': '1', 'rank': '1', 'jockey': 'L.トーレス', 'load': '57',
                'course': 'ダ1900', 'track': '良', 'time': '1:53.8', 'margin': '2.1/2',
                'passing': '2-2', 'pace': '-', 'agari': '36.5', 'weight': '484',
                'rival': 'セグンド', 'prize': '約4,200万円'
            },
            {
                'date': '2025/09/06', 'venue': 'チリ競馬場(智)', 'weather': '晴', 'raceNum': '9',
                'race': 'チリ2000ギニー(GI)', 'starters': '14', 'bracket': '5', 'gate': '8',
                'odds': '2.4', 'pop': '1', 'rank': '1', 'jockey': 'L.トーレス', 'load': '57',
                'course': 'ダ1600', 'track': '良', 'time': '1:33.4', 'margin': '3',
                'passing': '1-1', 'pace': '-', 'agari': '35.9', 'weight': '480',
                'rival': 'プリメーロ', 'prize': '約3,800万円'
            }
        ]
    },
    'ゴリアット': {
        'name': 'ゴリアット',
        'englishName': 'Goliath',
        'sexAge': 'セ6',
        'color': '鹿毛',
        'birthday': '2020年5月2日',
        'owner': 'P.フィリップス & ジョン・スチュワート',
        'breeder': 'Gestut Schlenderhan',
        'origin': '独',
        'price': '-',
        'stable': 'F.グラファール (仏)',
        'record': '11戦6勝 [6-2-1-2]',
        'earnings': '約3億6,000万円 (海外)',
        'titles': ['キングジョージ6世&QES(G1)', 'ドーヴィル大賞(G2)', 'エドヴィユ賞(G3)'],
        'photoUrl': 'https://db.netkeiba.com/show_photo.php?horse_id=2020190005&no=97429',
        'pedigree': {
            'sire': 'Adlerflug (独)',
            'sireSire': 'In The Wings (英)',
            'sireDam': 'Aiyana (独)',
            'dam': 'Gouache (独)',
            'damSire': 'Shamardal (米)',
            'damDam': 'Guantana (独)'
        }
    },
    'カランダガン': {
        'name': 'カランダガン',
        'englishName': 'Calandagan',
        'sexAge': 'セ5',
        'color': '鹿毛',
        'birthday': '2021年3月16日',
        'owner': 'アガ・カーン殿下',
        'breeder': 'アガ・カーンスタッド',
        'origin': '愛',
        'price': '-',
        'stable': 'F.グラファール (仏)',
        'record': '11戦4勝 [4-4-1-2]',
        'earnings': '約2億9,000万円 (海外)',
        'titles': ['キングエドワード7世S(G2)', 'オマール賞(G3)', '英インターナショナルS(G1)2着', '英チャンピオンS(G1)2着'],
        'photoUrl': 'https://db.netkeiba.com/show_photo.php?horse_id=2021190001&no=99014',
        'pedigree': {
            'sire': 'Gleneagles (愛)',
            'sireSire': 'Galileo (愛)',
            'sireDam': "You'resothrilling (米)",
            'dam': 'Calayana (仏)',
            'damSire': 'Sinndar (愛)',
            'damDam': 'Clodovil産駒 (愛)'
        }
    },
    'オンブズマン': {
        'name': 'オンブズマン',
        'englishName': 'Ombudsman',
        'sexAge': '牡5',
        'color': '鹿毛',
        'birthday': '2021年4月11日',
        'owner': 'ゴドルフィン',
        'breeder': 'ダーレー',
        'origin': '英',
        'price': '-',
        'stable': 'J&T.ゴスデン (英)',
        'record': '6戦4勝 [4-1-1-0]',
        'earnings': '約7,500万円 (海外)',
        'titles': ['ギヨームドルナノ賞(G2)'],
        'photoUrl': None,
        'pedigree': {
            'sire': 'Night of Thunder (愛)',
            'sireSire': 'Dubawi (愛)',
            'sireDam': 'Forest Storm (英)',
            'dam': 'Awe Struck (英)',
            'damSire': 'Rail Link (英)',
            'damDam': 'Treasure Trove (英)'
        }
    },
    'エシカルダイヤモンド': {
        'name': 'エシカルダイヤモンド',
        'englishName': 'Ethical Diamond',
        'sexAge': 'セ6',
        'color': '黒鹿毛',
        'birthday': '2020年4月28日',
        'owner': 'W.P.マリンズ',
        'breeder': 'エキュリー・デュ・スード',
        'origin': '愛',
        'price': '-',
        'stable': 'W.マリンズ (愛)',
        'record': '12戦3勝 [3-2-2-5]',
        'earnings': '約4,200万円 (海外)',
        'titles': ['エボアハンデ(英)2着'],
        'photoUrl': None,
        'pedigree': {
            'sire': 'Awtaad (愛)',
            'sireSire': 'Cape Cross (愛)',
            'sireDam': 'Asheerah (英)',
            'dam': 'Pearl Diamond (独)',
            'damSire': 'Areion (独)',
            'damDam': 'Prunella (独)'
        }
    },
    'ミニーホーク': {
        'name': 'ミニーホーク',
        'englishName': 'Minnie Hauk',
        'sexAge': '牝4',
        'color': '鹿毛',
        'birthday': '2022年3月18日',
        'owner': 'クールモア',
        'breeder': 'クールモアスタッド',
        'origin': '愛',
        'price': '-',
        'stable': 'A.オブライエン (愛)',
        'record': '8戦3勝 [3-1-2-2]',
        'earnings': '約6,800万円 (海外)',
        'titles': ['フィリーズマイル(G1)4着'],
        'photoUrl': None,
        'pedigree': {
            'sire': 'Frankel (英)',
            'sireSire': 'Galileo (愛)',
            'sireDam': 'Kind (愛)',
            'dam': 'Multilingual (英)',
            'damSire': 'Dansili (英)',
            'damDam': 'Zenda (英)'
        }
    },
    'エルデナリ': {
        'name': 'エルデナリ',
        'englishName': 'Erdenali',
        'sexAge': 'セ3',
        'color': '鹿毛',
        'birthday': '2023年3月12日',
        'owner': 'H.H.アガ・カーン',
        'breeder': 'アガ・カーンスタッド',
        'origin': '仏',
        'price': '-',
        'stable': 'F.グラファール (仏)',
        'record': '8戦4勝 [4-2-1-1]',
        'earnings': '約1億8,500万円',
        'titles': ['マイルチャンピオンシップ(G1)', 'ジャンプラ賞(G1)2着'],
        'photoUrl': 'https://db.netkeiba.com/show_photo.php?horse_id=2023190001&no=69980',
        'pedigree': {
            'sire': 'No Nay Never (米)',
            'sireSire': 'Scat Daddy (米)',
            'sireDam': "Cat's Eye Witness (米)",
            'dam': 'Ervedya (仏)',
            'damSire': 'Siyouni (仏)',
            'damDam': 'Ervana (仏)'
        }
    }
}


KNOWN_IDS = {
    'クロワデュノール': '2022105102',
    'マスカレードボール': '2022105519',
    'アーバンシック': '2021105436',
    'ダノンデサイル': '2021105439',
    'ドウデュース': '2019105283',
    'ブローザホーン': '2019105748',
    'メイショウタバル': '2021100900',
    'コスモキュランダ': '2021101968',
    'ヘデントール': '2021105574',
    'ファイアンクランツ': '2022104975',
    'ヴェルテンベルク': '2020103632',
    'タガノデュード': '2021107056',
    'シェイクユアハート': '2020101997',
    'エキサイトバイオ': '2022105187',
    'サトノカルナバル': '2022105128',
    'エイシンワンド': '2022102849',
    'パンジャタワー': '2022101732',
    'ランフォーヴァウ': '2022105291',
    'コートアリシアン': '2022105326',
    'シャンパンカラー': '2020103075',
    'ネブラディスク': '2022105140',
    'マイエレメント': '2022101197',
    'ミッキージュエリー': '2022103245',
    'ジョバンニ': '2022103995',
    'リアライズシリウス': '2023103604',
    'レディネス': '2022104416',
    'タイセイカレント': '2022104588',
    'カレンラップスター': '2022104723',
    'サクラファレル': '2022104094',
    'ピコチャンブラック': '2022101745',
    'パープルレディ': '2018103558',
    'アスクシュタイン': '2022100161',
    'アルマヴェローチェ': '2022105110',
    'ソールオリエンス': '2020103608',
    'レガレイラ': '2021105426',
    'ベラジオオペラ': '2020103517',
    'ジャスティンパレス': '2019105056',
    'スターズオンアース': '2019105149',
    'シンエンペラー': '2021110142',
    'ディープボンド': '2017105318',
    'アドマイヤテラ': '2021105492',
    'エンブロイダリー': '2022105389',
    'オフトレイル': '2021110034',
    'スズハローム': '2020106822',
    'ガイアフォース': '2019105058',
    'シックスペンス': '2021105747',
    'ワールズエンド': '2021105537',
    'ウォーターリヒト': '2021101886',
    'エコロブルーム': '2021105393',
    'アドマイヤズーム': '2022105048',
    'アンパドゥ': '2021103306',
    'レモンポップ': '2018110080',
    'ウィルソンテソーロ': '2019100832',
    'ペプチドナイル': '2018102377',
    'クラウンプライド': '2019105404',
    'セラフィックコール': '2020103759',
    'サンライズジパング': '2021103601',
    'ヤマニンウルス': '2020102146',
    'ハギノアレグリアス': '2017105325',
    'ドゥラエレーデ': '2020103698',
    'ミックファイア': '2020104616',
    'グロリアムンディ': '2018105042',
    'スレイマン': '2018105139',
    'テーオードレフォン': '2019102421',
    'アーテルアストレア': '2019104863',
    'メイショウハリオ': '2017104953',
    'ブラウンラチェット': '2022105370',
    'カムニャック': '2022105198',
    'アルテヴェローチェ': '2022105030',
    'ピコローズ': '2020105500',
    'チェルヴィニア': '2021105423',
    'ステレンボッシュ': '2021105383',
    'クイーンズウォーク': '2021105504',
    'ショウナンラプンタ': '2021105380',
    'ダノンエアズロック': '2021105549',
    'ジャスティンミラノ': '2021105459'
}

def audit_and_enrich():
    print("=== 1. Loading existing databases ===")
    with open(HORSE_JSON, 'r', encoding='utf-8') as f:
        horse_db = json.load(f)
    with open(ENTRIES_JSON, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        preds = json.load(f)

    # 1. Fix Race 19 Japan Cup starter entries
    print("=== 2. Fixing Race 19 (Japan Cup) entries ===")
    r19_fixes = {
        'テアオ': {'jockey': 'L.トーレス', 'stable': 'J.サドラー (米)'},
        'ファイアンクランツ': {'jockey': 'J.モレイラ', 'stable': '堀宣行 (美浦)'},
        'ヘデントール': {'jockey': 'T.マーカンド', 'stable': '木村哲也 (美浦)'},
        'アーバンシック': {'jockey': 'A.プーシャン', 'stable': '武井亮 (美浦)'},
        'クロワデュノール': {'jockey': 'C.デムーロ', 'stable': '斉藤崇史 (栗東)'},
        'マスカレードボール': {'jockey': 'C.ルメール', 'stable': '手塚貴久 (美浦)'},
        'コスモキュランダ': {'jockey': '丹内祐次', 'stable': '加藤士津八 (美浦)'},
        'ゴリアット': {'jockey': 'C.スミヨン', 'stable': 'F.グラファール (仏)'},
        'カランダガン': {'jockey': 'M.バルザローナ', 'stable': 'F.グラファール (仏)'},
        'オンブズマン': {'jockey': 'W.ビュイック', 'stable': 'J&T.ゴスデン (英)'},
        'エシカルダイヤモンド': {'jockey': '坂井瑠星', 'stable': 'W.マリンズ (愛)'},
        'ミニーホーク': {'jockey': 'R.ムーア', 'stable': 'A.オブライエン (愛)'},
        'ダノンデサイル': {'jockey': '戸崎圭太', 'stable': '安田翔伍 (栗東)'},
        'タガノデュード': {'jockey': 'M.デムーロ', 'stable': '宮徹 (栗東)'},
        'シェイクユアハート': {'jockey': '古川吉洋', 'stable': '宮徹 (栗東)'},
        'エキサイトバイオ': {'jockey': '荻野極', 'stable': '今野貞一 (栗東)'},
        'メイショウタバル': {'jockey': '武豊', 'stable': '石橋守 (栗東)'},
        'ヴェルテンベルク': {'jockey': '横山典弘', 'stable': '宮本博 (栗東)'}
    }

    if '19' in entries:
        for s in entries['19']:
            name = s.get('horseName')
            if name in r19_fixes:
                s.update(r19_fixes[name])

    if 'races' in preds and '19' in preds['races']:
        for s in preds['races']['19'].get('starters', []):
            name = s.get('horseName')
            if name in r19_fixes:
                s.update(r19_fixes[name])
        for r in preds['races']['19'].get('ranking', []):
            name = r.get('horseName')
            if name in r19_fixes:
                r.update(r19_fixes[name])

    # Fix Race 21 クウネル -> アルマヴェローチェ
    print("=== 3. Fixing Race 21 (阪神JF) クウネル -> アルマヴェローチェ ===")
    if '21' in entries:
        for s in entries['21']:
            if s.get('horseName') == 'クウネル':
                s.update({
                    'horseName': 'アルマヴェローチェ',
                    'sexAge': '牝2',
                    'load': 55,
                    'jockey': '岩田望来',
                    'stable': '上村洋行 (栗東)'
                })

    if 'races' in preds and '21' in preds['races']:
        for s in preds['races']['21'].get('starters', []):
            if s.get('horseName') == 'クウネル':
                s.update({
                    'horseName': 'アルマヴェローチェ',
                    'sexAge': '牝2',
                    'load': 55,
                    'jockey': '岩田望来',
                    'stable': '上村洋行 (栗東)'
                })
        for r in preds['races']['21'].get('ranking', []):
            if r.get('horseName') == 'クウネル':
                r.update({
                    'horseName': 'アルマヴェローチェ',
                    'sexAge': '牝2',
                    'load': 55,
                    'jockey': '岩田望来',
                    'stable': '上村洋行 (栗東)'
                })

    # Save entries and predictions
    with open(ENTRIES_JSON, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    with open(ENTRIES_JS, 'w', encoding='utf-8') as f:
        f.write('export const ENTRIES_DATA = ' + json.dumps(entries, ensure_ascii=False, indent=2) + ';\n')

    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(preds, f, ensure_ascii=False, indent=2)
    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write('export const PREDICTION_DATA = ' + json.dumps(preds, ensure_ascii=False, indent=2) + ';\n')

    # 4. Collect all horses to enrich/audit
    all_target_horses = set()
    for starters in entries.values():
        if isinstance(starters, list):
            for s in starters:
                if isinstance(s, dict) and s.get('horseName'):
                    all_target_horses.add(s['horseName'])

    for p in preds.get('races', {}).values():
        for s in p.get('starters', []):
            if isinstance(s, dict) and s.get('horseName'):
                all_target_horses.add(s['horseName'])
        for r in p.get('ranking', []):
            if isinstance(r, dict) and r.get('horseName'):
                all_target_horses.add(r['horseName'])

    print(f"Total target horses across all active race cards: {len(all_target_horses)}")

    # 5. Apply curated foreign horses first
    for name, data in CURATED_FOREIGN.items():
        existing = horse_db.get(name, {})
        # preserve authentic career if longer
        if len(existing.get('career', [])) > len(data.get('career', [])):
            data['career'] = existing['career']
        horse_db[name] = data
        print(f"  Applied Curated Foreign: {name}")

    # 6. Fetch / Audit Japanese horses
    for name in sorted(all_target_horses):
        if name in CURATED_FOREIGN:
            continue

        existing = horse_db.get(name)
        # Check if existing profile is already good (has birthday, owner, pedigree without mojibake)
        has_good_data = False
        if existing:
            bday = existing.get('birthday', '-')
            owner = existing.get('owner', '-')
            sire = existing.get('pedigree', {}).get('sire', '')
            if bday != '-' and owner != '-' and sire and '' not in sire and '&nbsp;' not in sire:
                has_good_data = True

        if has_good_data:
            # Clean up &nbsp; in existing pedigree if any
            for k, v in existing.get('pedigree', {}).items():
                existing['pedigree'][k] = clean_text(v)
            continue

        # Needs fetch
        hid = KNOWN_IDS.get(name) or search_netkeiba_id(name)
        if hid:
            print(f"  Fetching NetKeiba for {name} (ID: {hid})...")
            fresh_data = fetch_netkeiba_horse(hid, name)
            # Retain photoUrl if existing had one and fresh didn't
            if not fresh_data.get('photoUrl') and existing and existing.get('photoUrl'):
                fresh_data['photoUrl'] = existing['photoUrl']
            horse_db[name] = fresh_data
            time.sleep(0.3)
        else:
            print(f"  [WARN] Could not find NetKeiba ID for {name}")

    # 7. Clean all remaining horses in horse_db of mojibake & &nbsp;
    for name, h in horse_db.items():
        if 'pedigree' in h and isinstance(h['pedigree'], dict):
            for k, v in h['pedigree'].items():
                if isinstance(v, str):
                    h['pedigree'][k] = clean_text(v)

    # Save enriched horse database
    print(f"=== Saving updated horse database ({len(horse_db)} horses) ===")
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(horse_db, f, ensure_ascii=False, indent=2)
    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write('export const HORSE_DATABASE = ' + json.dumps(horse_db, ensure_ascii=False, indent=2) + ';\n')

    print("=== Audit and Enrichment Complete! ===")

if __name__ == '__main__':
    audit_and_enrich()
