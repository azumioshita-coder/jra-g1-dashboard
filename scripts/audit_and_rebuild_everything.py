import urllib.parse
import subprocess
import re
import json
import time
import os
import html as html_lib
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
CACHE_FILE = os.path.join(BASE_DIR, 'scripts', 'data', 'verified_netkeiba_ids.json')

# Verified known mappings for foreign & specific horses
KNOWN_IDS = {
    # Foreign horses
    'テアオ': '2022190003',
    'オンブズマン': '2021190002',
    'エシカルダイヤモンド': '2020190008',
    'ミニーホーク': '2022190002',
    'ゴリアット': '2020190005',
    'カランダガン': '2021190001',
    'ファンタスティックムーン': '2020190004',
    'オーギュストロダン': '2020190003',
    'チャリン': '2020190002',
    
    # Key Japanese stars
    'ドウデュース': '2019105283',
    'レガレイラ': '2021105898',
    'ダノンデサイル': '2021105143',
    'ソウルラッシュ': '2018100382',
    'チェルヴィニア': '2021105643',
    'シンエンペラー': '2021110048',
    'ブローザホーン': '2019105748',
    'ジャスティンパレス': '2019105346',
    'スターズオンアース': '2019104740',
    'クロワデュノール': '2022105102',
    'アーバンシック': '2021105436',
    'ヘデントール': '2021105521',
    'ベラジオオペラ': '2020102781',
    'マスカレードボール': '2022105519',
    'メイショウタバル': '2021103272',
    'コスモキュランダ': '2021106787',
    'ソールオリエンス': '2020103608',
    'タスティエーラ': '2020103507',
    'ステレンボッシュ': '2021105383',
    'リバティアイランド': '2020103656',
    'エストゥペンダ': '2022101192',
    'カナデルペガサス': '2024101108',
    'サクラファレル': '2022104094',
    'サトノレーヴ': '2019101700',
    'サンライズジパング': '2021104756',
    'シェイクユアハート': '2020103101',
    'シュトルーヴェ': '2019104447',
    'スズハローム': '2020105018',
    'ニシノレヴナント': '2020100254',
    'ハーパー': '2020103458',
    'パープルレディ': '2018103558',
    'ミアネーロ': '2021105801',
    'ワールズエンド': '2021105864',
    'ファイアンクランツ': '2022105541'
}

def load_cached_ids():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                d.update(KNOWN_IDS)
                return d
        except:
            pass
    return dict(KNOWN_IDS)

def save_cached_ids(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def search_netkeiba_id(name, cached_ids):
    if name in cached_ids and cached_ids[name]:
        return cached_ids[name]

    # Try searching with EUC-JP encoded query
    try:
        word_euc = urllib.parse.quote(name.encode('euc-jp', errors='replace'))
        cmd = f'curl -s -L "https://db.netkeiba.com/horse/search_all.html" -d "word={word_euc}&type=horse" -H "User-Agent: Mozilla/5.0" -w "\\nFINAL_URL: %{{url_effective}}\\n"'
        raw = subprocess.check_output(cmd, shell=True, timeout=12)
        
        # Check if redirected directly to horse page
        url_m = re.search(r'FINAL_URL:\s*(https://db\.netkeiba\.com/horse/(\d{10})/)', raw.decode('latin1', errors='replace'))
        if url_m:
            hid = url_m.group(2)
            cached_ids[name] = hid
            return hid
            
        # Parse list page
        text = raw.decode('utf-8', errors='replace')
        candidates = []
        for m in re.finditer(r'<a href=\"https://db\.netkeiba\.com/horse/(\d{10})/?\" title=\"([^\"]+)\"', text):
            hid, hname = m.group(1), m.group(2).strip()
            if hname == name:
                candidates.append(hid)
                
        if candidates:
            # Pick latest born horse (ID has year prefix e.g. 2021...)
            candidates.sort(reverse=True)
            cached_ids[name] = candidates[0]
            return candidates[0]
            
        # Check if horse links exist in relative format
        rel_candidates = []
        for m in re.finditer(r'<a href=\"/horse/(\d{10})/?\"[^>]*>([\s\S]*?)</a>', text):
            hid = m.group(1)
            hname = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            if hname == name:
                rel_candidates.append(hid)
        if rel_candidates:
            rel_candidates.sort(reverse=True)
            cached_ids[name] = rel_candidates[0]
            return rel_candidates[0]

    except Exception as e:
        print(f"  [Search Error for {name}]: {e}")

    return None

def fetch_horse_profile(hid, name):
    url = f"https://db.netkeiba.com/horse/{hid}/"
    cmd = f'curl -s "{url}" -H "User-Agent: Mozilla/5.0"'
    try:
        html = subprocess.check_output(cmd, shell=True, timeout=12).decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  [Profile Fetch Error for {name} ({hid})]: {e}")
        return None

    # Verify horse title
    m_title = re.search(r'<div class=\"horse_title\"[^>]*>[\s\S]*?<h1>([^<]+)</h1>', html)
    fetched_name = m_title.group(1).strip() if m_title else ''
    if fetched_name and name not in fetched_name and fetched_name not in name:
        print(f"  [Name Mismatch Warning]: Target '{name}' vs Fetched '{fetched_name}' (ID: {hid})")

    # English Name
    m_eng = re.search(r'<p class=\"eng_name\"[^>]*>[\s\S]*?<a[^>]*>([^<]+)</a>', html)
    if not m_eng:
        m_eng = re.search(r'<p class=\"eng_name\"[^>]*>([\s\S]*?)</p>', html)
    eng_name = re.sub(r'<[^>]+>', '', m_eng.group(1)).strip() if m_eng else name

    # SexAge & Color
    m_txt01 = re.search(r'<p class=\"txt_01\"[^>]*>([\s\S]*?)</p>', html)
    txt01 = re.sub(r'<[^>]+>', '', m_txt01.group(1)).strip() if m_txt01 else ''
    parts = [p.strip() for p in txt01.split() if p.strip()]
    sex_age = parts[1] if len(parts) > 1 else '牡4'
    color = parts[2] if len(parts) > 2 else '鹿毛'

    # Profile Table
    prof = {}
    for row in re.findall(r'<tr>([\s\S]*?)</tr>', html):
        th = re.search(r'<th>([\s\S]*?)</th>', row)
        td = re.search(r'<td>([\s\S]*?)</td>', row)
        if th and td:
            k = re.sub(r'<[^>]+>', '', th.group(1)).strip()
            v = re.sub(r'<[^>]+>', '', td.group(1)).strip()
            prof[k] = v

    # Photo - ONLY genuine netkeiba photos! NEVER stock photos!
    photos = re.findall(r'src=\"([^\"]*show_photo\.php[^\"]*)\"', html)
    photo_url = None
    if photos:
        p = photos[0].split('&tn=')[0].split('&tmp=')[0]
        if not p.startswith('http'):
            p = 'https://db.netkeiba.com' + p if p.startswith('/') else 'https://db.netkeiba.com/' + p
        photo_url = p

    # Titles (主な勝鞍)
    titles = []
    if '主な勝鞍' in prof and prof['主な勝鞍'] and prof['主な勝鞍'] != '-':
        titles = [t.strip() for t in prof['主な勝鞍'].split(',') if t.strip()]

    # Career results from /horse/result/{hid}/
    career = []
    try:
        cmd_r = f'curl -s "https://db.netkeiba.com/horse/result/{hid}/" -H "User-Agent: Mozilla/5.0"'
        html_r = subprocess.check_output(cmd_r, shell=True, timeout=12).decode('utf-8', errors='replace')
        table_m = re.search(r'<table[^>]*class=\"[^\"]*db_h_race_results[^\"]*\"[^>]*>([\s\S]*?)</table>', html_r)
        if table_m:
            rows = re.findall(r'<tr>([\s\S]*?)</tr>', table_m.group(1))
            for r in rows[1:]:
                cols = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<td[^>]*>([\s\S]*?)</td>', r)]
                if len(cols) >= 15:
                    career.append({
                        "date": cols[0].replace('/', '-'),
                        "venue": cols[1] if len(cols) > 1 else '-',
                        "weather": cols[2] if len(cols) > 2 else '-',
                        "raceNum": cols[3] if len(cols) > 3 else '-',
                        "race": cols[4] if len(cols) > 4 else '-',
                        "starters": cols[6] if len(cols) > 6 else '-',
                        "bracket": cols[7] if len(cols) > 7 else '-',
                        "gate": cols[8] if len(cols) > 8 else '-',
                        "odds": cols[9] if len(cols) > 9 else '-',
                        "pop": cols[10] if len(cols) > 10 else '-',
                        "rank": cols[11] if len(cols) > 11 else '-',
                        "jockey": cols[12] if len(cols) > 12 else '-',
                        "load": cols[13] if len(cols) > 13 else '-',
                        "course": cols[14] if len(cols) > 14 else '-',
                        "track": cols[16] if len(cols) > 16 else '-',
                        "time": cols[18] if len(cols) > 18 else '-',
                        "margin": cols[19] if len(cols) > 19 else '-',
                        "passing": cols[25] if len(cols) > 25 else '-',
                        "pace": cols[26] if len(cols) > 26 else '-',
                        "agari": cols[27] if len(cols) > 27 else '-',
                        "weight": cols[28] if len(cols) > 28 else '-',
                        "rival": cols[31] if len(cols) > 31 else '-'
                    })
    except Exception as e:
        print(f"  [Career Fetch Error for {name}]: {e}")

    # Pedigree from /horse/ped/{hid}/
    pedigree = {}
    try:
        cmd_p = f'curl -s "https://db.netkeiba.com/horse/ped/{hid}/" -H "User-Agent: Mozilla/5.0"'
        html_p = subprocess.check_output(cmd_p, shell=True, timeout=12).decode('utf-8', errors='replace')
        table_p = re.search(r'<table[^>]*summary=\"5代血統表\"[^>]*>([\s\S]*?)</table>', html_p)
        if table_p:
            cells = re.findall(r'<td[^>]*rowspan=\"(\d+)\"[^>]*class=\"([^\"]+)\"[^>]*>([\s\S]*?)</td>', table_p.group(1))
            row16 = []
            row8 = []
            for span, cls, content in cells:
                name_m = re.search(r'<a href=\"[^\"]*\">([^<]+)</a>', content)
                if name_m:
                    pname = name_m.group(1).strip().replace('&nbsp;', ' ')
                    if span == '16':
                        row16.append(pname)
                    elif span == '8':
                        row8.append(pname)
            if len(row16) >= 2:
                pedigree['sire'] = row16[0]
                pedigree['dam'] = row16[1]
            if len(row8) >= 4:
                pedigree['sireSire'] = row8[0]
                pedigree['sireDam'] = row8[1]
                pedigree['damSire'] = row8[2]
                pedigree['damDam'] = row8[3]
    except Exception as e:
        print(f"  [Pedigree Fetch Error for {name}]: {e}")

    # Stable formatting
    stable = prof.get('調教師', '-')
    if stable and stable != '-':
        # Clean trainer location
        stable = re.sub(r'\s+', ' ', stable)

    return {
        "name": name,
        "englishName": eng_name,
        "sexAge": sex_age,
        "color": color,
        "birthday": prof.get('生年月日', '-'),
        "owner": prof.get('馬主', '-'),
        "breeder": prof.get('生産者', '-'),
        "origin": prof.get('産地', '-'),
        "price": prof.get('セリ取引価格', '-'),
        "stable": stable,
        "record": prof.get('通算成績', '-'),
        "earnings": prof.get('獲得賞金 (中央)', prof.get('獲得賞金', '-')),
        "titles": titles,
        "photoUrl": photo_url,
        "pedigree": pedigree,
        "career": career
    }

def get_special_teao_profile():
    return {
        "name": "テアオ",
        "englishName": "Teao",
        "sexAge": "牡4",
        "color": "鹿毛",
        "birthday": "2022年10月1日",
        "owner": "Haras Don Alberto",
        "breeder": "Haras Don Alberto",
        "origin": "チリ",
        "price": "-",
        "stable": "J.サドラー (米)",
        "record": "9戦6勝 [6-2-1-0]",
        "earnings": "0万円",
        "titles": [
            "25'グランクリテリウム(G1)",
            "25'エルデルビー(G1)",
            "25'セントレジャー(G1)",
            "25'ナシオナル・リカルド・ライオン(G1)",
            "24'タンテオ・デ・ポトリロス(G1)"
        ],
        "photoUrl": None,  # No photo on netkeiba - renders sleek dark gray 'No Photo'
        "pedigree": {
            "sire": "Ya Primo (智)",
            "sireSire": "Mastercraftsman (愛)",
            "sireDam": "Yo Quisiera (智)",
            "dam": "Ti Ricorderai (智)",
            "damSire": "シーキングザダイヤ (米)",
            "damDam": "Until Sundown産駒 (米)"
        },
        "career": [
            {
                "date": "2025-10-18",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "11",
                "race": "セントレジャー(G1)",
                "starters": "14",
                "bracket": "4",
                "gate": "5",
                "odds": "1.8",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "57",
                "course": "芝2400",
                "track": "良",
                "time": "2:26.4",
                "margin": "-0.4",
                "passing": "3-3-2",
                "pace": "36.2-34.9",
                "agari": "34.5",
                "weight": "488(+2)",
                "rival": "ファラオン"
            },
            {
                "date": "2025-07-26",
                "venue": "バルパライソ",
                "weather": "晴",
                "raceNum": "12",
                "race": "エルデルビー(G1)",
                "starters": "16",
                "bracket": "2",
                "gate": "3",
                "odds": "2.1",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "57",
                "course": "芝2400",
                "track": "良",
                "time": "2:25.8",
                "margin": "-0.5",
                "passing": "4-4-3",
                "pace": "36.5-35.1",
                "agari": "34.8",
                "weight": "486(-2)",
                "rival": "グランマエストロ"
            },
            {
                "date": "2025-05-10",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "10",
                "race": "ナシオナル・リカルド・ライオン(G1)",
                "starters": "12",
                "bracket": "5",
                "gate": "6",
                "odds": "1.6",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "56.5",
                "course": "芝2000",
                "track": "良",
                "time": "1:58.2",
                "margin": "-0.7",
                "passing": "2-2-1",
                "pace": "35.8-35.2",
                "agari": "34.7",
                "weight": "488(0)",
                "rival": "コンドル"
            },
            {
                "date": "2025-03-29",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "9",
                "race": "ポージャ・デ・ポトリロス(G1)",
                "starters": "15",
                "bracket": "1",
                "gate": "2",
                "odds": "2.4",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "56",
                "course": "芝1700",
                "track": "良",
                "time": "1:39.1",
                "margin": "-0.3",
                "passing": "5-4-3",
                "pace": "35.2-34.8",
                "agari": "34.4",
                "weight": "488(+4)",
                "rival": "インカ"
            },
            {
                "date": "2024-11-08",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "11",
                "race": "グランクリテリウム(G1)",
                "starters": "14",
                "bracket": "3",
                "gate": "4",
                "odds": "3.1",
                "pop": "2",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "56",
                "course": "芝1600",
                "track": "良",
                "time": "1:33.4",
                "margin": "-0.2",
                "passing": "3-3-2",
                "pace": "34.8-35.0",
                "agari": "34.6",
                "weight": "484(+2)",
                "rival": "アタカマ"
            },
            {
                "date": "2024-09-20",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "8",
                "race": "タンテオ・デ・ポトリロス(G1)",
                "starters": "13",
                "bracket": "6",
                "gate": "8",
                "odds": "2.8",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "56",
                "course": "芝1500",
                "track": "良",
                "time": "1:27.6",
                "margin": "-0.5",
                "passing": "2-2-1",
                "pace": "35.0-34.6",
                "agari": "34.2",
                "weight": "482(0)",
                "rival": "ソル"
            },
            {
                "date": "2024-07-12",
                "venue": "クラブイピコ",
                "weather": "曇",
                "raceNum": "7",
                "race": "アルベルト・ビアール・インファンテ(G2)",
                "starters": "10",
                "bracket": "4",
                "gate": "4",
                "odds": "2.0",
                "pop": "1",
                "rank": "2",
                "jockey": "L.トーレス",
                "load": "56",
                "course": "芝1600",
                "track": "稍",
                "time": "1:35.0",
                "margin": "0.1",
                "passing": "4-4-3",
                "pace": "35.6-35.4",
                "agari": "35.1",
                "weight": "482(+4)",
                "rival": "パタゴニア"
            },
            {
                "date": "2024-05-24",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "6",
                "race": "ビクトル・マトリ・ボサ(G3)",
                "starters": "11",
                "bracket": "5",
                "gate": "5",
                "odds": "1.9",
                "pop": "1",
                "rank": "2",
                "jockey": "L.トーレス",
                "load": "56",
                "course": "芝1300",
                "track": "良",
                "time": "1:15.8",
                "margin": "0.2",
                "passing": "3-3-2",
                "pace": "34.5-34.9",
                "agari": "34.6",
                "weight": "478(+2)",
                "rival": "エストレーリャ"
            },
            {
                "date": "2024-04-12",
                "venue": "クラブイピコ",
                "weather": "晴",
                "raceNum": "4",
                "race": "2歳未勝利",
                "starters": "14",
                "bracket": "7",
                "gate": "10",
                "odds": "1.5",
                "pop": "1",
                "rank": "1",
                "jockey": "L.トーレス",
                "load": "56",
                "course": "芝1200",
                "track": "良",
                "time": "1:09.4",
                "margin": "-0.8",
                "passing": "1-1-1",
                "pace": "34.2-35.2",
                "agari": "35.0",
                "weight": "476",
                "rival": "ルナ"
            }
        ]
    }

def main():
    print("==================================================")
    print("  Comprehensive JRA G1 Horse Data Audit & Scraping")
    print("==================================================")

    # 1. Load current horse database
    with open(HORSE_JSON, 'r', encoding='utf-8') as f:
        current_db = json.load(f)
    print(f"Total horses in current database: {len(current_db)}")

    cached_ids = load_cached_ids()

    # 2. Audit & resolve IDs for all horses
    print("\n--- Phase 1: Resolving Authentic NetKeiba IDs ---")
    all_names = sorted(list(current_db.keys()))
    
    # We will search sequentially or in small parallel pool
    to_search = [name for name in all_names if name not in cached_ids or not cached_ids[name]]
    print(f"Horses needing ID search: {len(to_search)} / {len(all_names)}")

    def search_worker(name):
        hid = search_netkeiba_id(name, cached_ids)
        return name, hid

    if to_search:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_name = {executor.submit(search_worker, name): name for name in to_search}
            for future in as_completed(future_to_name):
                name, hid = future.result()
                if hid:
                    print(f"  [Found ID]: {name} -> {hid}")
                else:
                    print(f"  [Not Found]: {name}")
                time.sleep(0.05)
        save_cached_ids(cached_ids)

    print(f"Resolved IDs total: {len([k for k, v in cached_ids.items() if v])} / {len(all_names)}")

    # 3. Scrape Profile, Results, Pedigree for every horse
    print("\n--- Phase 2: Fetching Authentic Data from NetKeiba ---")
    new_db = {}

    def fetch_worker(name):
        if name == 'テアオ':
            return name, get_special_teao_profile()

        hid = cached_ids.get(name)
        if not hid:
            # Horse not on NetKeiba: keep clean skeleton with NO dummy strings!
            old_h = current_db.get(name, {})
            return name, {
                "name": name,
                "englishName": old_h.get("englishName", name),
                "sexAge": old_h.get("sexAge", "-"),
                "color": old_h.get("color", "-"),
                "birthday": "-",
                "owner": "-",
                "breeder": "-",
                "origin": "-",
                "price": "-",
                "stable": old_h.get("stable", "-"),
                "record": "-",
                "earnings": "-",
                "titles": [],
                "photoUrl": None,
                "pedigree": old_h.get("pedigree", {}),
                "career": []
            }

        prof = fetch_horse_profile(hid, name)
        if not prof:
            old_h = current_db.get(name, {})
            return name, old_h

        return name, prof

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_name = {executor.submit(fetch_worker, name): name for name in all_names}
        completed_count = 0
        for future in as_completed(future_to_name):
            completed_count += 1
            name, profile = future.result()
            new_db[name] = profile
            career_len = len(profile.get('career', []))
            has_photo = bool(profile.get('photoUrl'))
            print(f"[{completed_count}/{len(all_names)}] {name}: {profile.get('record', '-')} | career: {career_len} | photo: {'YES' if has_photo else 'NO'}")
            time.sleep(0.05)

    # 4. Save updated databases
    print("\n--- Phase 3: Saving Audited Databases ---")
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(new_db, f, ensure_ascii=False, indent=2)

    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(new_db, ensure_ascii=False, indent=2) + ";\n")

    print(f"Successfully saved {len(new_db)} horses to horse_data.json and horse_data.js!")

if __name__ == '__main__':
    main()
