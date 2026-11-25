import urllib.request
import urllib.parse
import json
import re
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
ID_MAP_FILE = os.path.join(BASE_DIR, 'scripts', 'data', 'verified_netkeiba_ids.json')
PADDOCKS_FILE = os.path.join(BASE_DIR, 'scripts', 'data', 'jra_van_photopaddocks.json')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_netkeiba_best_photo(hid):
    url = 'https://db.netkeiba.com/photo/api_horse_photo_list.html'
    for period in ['2', '1']:  # 2: popular, 1: recent
        data = urllib.parse.urlencode({
            'input': 'UTF-8',
            'output': 'json',
            'horse_id': hid,
            'limit': '16',
            'page': '1',
            'period': period
        }).encode('ascii')
        req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            res = urllib.request.urlopen(req, timeout=6).read().decode('utf-8', errors='replace')
            parsed = json.loads(res)
            # Find photo link
            links = re.findall(r'<a href=\"([^\"]*show_photo[^\"]*)\"[^>]*title=\"([^\"]*)\"', parsed)
            if links:
                for best_link, title in links:
                    clean_url = best_link.split('&tn=')[0].split('&tmp=')[0]
                    if not clean_url.startswith('http'):
                        clean_url = 'https://cdnv2.netkeiba.com/img.db/' + clean_url.lstrip('/')
                    return clean_url, title
        except Exception:
            pass
    return None, None

def main():
    print("==================================================")
    print("  Enriching Horses with NetKeiba Photos & JRA-VAN Photo Paddocks")
    print("==================================================")

    horse_db = load_json(HORSE_JSON)
    id_map = load_json(ID_MAP_FILE)
    paddocks = load_json(PADDOCKS_FILE)

    print(f"Total horses: {len(horse_db)}")
    print(f"JRA-VAN Photo Paddocks available for {len(paddocks)} horses")

    def worker(name):
        h = horse_db[name]
        hid = id_map.get(name)
        
        # 1. Netkeiba best photo extraction
        if hid and name != 'テアオ':
            best_photo, photo_title = get_netkeiba_best_photo(hid)
            if best_photo:
                h['photoUrl'] = best_photo
                h['photoTitle'] = photo_title
        elif name == 'テアオ':
            h['photoUrl'] = None

        # 2. Attach JRA-VAN Photo Paddocks
        h_paddocks = paddocks.get(name, [])
        h['photoPaddocks'] = h_paddocks

        return name, bool(h.get('photoUrl')), len(h_paddocks)

    all_names = sorted(list(horse_db.keys()))
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(worker, name): name for name in all_names}
        done = 0
        for f in as_completed(futures):
            done += 1
            name, has_p, paddock_cnt = f.result()
            p_str = f"Paddocks: {paddock_cnt}" if paddock_cnt > 0 else "No Paddock"
            print(f"[{done}/{len(all_names)}] {name}: Photo={'YES' if has_p else 'NO'} | {p_str}")
            time.sleep(0.04)

    # Save to src/horse_data.json and src/horse_data.js
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(horse_db, f, ensure_ascii=False, indent=2)

    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(horse_db, ensure_ascii=False, indent=2) + ";\n")

    print(f"\nSuccessfully enriched all {len(horse_db)} horses with verified photos & JRA-VAN paddocks!")

if __name__ == '__main__':
    main()
