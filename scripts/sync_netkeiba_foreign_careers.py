import json
import os
import re
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORSE_JSON = os.path.join(BASE_DIR, 'src', 'horse_data.json')
HORSE_JS = os.path.join(BASE_DIR, 'src', 'horse_data.js')
PRED_JSON = os.path.join(BASE_DIR, 'src', 'prediction_data.json')
PRED_JS = os.path.join(BASE_DIR, 'src', 'prediction_data.js')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

TARGET_HORSES = {
    'オンブズマン': '2021190002',
    'カランダガン': '2021190001',
    'ゴリアット': '2020190005',
    'エシカルダイヤモンド': '2020190008',
    'テアオ': '2022190003',
    'ミニーホーク': '2022190002',
    'エルデナリ': '2023190001',
    'オーギュストロダン': '2020190003',
    'ファンタスティックムーン': '2020190004',
    'チャリン': '2020190002',
}

def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='replace')

def parse_profile(hid):
    url = f'https://db.netkeiba.com/horse/{hid}/'
    html = fetch_html(url)
    prof = {}
    for m in re.finditer(r'<th>(.*?)</th>\s*<td>(.*?)</td>', html, re.DOTALL):
        th = re.sub(r'<.*?>', '', m.group(1)).strip()
        td = re.sub(r'<.*?>', '', m.group(2)).strip()
        prof[th] = td
    
    # parse titles from 主な勝鞍
    raw_titles = prof.get('主な勝鞍', '')
    titles = []
    if raw_titles and raw_titles != '-':
        for t in re.split(r'[,、\n]', raw_titles):
            t_clean = t.strip()
            if t_clean:
                titles.append(t_clean)

    return {
        'birthday': prof.get('生年月日', ''),
        'stable': prof.get('調教師', ''),
        'owner': prof.get('馬主', ''),
        'breeder': prof.get('生産者', ''),
        'origin': prof.get('産地', ''),
        'record': prof.get('通算成績', ''),
        'earnings': prof.get('獲得賞金 (中央)', '0万円') if prof.get('獲得賞金 (中央)') else '0万円',
        'titles': titles
    }

def parse_career(hid):
    url = f'https://db.netkeiba.com/horse/result/{hid}/'
    html = fetch_html(url)
    table = re.search(r'<table[^>]*class=\"[^\"]*db_h_race_results[^\"]*\"[^>]*>(.*?)</table>', html, re.DOTALL)
    if not table:
        return []
    
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table.group(1), re.DOTALL)
    career = []
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
    return career

def run_sync():
    with open(HORSE_JSON, 'r', encoding='utf-8') as f:
        hd = json.load(f)

    with open(PRED_JSON, 'r', encoding='utf-8') as f:
        pd = json.load(f)

    for name, hid in TARGET_HORSES.items():
        print(f"Syncing {name} ({hid}) from Netkeiba...")
        prof = parse_profile(hid)
        career = parse_career(hid)
        
        if name not in hd:
            hd[name] = {"name": name}
        
        h = hd[name]
        h['netkeiba_id'] = hid
        if prof['birthday']:
            h['birthday'] = prof['birthday']
        if prof['stable']:
            h['stable'] = prof['stable']
        # If owner / breeder is empty, store "" or "-" so no fake placeholder is rendered
        h['owner'] = prof['owner'] if prof['owner'] else '-'
        h['breeder'] = prof['breeder'] if prof['breeder'] else '-'
        h['origin'] = prof['origin'] if prof['origin'] else ''
        if prof['record']:
            h['record'] = prof['record']
        h['earnings'] = prof['earnings']
        if prof['titles']:
            h['titles'] = prof['titles']
        
        if career:
            h['career'] = career
            print(f"  -> Successfully imported {len(career)} races directly from Netkeiba.")
            print(f"  -> Latest race: {career[0]['date']} {career[0]['race']} {career[0]['rank']}着")
        else:
            print(f"  -> Warning: No career races found for {name}")

        # Ensure photoUrl is None if no real photo exists, avoiding any mock stock photo
        if h.get('photoUrl') and 'unsplash' in h['photoUrl']:
            h['photoUrl'] = None

    # Write back horse_data.json and horse_data.js
    with open(HORSE_JSON, 'w', encoding='utf-8') as f:
        json.dump(hd, f, ensure_ascii=False, indent=2)

    with open(HORSE_JS, 'w', encoding='utf-8') as f:
        f.write("export const HORSE_DATABASE = " + json.dumps(hd, ensure_ascii=False, indent=2) + ";\n")

    print("\nUpdated horse_data.json & horse_data.js successfully.")

    # Now update starters and rankings in prediction_data.json
    starters_r19 = pd.get('races', {}).get('19', {}).get('starters', [])
    for s in starters_r19:
        hname = s.get('horseName')
        if hname in TARGET_HORSES and hname in hd and hd[hname].get('career'):
            latest = hd[hname]['career'][0]
            # format e.g. "英チャンピオンS(G1) 1着"
            r_name = latest['race'].replace('GI', 'G1').replace('GII', 'G2').replace('GIII', 'G3')
            s['lastRace'] = f"{r_name} {latest['rank']}着"
            print(f"Updated starter lastRace for {hname}: {s['lastRace']}")

    # Update contender ranking comments and marks
    foreign_analysis = {
        'オンブズマン': {
            'comment': '前走アスコットの英チャンピオンS(G1)でカランダガンを撃破して圧勝した欧州最強中距離馬。名門ゴスデン厩舎の看板を背負い、主戦W.ビュイック騎手の手綱でジャパンカップ頂点を狙う。',
            'strengths': '前走英チャンピオンS(G1)圧勝、通算13戦9勝[9-3-0-1]。瞬発力と高速持続力を兼備。'
        },
        'カランダガン': {
            'comment': '前走英チャンピオンS(G1)2着。昨年のジャパンカップを衝撃的な末脚で制したディフェンディングチャンピオン。府中の芝2400mに対する適性は最高峰。',
            'strengths': '昨年のジャパンカップ覇者、通算19戦10勝[10-7-1-1]。東京コースの直線での爆発的末脚は実証済み。'
        },
        'ゴリアット': {
            'comment': '前走独オイロパ賞(G1)快勝、昨年のキングジョージ(G1)覇者。強烈な先行力と底知れぬスタミナを武器に、スミヨン騎手とともに世界を制圧しにかかる。',
            'strengths': '前走オイロパ賞(G1)1着、キングジョージ覇者。通算23戦10勝[10-4-2-7]。'
        },
        'テアオ': {
            'comment': '前走ペルーのラテンアメリカ大賞(G1)を快勝、チリのエルダービー(G1)など南米G1を席巻したチリ最強馬。L.トーレス騎手とともに未知のスピードとスタミナで挑む。',
            'strengths': '前走ラテンアメリカ大賞(G1)1着、通算9戦6勝[6-2-1-0]。南米G1複数制覇の圧倒的能力。'
        },
        'ミニーホーク': {
            'comment': '前走英チャンピオンズF&M(G1)を制覇、英オークス馬。A.オブライエン調教師×R.ムーア騎手の世界的黄金コンビが送り込む最強牝馬。',
            'strengths': '前走英チャンピオンズF&M(G1)1着、通算15戦7勝[7-3-1-4]。英オークス制覇の長距離適性と瞬発力。'
        },
        'エシカルダイヤモンド': {
            'comment': '前走BCターフ(G1)に参戦した愛国のスタミナ自慢。W.マリンズ厩舎が送り込み、日本の名手・坂井瑠星騎手とのコンビで波乱を狙う。',
            'strengths': '通算14戦5勝[5-2-0-7]、前走BCターフ出走。長距離G1でのタフな追撃力。'
        }
    }

    for root_dict in [pd.get('races', {}).get('19', {}), pd]:
        for cr in root_dict.get('contenderRanking', []):
            name = cr.get('horseName')
            if name in foreign_analysis:
                cr['comment'] = foreign_analysis[name]['comment']
                cr['strengths'] = foreign_analysis[name]['strengths']

    with open(PRED_JSON, 'w', encoding='utf-8') as f:
        json.dump(pd, f, ensure_ascii=False, indent=2)

    with open(PRED_JS, 'w', encoding='utf-8') as f:
        f.write("export const PREDICTION_DATA = " + json.dumps(pd, ensure_ascii=False, indent=2) + ";\n")

    print("Updated prediction_data.json & prediction_data.js successfully.")

if __name__ == '__main__':
    run_sync()
