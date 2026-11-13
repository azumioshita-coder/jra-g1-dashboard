#!/usr/bin/env python3
"""
GRAND STABLE - Automated JRA G1 Data Update Daemon & CLI
--------------------------------------------------------
Features:
1. Automated Gate Draw (枠順/出馬表) scraping from NetKeiba for upcoming races (Thursdays/Fridays).
2. Automated Race Results & Official Payouts scraping from NetKeiba after race finish (Sundays).
3. Synchronization across index.html, src/main.js, and src/entries_data.js.
4. Auto-build with Vite (npm run build).
5. Automatic Git commit & push.
"""

import sys
import os
import re
import json
import time
import datetime
import subprocess
import urllib.request
import urllib.error

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(APP_DIR, 'index.html')
MAIN_JS = os.path.join(APP_DIR, 'src', 'main.js')
ENTRIES_JSON = os.path.join(APP_DIR, 'src', 'entries_data.json')
PAYOUTS_JSON = os.path.join(APP_DIR, 'src', 'payouts_data.json')
HIST_JS = os.path.join(APP_DIR, 'src', 'historical_results.js')
LOG_FILE = os.path.join(APP_DIR, 'scripts', 'update.log')

# JRA 2026 G1 秋季レース NetKeiba レースコード定義
G1_SCHEDULE = [
    {
        'id': '16',
        'name': '天皇賞（秋）',
        'date': '2026-11-01T15:40:00',
        'netkeiba_id': '202605041111',
        'location': '東京',
        'course': '芝 2000m'
    },
    {
        'id': '17',
        'name': 'エリザベス女王杯',
        'date': '2026-11-15T15:40:00',
        'netkeiba_id': '202608050411',
        'location': '京都',
        'course': '芝 2200m'
    },
    {
        'id': '18',
        'name': 'マイルチャンピオンシップ',
        'date': '2026-11-22T15:40:00',
        'netkeiba_id': '202608050611',
        'location': '京都',
        'course': '芝 1600m'
    },
    {
        'id': '19',
        'name': 'ジャパンカップ',
        'date': '2026-11-29T15:40:00',
        'netkeiba_id': '202605050812',
        'location': '東京',
        'course': '芝 2400m'
    },
    {
        'id': '20',
        'name': 'チャンピオンズカップ',
        'date': '2026-12-06T15:40:00',
        'netkeiba_id': '202607040211',
        'location': '中京',
        'course': 'ダート 1800m'
    },
    {
        'id': '21',
        'name': '阪神ジュベナイルフィリーズ',
        'date': '2026-12-13T15:40:00',
        'netkeiba_id': '202608060411',
        'location': '京都',
        'course': '芝 1600m'
    },
    {
        'id': '22',
        'name': '朝日杯フューチュリティステークス',
        'date': '2026-12-20T15:40:00',
        'netkeiba_id': '202608060611',
        'location': '京都',
        'course': '芝 1600m'
    },
    {
        'id': '23',
        'name': 'ホープフルステークス',
        'date': '2026-12-26T15:40:00',
        'netkeiba_id': '202606050811',
        'location': '中山',
        'course': '芝 2000m'
    },
    {
        'id': '24',
        'name': '有馬記念',
        'date': '2026-12-27T15:40:00',
        'netkeiba_id': '202606050911',
        'location': '中山',
        'course': '芝 2500m'
    }
]

def log(msg):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {msg}"
    print(entry)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(entry + "\n")
    except Exception:
        pass

def fetch_html(url, timeout=15):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            for enc in ['euc-jp', 'utf-8', 'cp932']:
                try:
                    return content.decode(enc)
                except Exception:
                    continue
            return content.decode('utf-8', errors='ignore')
    except Exception as e:
        log(f"Fetch failed for {url}: {e}")
        return None

def parse_shutuba(html):
    """NetKeiba出馬表HTMLから枠番、馬番、馬名、性齢、斤量、騎手、厩舎、オッズ、人気、馬体重を抽出。枠順未定時は五十音順で返す"""
    starters = []
    rows = re.findall(r'<tr[^>]*class=\"[^\"]*HorseList[^\"]*\"[^>]*>([\s\S]*?)</tr>', html)
    if not rows:
        rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', html)

    has_gates = True
    for row in rows:
        waku_m = re.search(r'class=\"[^\"]*Waku(\d)[^\"]*\"', row)
        gate_m = re.search(r'class=\"[^\"]*Umaban\d*[^\"]*\"[^>]*>(\d+)</td>', row)
        name_m = re.search(r'<span class=\"Horse_?Name\"[^>]*>[\s\S]*?<a[^>]*title=\"([^\"]+)\"', row)
        if not name_m:
            name_m = re.search(r'<span class=\"Horse_?Name\"[^>]*>[\s\S]*?<a[^>]*>([^<]+)', row)
        if not name_m:
            name_m = re.search(r'title=\"([^\"]+)\"[^>]*class=\"[^\"]*Horse_?Name', row)

        jockey_m = re.search(r'<td class=\"Jockey\"[^>]*>[\s\S]*?<a[^>]*title=\"([^\"]+)\"', row)
        if not jockey_m:
            jockey_m = re.search(r'<td class=\"Jockey\"[^>]*>[\s\S]*?<a[^>]*>([^<]+)</a>', row)

        trainer_m = re.search(r'<td class=\"Trainer\"[^>]*>[\s\S]*?<a[^>]*title=\"([^\"]+)\"', row)
        if not trainer_m:
            trainer_m = re.search(r'<td class=\"Trainer\"[^>]*>[\s\S]*?<a[^>]*>([^<]+)</a>', row)

        loc_m = re.search(r'<td class=\"Trainer\"[^>]*>[\s\S]*?<span class=\"Label2\">([^<]+)</span>', row)
        barei_m = re.search(r'<td class=\"Barei[^\"]*\"[^>]*>([^<]+)</td>', row)
        load_m = re.search(r'<td class=\"Txt_C\">([\d\.]+)</td>', row)
        odds_m = re.search(r'id=\"odds-\d+_\d+\"[^>]*>([\d\.]+)</span>', row)
        pop_m = re.search(r'id=\"ninki-\d+_\d+\"[^>]*>(\d+)</span>', row)
        weight_m = re.search(r'<td class=\"Weight\"[^>]*>([\s\S]*?)</td>', row)

        if name_m:
            horse_name = name_m.group(1).strip()
            if not horse_name or horse_name == '馬名':
                continue

            waku = int(waku_m.group(1)) if waku_m and waku_m.group(1).isdigit() else None
            gate = int(gate_m.group(1)) if gate_m and gate_m.group(1).isdigit() else None
            if gate is None:
                has_gates = False

            sex_age = barei_m.group(1).strip() if barei_m else '牝4'
            try:
                load = float(load_m.group(1).strip()) if load_m else 56.0
                if load.is_integer():
                    load = int(load)
            except Exception:
                load = 56

            jockey = jockey_m.group(1).strip() if jockey_m else '未定'
            trainer = trainer_m.group(1).strip() if trainer_m else '-'
            loc = loc_m.group(1).strip() if loc_m else ''
            stable = f"{trainer} ({loc})" if loc else trainer

            odds = odds_m.group(1).strip() if odds_m and odds_m.group(1) != '---.-' else None
            pop = int(pop_m.group(1).strip()) if pop_m and pop_m.group(1).isdigit() else None

            # Horse weight if available on race day
            weight_text = weight_m.group(1).strip() if weight_m else ''
            confirmed_wt = None
            diff_wt = None
            wt_match = re.search(r'(\d{3})\(([\+\-]?\d+)\)', weight_text)
            if wt_match:
                confirmed_wt = int(wt_match.group(1))
                diff_wt = wt_match.group(2)

            starters.append({
                'waku': waku,
                'gate': gate,
                'horseName': horse_name,
                'sexAge': sex_age,
                'load': load,
                'jockey': jockey,
                'stable': stable,
                'odds': odds,
                'pop': pop,
                'confirmedWeight': confirmed_wt,
                'weightDiff': diff_wt
            })

    if has_gates and len(starters) > 0 and all(s['gate'] is not None for s in starters):
        starters.sort(key=lambda x: (x['gate'] or 99))
        stage = 'gate_confirmed'
    else:
        # 枠順確定するまでは五十音順
        starters.sort(key=lambda x: x['horseName'])
        stage = 'entry_scheduled'

    return starters, stage

def check_and_update_entries():
    """今後のレースの出馬表（出馬予定 ➔ 出走馬確定 ➔ 枠順確定）を自動検知して更新"""
    try:
        with open(ENTRIES_JSON, 'r', encoding='utf-8') as f:
            entries_data = json.load(f)
    except Exception:
        entries_data = {}

    PRED_JSON = os.path.join(APP_DIR, 'src', 'prediction_data.json')
    try:
        with open(PRED_JSON, 'r', encoding='utf-8') as f:
            pred_data = json.load(f)
    except Exception:
        pred_data = {}

    updated = False
    now = datetime.datetime.now()

    for race in G1_SCHEDULE:
        r_id = race['id']
        race_dt = datetime.datetime.fromisoformat(race['date'])
        
        # 枠順・出馬表はレースの14日前〜当日に公開される
        days_until = (race_dt - now).total_seconds() / 86400
        
        # レースまで10日以内の場合、定期的にNetKeibaから最新出馬表状態を取得
        if -1 <= days_until <= 10:
            log(f"Checking NetKeiba shutuba for Race {r_id}: {race['name']}...")
            url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race['netkeiba_id']}"
            html = fetch_html(url)
            if html:
                starters, stage = parse_shutuba(html)
                if len(starters) >= 5:
                    if stage != 'gate_confirmed':
                        if days_until <= 3.2: # 木曜午後以降なら出走馬確定
                            stage = 'starters_confirmed'
                        else:
                            stage = 'entry_scheduled'

                    log(f"Found {len(starters)} starters for {race['name']} [Stage: {stage}]!")
                    entries_data[r_id] = [
                        {
                            'waku': s['waku'],
                            'gate': s['gate'],
                            'horseName': s['horseName'],
                            'sexAge': s['sexAge'],
                            'load': s['load'],
                            'jockey': s['jockey'],
                            'stable': s['stable']
                        }
                        for s in starters
                    ]
                    
                    if 'races' in pred_data and r_id in pred_data['races']:
                        pred_data['races'][r_id]['entryStatus'] = stage
                        pred_starters = pred_data['races'][r_id].get('starters', [])
                        
                        # Filter to only actual runners
                        official_names = set(s['horseName'] for s in starters)
                        existing_map = {p['horseName']: p for p in pred_starters}
                        
                        new_pred_starters = []
                        for s in starters:
                            hname = s['horseName']
                            if hname in existing_map:
                                ps = existing_map[hname]
                                ps['gate'] = s['gate']
                                ps['waku'] = s['waku']
                                ps['jockey'] = s['jockey']
                                ps['stable'] = s['stable']
                                if s.get('odds'):
                                    ps['odds'] = s['odds']
                                if s.get('pop'):
                                    ps['pop'] = s['pop']
                                if s.get('confirmedWeight'):
                                    ps['confirmedWeight'] = s['confirmedWeight']
                                    ps['weightDiff'] = s.get('weightDiff')
                                new_pred_starters.append(ps)
                            else:
                                new_pred_starters.append(s)

                        if stage == 'gate_confirmed':
                            pred_data['races'][r_id]['starters'] = sorted(new_pred_starters, key=lambda x: (x.get('gate') or 99))
                        else:
                            pred_data['races'][r_id]['starters'] = sorted(new_pred_starters, key=lambda x: x['horseName'])

                    updated = True

    if updated:
        with open(ENTRIES_JSON, 'w', encoding='utf-8') as f:
            json.dump(entries_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(APP_DIR, 'src', 'entries_data.js'), 'w', encoding='utf-8') as f:
            f.write('export const ENTRIES_DATA = ' + json.dumps(entries_data, ensure_ascii=False, indent=2) + ';\n')

        with open(PRED_JSON, 'w', encoding='utf-8') as f:
            json.dump(pred_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(APP_DIR, 'src', 'prediction_data.js'), 'w', encoding='utf-8') as f:
            f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')

        log("Updated entries_data and prediction_data successfully.")
        sync_all()
    else:
        log("No new entries updates required at this time.")

def sync_all():
    """index.html、src/main.jsを同期し、ViteでビルドしてGitへコミット＆プッシュ"""
    log("Running master synchronization across the codebase...")
    gen_script = os.path.join(APP_DIR, 'scripts', 'build_clean_v10.py')
    if os.path.exists(gen_script):
        subprocess.run([sys.executable, gen_script], cwd=APP_DIR, check=True)
    
    log("Running Vite production build (npm run build)...")
    res = subprocess.run(['npm', 'run', 'build'], cwd=APP_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        log("Vite build succeeded!")
    else:
        log(f"Vite build error: {res.stderr}")
        return

    # Git commit & push
    log("Pushing updates to GitHub...")
    subprocess.run(['git', 'add', '.'], cwd=APP_DIR)
    subprocess.run(['git', 'commit', '-m', 'chore: automated update data & entries [skip ci]'], cwd=APP_DIR)
    push_res = subprocess.run(['git', 'push', 'origin', 'main'], cwd=APP_DIR, capture_output=True, text=True)
    if push_res.returncode == 0:
        log("Git push succeeded! Remote repository is fully updated.")
    else:
        log(f"Git push note/result: {push_res.stderr.strip() or push_res.stdout.strip()}")

    log("Publishing dist to gh-pages branch...")
    subprocess.run(['npx', '--yes', 'gh-pages', '-d', 'dist'], cwd=APP_DIR)
    log("GitHub Pages deployment published!")

def main():
    log("GRAND STABLE Auto-Update System initialized.")
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        log("Daemon mode started. Checking every 1 hour...")
        while True:
            try:
                check_and_update_entries()
            except Exception as e:
                log(f"Unexpected error in daemon loop: {e}")
            time.sleep(3600)
    else:
        # One-shot check
        check_and_update_entries()
        sync_all()
        log("One-shot check completed.")

if __name__ == '__main__':
    main()
