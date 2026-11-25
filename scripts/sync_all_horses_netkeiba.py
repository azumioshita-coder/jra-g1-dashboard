import concurrent.futures
import json
import os
import re
import urllib.request
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
PRED_JSON = os.path.join(BASE_DIR, 'src', 'prediction_data.json')
PRED_JS = os.path.join(BASE_DIR, 'src', 'prediction_data.js')
VERIFIED_IDS_FILE = os.path.join(BASE_DIR, 'scripts', 'data', 'verified_netkeiba_ids.json')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

def fetch_html(url, retries=2):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                return resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            if i == retries - 1:
                return None
            time.sleep(1)
    return None

def parse_horse(name, hid):
    # 1. Profile
    prof_url = f'https://db.netkeiba.com/horse/{hid}/'
    p_html = fetch_html(prof_url)
    prof = {}
    if p_html:
        for m in re.finditer(r'<th>(.*?)</th>\s*<td>(.*?)</td>', p_html, re.DOTALL):
            th = re.sub(r'<.*?>', '', m.group(1)).strip()
            td = re.sub(r'<.*?>', '', m.group(2)).strip()
            prof[th] = td
        raw_titles = prof.get('主な勝鞍', '')
        titles = []
        if raw_titles and raw_titles != '-':
            for t in re.split(r'[,、\n]', raw_titles):
                t_clean = t.strip()
                if t_clean:
                    titles.append(t_clean)
        prof['titles_list'] = titles

    # 2. Career
    res_url = f'https://db.netkeiba.com/horse/result/{hid}/'
    r_html = fetch_html(res_url)
    career = []
    if r_html:
        table = re.search(r'<table[^>]*class=\"[^\"]*(?:db_h_race_results|race_table_01)[^\"]*\"[^>]*>(.*?)</table>', r_html, re.DOTALL)
        if table:
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table.group(1), re.DOTALL)
            for r in rows[1:]:
                cols = [re.sub(r'<.*?>', '', c).replace('&nbsp;', '').strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL)]
                if len(cols) < 20:
                    continue
                rival = cols[31] if len(cols) > 31 else ''
                rival = re.sub(r'[\(\)]', '', rival).strip()

                career.append({
                    'date': cols[0].replace('/', '-'),
                    'venue': cols[1],
                    'weather': cols[2],
                    'raceNum': cols[3],
                    'race': cols[4],
                    'starters': cols[6],
                    'bracket': cols[7],
                    'gate': cols[8],
                    'odds': cols[9],
                    'pop': cols[10],
                    'rank': cols[11],
                    'jockey': cols[12],
                    'load': cols[13],
                    'course': cols[14],
                    'track': cols[16],
                    'time': cols[18],
                    'margin': cols[19],
                    'passing': cols[25] if len(cols) > 25 else '',
                    'pace': cols[26] if len(cols) > 26 else '',
                    'agari': cols[27] if len(cols) > 27 else '',
                    'weight': cols[28] if len(cols) > 28 else '',
                    'rival': rival
                })

    return name, hid, prof, career

def main():
    with open(VERIFIED_IDS_FILE, 'r', encoding='utf-8') as f:
        verified_ids = json.load(f)

    with open(HORSE_JSON, 'r', encoding='utf-8') as f:
        hd = json.load(f)

    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        pd = json.load(f)

    print(f"Starting authentic NetKeiba sync for {len(verified_ids)} horses...")

    updated_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(parse_horse, name, hid): name for name, hid in verified_ids.items()}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                name, hid, prof, career = future.result()
                if name not in hd:
                    hd[name] = {"name": name}
                h = hd[name]
                h['netkeiba_id'] = hid

                # Update profile fields if found on netkeiba
                if prof.get('生年月日'):
                    h['birthday'] = prof['生年月日']
                if prof.get('調教師'):
                    h['stable'] = prof['調教師']
                if '馬主' in prof:
                    h['owner'] = prof['馬主'] if prof['馬主'] else '-'
                if '生産者' in prof:
                    h['breeder'] = prof['生産者'] if prof['生産者'] else '-'
                if '産地' in prof:
                    h['origin'] = prof['産地'] if prof['産地'] else ''
                if prof.get('通算成績'):
                    h['record'] = prof['通算成績']
                if prof.get('獲得賞金 (中央)'):
                    h['earnings'] = prof['獲得賞金 (中央)']
                if prof.get('titles_list'):
                    h['titles'] = prof['titles_list']

                # Update career
                if career:
                    h['career'] = career
                    updated_count += 1
                    latest_r = career[0]
                    # print short status
                    print(f"[{name}] {len(career)} races -> Latest: {latest_r['date']} {latest_r['race']} {latest_r['rank']}着 ({latest_r['jockey']})")
                else:
                    print(f"[{name}] Warning: No career found on NetKeiba")
            except Exception as e:
                print(f"[{name}] Error syncing: {e}")

    # Save to src/horse_data.json and src/horse_data.js
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(hd, f, ensure_ascii=False, indent=2)

    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(hd, ensure_ascii=False, indent=2) + ";\n")

    print(f"\nSuccessfully updated {updated_count} horses in horse_data.json & horse_data.js!")

    # Now synchronize lastRace across all starters in prediction_data.json
    starters_updated = 0
    for rid, r in pd.get('races', {}).items():
        for s in r.get('starters', []):
            hname = s.get('horseName')
            if hname in hd and hd[hname].get('career'):
                latest = hd[hname]['career'][0]
                r_name = latest['race'].replace('GIII', 'G3').replace('GII', 'G2').replace('GI', 'G1')
                # Format: "天皇賞（秋）(G1) 1着"
                new_last_race = f"{r_name} {latest['rank']}着"
                old_last_race = s.get('lastRace')
                if old_last_race != new_last_race:
                    s['lastRace'] = new_last_race
                    starters_updated += 1
                    print(f"Race {rid} [{hname}] updated lastRace: '{old_last_race}' -> '{new_last_race}'")

    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(pd, f, ensure_ascii=False, indent=2)

    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write("export const PREDICTION_DATA = " + json.dumps(pd, ensure_ascii=False, indent=2) + ";\n")

    print(f"\nSuccessfully updated {starters_updated} starter entries in prediction_data.json & prediction_data.js!")

if __name__ == '__main__':
    main()
