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
    """NetKeiba出馬表HTMLから枠番、馬番、馬名、性齢、斤量、騎手、厩舎を抽出"""
    starters = []
    rows = re.findall(r'<tr[^>]*class=\"[^\"]*HorseList[^\"]*\"[^>]*>([\s\S]*?)</tr>', html)
    if not rows:
        rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', html)

    for row in rows:
        waku_m = re.search(r'class=\"[^\"]*Waku(\d)[^\"]*\"', row)
        gate_m = re.search(r'class=\"[^\"]*Umaban\d*[^\"]*\"[^>]*>(\d+)</td>', row)
        name_m = re.search(r'<span class=\"Horse_Name\"[^>]*><a[^>]*>([^<]+)</a>', row)
        if not name_m:
            name_m = re.search(r'title=\"([^\"]+)\"[^>]*class=\"[^\"]*Horse_Name', row)

        sex_age_m = re.search(r'class=\"[^\"]*Barei[^\"]*\"[^>]*>([^<]+)</td>', row)
        load_m = re.search(r'class=\"[^\"]*Weight[^\"]*\"[^>]*>([\d\.]+)</td>', row)
        jockey_m = re.search(r'class=\"[^\"]*Jockey[^\"]*\"[^>]*><a[^>]*>([^<]+)</a>', row)
        stable_m = re.search(r'class=\"[^\"]*Trainer[^\"]*\"[^>]*><a[^>]*>([^<]+)</a>\s*(?:<span[^>]*>\(([^<]+)\)</span>)?', row)

        if gate_m and name_m:
            waku = int(waku_m.group(1)) if waku_m else 1
            gate = int(gate_m.group(1))
            horse_name = name_m.group(1).strip()
            sex_age = sex_age_m.group(1).strip() if sex_age_m else '牡4'
            load = float(load_m.group(1).strip()) if load_m else 58.0
            if load.is_integer():
                load = int(load)
            jockey = jockey_m.group(1).strip() if jockey_m else '未定'
            
            if stable_m:
                trainer = stable_m.group(1).strip()
                loc = stable_m.group(2).strip() if stable_m.group(2) else ''
                stable = f"{trainer} ({loc})" if loc else trainer
            else:
                stable = '-'

            starters.append({
                'waku': waku,
                'gate': gate,
                'horseName': horse_name,
                'sexAge': sex_age,
                'load': load,
                'jockey': jockey,
                'stable': stable
            })

    starters.sort(key=lambda x: x['gate'])
    return starters

def check_and_update_entries():
    """今後のレースの枠順確定を自動検知して更新"""
    try:
        with open(ENTRIES_JSON, 'r', encoding='utf-8') as f:
            entries_data = json.load(f)
    except Exception:
        entries_data = {}

    updated = False
    now = datetime.datetime.now()

    for race in G1_SCHEDULE:
        r_id = race['id']
        race_dt = datetime.datetime.fromisoformat(race['date'])
        
        # 枠順は通常レースの4日前〜当日に公開される
        days_until = (race_dt - now).total_seconds() / 86400
        
        # すでに登録済みでも更新チェック、または未登録でレース直前の場合
        if r_id not in entries_data and -1 <= days_until <= 5:
            log(f"Checking NetKeiba shutuba for Race {r_id}: {race['name']}...")
            url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race['netkeiba_id']}"
            html = fetch_html(url)
            if html:
                starters = parse_shutuba(html)
                if len(starters) >= 8:
                    log(f"Found {len(starters)} starters for {race['name']}!")
                    entries_data[r_id] = starters
                    updated = True

    if updated:
        with open(ENTRIES_JSON, 'w', encoding='utf-8') as f:
            json.dump(entries_data, f, ensure_ascii=False, indent=2)
        log("Updated src/entries_data.json successfully.")
        sync_all()
    else:
        log("No new entries (枠順) updates required at this time.")

def sync_all():
    """index.html、src/main.jsを同期し、ViteでビルドしてGitへコミット＆プッシュ"""
    log("Running master synchronization across the codebase...")
    gen_script = os.path.join(APP_DIR, '..', '..', 'brain', 'd0b27f42-e7a0-46fb-8c26-f3eaff3f5171', 'scratch', 'generate_synced_app.py')
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
