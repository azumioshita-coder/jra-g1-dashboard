import urllib.request
import json
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
NK_PADDOCKS_FILE = os.path.join(BASE_DIR, 'scripts', 'data', 'netkeiba_all_paddocks.json')
JRA_PADDOCKS_FILE = os.path.join(BASE_DIR, 'scripts', 'data', 'jra_van_photopaddocks.json')

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("==================================================")
    print("  Applying Verified Official NetKeiba & JRA-VAN Photo Paddocks")
    print("==================================================")

    horse_db = load_json(HORSE_JSON)
    nk_data = load_json(NK_PADDOCKS_FILE)
    jra_data = load_json(JRA_PADDOCKS_FILE)

    print(f"Total horses: {len(horse_db)}")

    enriched_paddocks_count = 0
    clean_photos_count = 0

    for name, h in horse_db.items():
        nk_list = nk_data.get(name, [])
        jra_list = jra_data.get(name, [])

        combined = list(nk_list)
        existing_races = {p["race"] for p in combined}
        for jp in jra_list:
            j_race = jp.get("race", "")
            if j_race not in existing_races:
                combined.append({
                    "race": j_race,
                    "grade": "GI",
                    "fullRace": f"{j_race} GI",
                    "rank": "",
                    "raceDate": "",
                    "shotDate": jp.get("date", ""),
                    "imgUrl": jp.get("photoUrl", ""),
                    "commentator": "JRA-VAN 公式馬体診断",
                    "source": "jra_van"
                })
                existing_races.add(j_race)

        if combined:
            current = combined[0]
            prev = combined[1] if len(combined) > 1 else None

            # Filter good runs: 1着, 2着, 3着 or G1 4着, excluding current and prev
            good_runs = []
            prev_img = prev.get("imgUrl") if prev else None
            curr_img = current.get("imgUrl") if current else None

            for p in combined[1:]:
                img = p.get("imgUrl")
                if img == prev_img or img == curr_img:
                    continue
                rank_str = p.get("rank", "").strip()
                grade_str = p.get("grade", "").strip()
                if re.match(r"^[123]着$", rank_str):
                    good_runs.append(p)
                elif rank_str == "4着" and "GI" in grade_str:
                    good_runs.append(p)

            # Assign 100% verified official photo from latest photo paddock
            h["photoUrl"] = current["imgUrl"]
            h["photoTitle"] = f"{current['fullRace']} ({current['shotDate']})"
            clean_photos_count += 1
            enriched_paddocks_count += 1

            # Store structured paddock info
            h["photoPaddocks"] = combined
            h["paddockStructure"] = {
                "current": current,
                "prev": prev,
                "goodRuns": good_runs,
                "totalCount": len(combined)
            }
        else:
            # Foreign horses or horses without verified official photo paddocks:
            # Set photoUrl to None so it cleanly shows the 'No Photo' placeholder
            # NEVER show random fan photos of other horses or stock photos!
            h["photoUrl"] = None
            h["photoTitle"] = None
            h["photoPaddocks"] = []
            h["paddockStructure"] = {
                "current": None,
                "prev": None,
                "goodRuns": [],
                "totalCount": 0
            }

    # Save to src/horse_data.json and src/horse_data.js
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(horse_db, f, ensure_ascii=False, indent=2)

    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(horse_db, ensure_ascii=False, indent=2) + ";\n")

    print(f"Finished! {enriched_paddocks_count} horses have official photo paddocks & verified photos.")
    print(f"{len(horse_db) - enriched_paddocks_count} horses without paddocks have clean No-Photo states.")

if __name__ == '__main__':
    main()
