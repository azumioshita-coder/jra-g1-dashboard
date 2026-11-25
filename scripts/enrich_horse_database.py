import urllib.request
import urllib.parse
import re
import json
import time
import os
import html as html_lib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')

def decode_html(raw):
    for enc in ['utf-8', 'euc-jp', 'cp932']:
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode('utf-8', errors='replace')

def clean_text(text):
    if not text:
        return ''
    t = re.sub(r'<[^>]+>', '', text)
    t = html_lib.unescape(t)
    return t.replace('&nbsp;', ' ').replace('　', ' ').strip()

def fetch_horse_details(hid, name):
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
    
    # 1. Main Page
    main_url = f'https://db.netkeiba.com/horse/{hid}/'
    try:
        req = urllib.request.Request(main_url, headers=HEADERS)
        raw = urllib.request.urlopen(req, timeout=10).read()
        page_html = decode_html(raw)
        
        # English Name
        eng_m = re.search(r'<p class=\"eng_name\"[^>]*>([\s\S]*?)</p>', page_html)
        if eng_m:
            data['englishName'] = clean_text(eng_m.group(1)) or name

        # SexAge & Color
        txt01_m = re.search(r'<p class=\"txt_01\"[^>]*>([\s\S]*?)</p>', page_html)
        if txt01_m:
            txt01 = clean_text(txt01_m.group(1))
            parts = [p.strip() for p in txt01.split() if p.strip()]
            if len(parts) > 1:
                data['sexAge'] = parts[1]
            if len(parts) > 2:
                data['color'] = parts[2]

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
        prof = {}
        prof_m = re.search(r'<table[^>]*class=\"[^\"]*db_prof_table[^\"]*\"[^>]*>([\s\S]*?)</table>', page_html)
        if not prof_m:
            prof_m = re.search(r'<table summary=\"[^\"]*プロフィール\"[^>]*>([\s\S]*?)</table>', page_html)
        if prof_m:
            for tr in re.findall(r'<tr>([\s\S]*?)</tr>', prof_m.group(1)):
                th = re.search(r'<th>(.*?)</th>', tr)
                td = re.search(r'<td>(.*?)</td>', tr)
                if th and td:
                    k = clean_text(th.group(1))
                    v = clean_text(td.group(1)).replace('\n', ' ')
                    prof[k] = v

        if '生年月日' in prof: data['birthday'] = prof['生年月日']
        if '調教師' in prof: data['stable'] = prof['調教師']
        if '馬主' in prof: data['owner'] = prof['馬主']
        if '生産者' in prof: data['breeder'] = prof['生産者']
        if '産地' in prof: data['origin'] = prof['産地']
        if '通算成績' in prof: data['record'] = prof['通算成績']
        if '獲得賞金' in prof: data['earnings'] = prof['獲得賞金']
        if 'セレクトセール' in prof: data['price'] = prof['セレクトセール']
        
        # Titles
        if '主な勝鞍' in prof and prof['主な勝鞍']:
            titles = [t.strip() for t in prof['主な勝鞍'].split('、') if t.strip()]
            data['titles'] = titles

    except Exception as e:
        print(f"  [Main Page Error for {hid}]: {e}")

    # 2. Career Results Page
    res_url = f'https://db.netkeiba.com/horse/result/{hid}/'
    try:
        req = urllib.request.Request(res_url, headers=HEADERS)
        raw = urllib.request.urlopen(req, timeout=10).read()
        res_html = decode_html(raw)
        
        career = []
        tbl_m = re.search(r'<table[^>]*class=\"[^\"]*db_h_race_results[^\"]*\"[^>]*>([\s\S]*?)</table>', res_html)
        if tbl_m:
            rows = re.findall(r'<tr>([\s\S]*?)</tr>', tbl_m.group(1))
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
        print(f"  [Career Page Error for {hid}]: {e}")

    # 3. Pedigree Page
    ped_url = f'https://db.netkeiba.com/horse/ped/{hid}/'
    try:
        req = urllib.request.Request(ped_url, headers=HEADERS)
        raw = urllib.request.urlopen(req, timeout=10).read()
        ped_html = decode_html(raw)
        
        blood_m = re.search(r'<table[^>]+class=\"[^\"]*blood_table[^\"]*\"[^>]*>([\s\S]*?)</table>', ped_html)
        if blood_m:
            tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', blood_m.group(1))
            clean_tds = [clean_text(t).split('\n')[0].strip() for t in tds]
            if len(clean_tds) >= 32:
                data['pedigree'] = {
                    'sire': clean_tds[0],
                    'sireSire': clean_tds[1],
                    'sireDam': clean_tds[16] if len(clean_tds) > 16 else '',
                    'dam': clean_tds[32] if len(clean_tds) > 32 else (clean_tds[17] if len(clean_tds) > 17 else ''),
                    'damSire': clean_tds[33] if len(clean_tds) > 33 else (clean_tds[18] if len(clean_tds) > 18 else ''),
                    'damDam': clean_tds[48] if len(clean_tds) > 48 else ''
                }
    except Exception as e:
        print(f"  [Pedigree Page Error for {hid}]: {e}")

    return data

def save_db(db):
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write('export const HORSE_DATABASE = ' + json.dumps(db, ensure_ascii=False, indent=2) + ';\n')
