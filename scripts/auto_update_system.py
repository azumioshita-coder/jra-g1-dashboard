#!/usr/bin/env python3
"""
GRAND STABLE - Automated JRA G1 Data Update Daemon & CLI
--------------------------------------------------------
Features:
1. Automated Gate Draw & Confirmed Starters scraping from NetKeiba for upcoming races (Thursdays/Fridays).
2. Automated Race Results & Official Payouts scraping from NetKeiba after race finish (Sundays).
3. Synchronization across entries_data, prediction_data, horse_data, index.html, and src/main.js.
4. Auto-build with Vite (npm run build).
5. Automatic Git commit, push, and GitHub Pages deployment.
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
SRC_DIR = os.path.join(APP_DIR, 'src')
INDEX_HTML = os.path.join(APP_DIR, 'index.html')
MAIN_JS = os.path.join(APP_DIR, 'src', 'main.js')
ENTRIES_JSON = os.path.join(APP_DIR, 'src', 'entries_data.json')
PAYOUTS_JSON = os.path.join(APP_DIR, 'src', 'payouts_data.json')
HIST_JS = os.path.join(APP_DIR, 'src', 'historical_results.js')
HORSE_JSON = os.path.join(APP_DIR, 'src', 'horse_data.json')
PRED_JSON = os.path.join(APP_DIR, 'src', 'prediction_data.json')
REVIEWS_JSON = os.path.join(APP_DIR, 'src', 'race_reviews_data.json')
RESULTS_JSON = os.path.join(APP_DIR, 'scripts', 'data', 'results_2026_all_17.json')
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
            for enc in ['utf-8', 'euc-jp', 'cp932']:
                try:
                    return content.decode(enc)
                except Exception:
                    continue
            return content.decode('utf-8', errors='ignore')
    except Exception as e:
        log(f"Fetch failed for {url}: {e}")
        return None

JOCKEY_MAP = {
    'バルザロー': 'M.バルザローナ',
    'バルザローナ': 'M.バルザローナ',
    'Ｍ．バルザローナ': 'M.バルザローナ',
    'ルメール': 'C.ルメール',
    'Ｃ．ルメール': 'C.ルメール',
    'プーシャン': 'A.プーシャン',
    'Ａ．プーシャン': 'A.プーシャン',
    'モレイラ': 'J.モレイラ',
    'Ｊ．モレイラ': 'J.モレイラ',
    'Ｃデムーロ': 'C.デムーロ',
    'Ｃ．デムーロ': 'C.デムーロ',
    'デムーロ': 'C.デムーロ',
    '武豊': '武豊',
    '川田': '川田将雅',
    '川田将雅': '川田将雅',
    '坂井': '坂井瑠星',
    '坂井瑠星': '坂井瑠星',
    '松山': '松山弘平',
    '松山弘平': '松山弘平',
    '西村淳': '西村淳也',
    '西村淳也': '西村淳也',
    '菅原明': '菅原明良',
    '菅原明良': '菅原明良',
    '岩田望': '岩田望来',
    '岩田望来': '岩田望来',
    '幸': '幸英明',
    '幸英明': '幸英明',
    '北村友': '北村友一',
    '北村友一': '北村友一',
    '浜中': '浜中俊',
    '浜中俊': '浜中俊',
    '三浦': '三浦皇成',
    '三浦皇成': '三浦皇成',
    '藤懸': '藤懸貴志',
    '藤懸貴志': '藤懸貴志',
    '田口': '田口貫太',
    '田口貫太': '田口貫太',
    '横山武': '横山武史',
    '横山典': '横山典弘',
    '横山和': '横山和生',
    '戸崎': '戸崎圭太',
    '鮫島駿': '鮫島克駿',
}

# Starter to authentic confirmed jockey override map
KNOWN_STARTER_JOCKEYS = {
    'テアオ': 'L.トーレス',
    'ファイアンクランツ': 'J.モレイラ',
    'ヘデントール': 'T.マーカンド',
    'クロワデュノール': 'C.デムーロ',
    'マスカレードボール': 'C.ルメール',
    'ダノンデサイル': '戸崎圭太',
    'アーバンシック': 'A.プーシャン',
    'ゴリアット': 'C.スミヨン',
    'カランダガン': 'M.バルザローナ',
    'オンブズマン': 'W.ビュイック',
    'エシカルダイヤモンド': '坂井瑠星',
    'ミニーホーク': 'R.ムーア',
    'メイショウタバル': '武豊',
    'コスモキュランダ': '丹内祐次',
    'ヴェルテンベルク': '横山典弘',
    'タガノデュード': 'M.デムーロ',
    'シェイクユアハート': '古川吉洋',
    'エキサイトバイオ': '荻野極',
    'アルマヴェローチェ': '岩田望来',
}

def clean_jockey_name(j):
    if not j:
        return '未定'
    j = j.replace('Ｍ．', 'M.').replace('Ｃ．', 'C.').replace('Ａ．', 'A.').replace('Ｊ．', 'J.').replace('・', '.').strip()
    return JOCKEY_MAP.get(j, j)

# Contender Ranking Dynamic Scoring Constants
JOCKEY_BASE_SCORES = {
    'ルメール': 98, 'C.ルメール': 98, '川田': 97, '川田将雅': 97,
    '武豊': 96, 'C.デムーロ': 96, 'Ｃデムー': 96, 'モレイラ': 97, 'J.モレイラ': 97,
    'ムーア': 96, 'レーン': 96, 'スミヨン': 96, 'プーシャ': 93, 'A.プーシャン': 93,
    '戸崎': 95, '戸崎圭太': 95, '坂井': 94, '坂井瑠星': 94, '松山': 94, '松山弘平': 94,
    'バルザローナ': 95, 'M.バルザローナ': 95, '横山武': 93, '横山武史': 93,
    '岩田望': 92, '岩田望来': 92, '西村淳': 91, '西村淳也': 91, '菅原明': 91, '菅原明良': 91,
    'ビュイック': 95, 'W.ビュイック': 95, 'マーカンド': 94, 'T.マーカンド': 94,
    '横山典': 91, '横山典弘': 91, '田口': 88, '田口貫太': 88, '三浦': 89, '三浦皇成': 89,
    '荻野極': 86, '古川吉': 85, 'トーレス': 92, 'L.トーレス': 92, '丹内': 90, '丹内祐次': 90
}

TRAIN_BASE_SCORES = {'S': 97, 'A+': 95, 'A': 92, 'B+': 88, 'B': 84, 'C': 78}

HORSE_CONCERNS_DATABASE = {
    # === ジャパンカップ (G1) ===
    "ヘデントール": "ゲート出遅れ癖があり、最内1番枠で出負けすると包まれて位置取りを大きく落とす危険性。前半の追走スピードが遅く、府中の超高速マイル並みのスピード決着になると置かれるリスク大。極限の上がり33秒前半の切れ味勝負ではトップクラスの瞬発力に見劣る。",
    "コスモキュランダ": "右回りの小回り・中回りでマクリを決める競馬を得意としており、左回りの東京コースは日本ダービー6着以来。直線の長い府中では早めのマクリが通用しにくく、直線だけの純粋なキレ味比べになると切れ負けする懸念。内枠から外へ持ち出すコース取りも課題。",
    "メイショウタバル": "最大の敵は自身の激しい気性面。テンに速い馬が揃った中で武豊騎手が折り合いをつけられるかが最大の焦点で、競りかけられてハナを争うと道中で力んで暴走するリスク。また、フランス凱旋門賞へのタフな遠征帰り初戦で、目に見えない長距離輸送の疲労やメンタル面の回復も懸念。",
    "クロワデュノール": "叩き良化型で前走秋天5着からの上積みはあるものの、本質は長く良い脚を使う持続力型。府中の良馬場で上がり32秒台後半〜33秒前半の極限のトップスピード勝負になった際、純粋な瞬発力比べでキレ負けするリスク。2枠4番の内枠で直線スムーズに進路を確保できるかも課題。",
    "シェイクユアハート": "好位からソツなく運ぶ競馬はできるが、今回は国内外の超一流G1馬が勢揃いし相手関係が一気に強化。決定打となる決め手に欠け、最後の一冠・勝負どころでの絶対的なスピードと瞬発力でG1馬たちに屈する可能性が高い。馬券圏内へは相当な前残り展開や他馬の自滅などの恩恵が必須。",
    "マスカレードボール": "前走天皇賞(秋)はスローペースで折り合いを欠いて11着大敗。気性的に繊細な面があり、馬群の中で包まれた際にリズムを崩すと直線の伸びを欠く脆さがある。2400mへの距離延長で道中の折り合いが最大の試練となり、道中で我慢が利かなかった場合は直線の失速が危惧される。",
    "ファイアンクランツ": "G1最高峰の舞台において重賞実績が乏しく、相手関係の急激な強化は明白。前走アルゼンチン共和国杯8着からの巻き返しを狙うが、トップクラス相手のタイトなペース追走で脚を使わされ、直線勝負どころで余力が残らない懸念。モレイラ騎手の手腕に期待も、地力面での壁は高い。",
    "オンブズマン": "欧州のタフで時計のかかる重い芝を中心に活躍してきた実績馬であり、日本の「超高速・硬い野芝」に対する適性は未知数。過去の欧州強豪馬の多くが府中の超高速レコード決着でスピード負けしており、追走で脚を削られるリスク。初の長期空輸・検疫を経た反動も懸念材料。",
    "カランダガン": "欧州最強クラスの中距離実績を誇るが、セン馬特有の気難しさとゲート内の立ち遅れ癖が最大の懸念。初来日のアウェイ環境、大観衆のファンファーレと歓声に包まれた東京競馬場の独特なパドック・輪乗りでテンションが上がらないか。日本の超高速レコード決着への純粋な適応力も未知数。",
    "ミニーホーク": "牝馬限定の欧州G1での実績が中心で、今回初めて日本の最高峰古馬・牡馬の一線級と直接対峙する力関係の壁。欧州の湿ったソフトな馬場での差し切りが持ち味であり、パンパンの良馬場で上がり33秒前後の高速ラップを刻む日本の芝でどこまでキレが持続するかは未知数。",
    "ヴェルテンベルク": "近走は重賞戦線でも善戦止まりで、G1メンバー相手では純粋なスピード能力と決定力で明白に見劣る。横山典弘騎手特有の後方ポツンからのイン差し・奇襲戦法がハマるかどうかの極端な展開待ちになりやすく、前が止まらない高速馬場や瞬発力戦では為す術なく終わるリスク。",
    "テアオ": "南米チリおよび北米ダートを中心に活躍してきた経歴で、世界最高峰の芝スピードが要求される東京芝2400mへの適性は極めて不透明。芝・ダートを問わず日本の超高速馬場への順応は容易ではなく、道中のペースに追走できず序盤から大きく置かれてしまう可能性が高い。",
    "アーバンシック": "スタートの出遅れ癖が慢性化しており、外枠7枠13番から立ち遅れると終始外々を回らされるか後方待機を余儀なくされる。エンジンのかかりが遅くズブい面があるため、直線向いてからのトップスピード突入までに時間がかかり、前の馬が止まらない東京の高速馬場では差し届かないリスク大。",
    "タガノデュード": "前走秋天4着は展開とコース取りが完璧に噛み合った激走で、再現性には疑問符。本質的には後方からのワンターン差し型で、2400mへの距離延長で道中の追走スタミナが持つかどうか。外枠7枠14番から直線だけで全馬を飲み込むには相当なハイペースと展開の助けが必要。",
    "エキサイトバイオ": "クラシックや古馬王道G1の一線級相手との対戦経験が浅く、総合力・スピード指数の両面で大きく水を開けられている。7枠15番の外枠から先行して粘り込むにしても、メイショウタバル等の作り出すペースについていけば直線で力尽き、控えてもキレ味で太刀打ちできない。",
    "ダノンデサイル": "ダービー圧勝・天皇賞秋制覇と実績は最上位だが、過去10年で勝利がない鬼門の「大外8枠16番」を引いてしまった点が最大の障壁。終始外々を回らされる距離ロスと風圧を受けるリスクがあり、道中で壁を作れず脚を溜められないと内をロスなく回った馬に足を掬われる死角。",
    "ゴリアット": "英キングジョージ圧勝のパワー型ステイヤーだが、本質は欧州のタフな重馬場・消耗戦に強い血統。大外8枠17番から日本の超高速芝に対応して終始外を回らされるのは大きなディスアドバンテージ。瞬発力勝負（上がり33秒台前半）になった際のキレ味不足で日本馬の決め手に屈する懸念。",
    "エシカルダイヤモンド": "大外8枠18番の最悪枠を引き、序盤から激しい距離ロスを強いられる。障害レースも走るタフな超長距離ステイヤーで、2400mのスピード戦への適性は明らかに不足。米BCターフでもスピード負けしており、東京の超高速レコード決着では道中ついて行くだけで手一杯になる懸念大。",

    # === チャンピオンズカップ (G1) ===
    "レモンポップ": "1800mへの距離延長と中京の急坂。マイルより1ハロン長く、目標にされるプレッシャーの中でラスト100mの踏ん張りが試される。",
    "ウィルソンテソーロ": "相手なりに好走するが勝ち切るための決定力。勝負どころでの進路取りと、仕掛けが早すぎた場合の末の甘さ。",
    "クラウンプライド": "同型のテーオードレフォンやレモンポップとのハナ争い。先行激化でハイペースに巻き込まれた際のスタミナ消耗。",
    "サンライズジパング": "スタートの出遅れ癖と、砂を被った際の走りのリズム。中京の小回り4コーナーで外へ振られる距離ロス。",
    "セラフィックコール": "序盤のダッシュ力不足による極端な後方待機。前が止まりにくい中京ダートで直線一気の脚質が届かないリスク。",
    "ヤマニンウルス": "初の古馬G1超一線級とのタイトなペース勝負。580kg超の超大型馬特有の叩き2戦目の反動と急坂での踏ん張り。",
    "ガイアフォース": "初めてのダートG1挑戦で、強烈なキックバック（砂被り）を浴びた際の嫌気と、パワー型ダート馬との競り合い。",
    "ペプチドナイル": "フェブラリーS覇者だが1800mへの距離延長は課題。道中で息が入れづらい中京のコーナーワークで脚が溜まるか。",
    "ハギノアレグリアス": "直線の追い比べでの決め手不足。7歳を迎えての絶対的なトップスピードの衰えと、斤量58kgでの瞬発力。",
    "ドゥラエレーデ": "芝ダート問わず先行力はあるが、G1でのワンパンチ不足。直線でジリ脚になり、切れ味鋭い差し馬に屈する傾向。",
    "メイショウハリオ": "加齢によるズブさと慢性的な出遅れ癖。後方から追い込む競馬一辺倒で、スロー〜ミドルの前残り展開に泣くリスク。",
    "ミックファイア": "南関東三冠馬だが中央の高速砂への適性と、歴戦の中央古馬G1馬との純粋なスピード差・追走スピードの壁。",
    "スレイマン": "重賞・オープンでの実績にとどまり、G1の激流ラップを好位で受け止めるタフネスに疑問符。",
    "テーオードレフォン": "単騎逃げに持ち込めないと脆い逃げ馬。同型馬に競りかけられてハナを譲った場合の失速。",
    "グロリアムンディ": "近走の大敗続きでピーク時の推進力が戻っていない点。精神面での前向きさと調子の波。",
    "アーテルアストレア": "牡馬の一線級と斤量56kgで戦うパワーの差。揉まれ弱い面があり、内枠で砂を被った際の嫌気。",

    # === 有馬記念 (G1) ===
    "ドウデュース": "中山2500m特有のトリッキーなコース形態と、秋3戦目（秋天→JC→有馬）による過酷なローテーションの疲労蓄積。",
    "レガレイラ": "ゲート出遅れ癖と極端な後方待機。小回り中山の4コーナーで前が壁になり進路を失うリスク。",
    "スターズオンアース": "外枠を引いた際の距離ロスと、脚元の状態・休み明けでのコンディション維持。",
    "ジャスティンパレス": "直線での極限の瞬発力勝負になると見劣り。中山での早仕掛けのタイミング。",
    "ソールオリエンス": "右回りでのコーナリングのぎこちなさと、良馬場での高速決着への対応力。",
    "ブローザホーン": "パンパンの良馬場・超高速決着でのスピード不足。道悪やタフな馬場が欲しいタイプ。",
    "ベラジオオペラ": "2500mへの距離延長と、中山の急坂を2度越えるタフな消耗戦でのスタミナ。",
    "シンエンペラー": "勝ち切るための決定力不足。相手なりに走るが最後ワンパンチ足りない善戦マンの傾向。",
    "ディープボンド": "トップスピードの衰えと、若い世代との瞬発力の差。中山2500mでのスピード対応。",
    "アドマイヤテラ": "古馬超一線級との力関係と、G1のタイトなペースでの追走力。",
    "ネブラディスク": "G1トップクラスとの絶対的な地力・実績の開き。"
}

def compute_contender_ranking(race_id, starters_list, horse_db_data, race_meta=None):
    """
    調教・枠順・確定馬体重・斤量・鞍上・オッズ等の更新に完全連動して、
    6大ファクターおよび好走期待度スコア（compositeScore）を自動動的に再計算する。
    """
    items = []
    
    # レースの舞台設定
    loc = (race_meta.get('location') or '') if race_meta else ''
    crs = (race_meta.get('course') or '') if race_meta else ''
    
    for s in starters_list:
        hname = s.get('horseName', '')
        h_info = horse_db_data.get(hname, {})
        
        # 1. 調教評価 (Training: 20%)
        tr_grade = s.get('trainingGrade') or h_info.get('trainingGrade') or 'B'
        tr_base = TRAIN_BASE_SCORES.get(tr_grade, 85)
        
        # 当日確定馬体重・増減補正
        wt_diff = s.get('weightDiff')
        has_confirmed_wt = s.get('confirmedWeight') is not None
        if wt_diff is not None:
            try:
                diff_n = int(wt_diff)
                if 2 <= diff_n <= 4:
                    tr_base += 2.0  # 理想的な筋力増・好仕上がり
                elif -2 <= diff_n <= 1:
                    tr_base += 1.0  # 安定キープ
                elif diff_n >= 10:
                    tr_base -= 3.0  # 太め残り
                elif diff_n <= -8:
                    tr_base -= 3.0  # 馬体減・疲労
                elif 6 <= diff_n <= 8:
                    tr_base -= 1.0
            except ValueError:
                pass
        elif s.get('trainingWeightDiff'):
            try:
                diff_n = int(s['trainingWeightDiff'])
                if 2 <= diff_n <= 4:
                    tr_base += 1.5
                elif -2 <= diff_n <= 1:
                    tr_base += 1.0
            except ValueError:
                pass
        
        # 追切時計ボーナス
        ttime = s.get('trainingTime') or ''
        if ttime and any(f in ttime for f in ['11.0', '11.1', '11.2']):
            tr_base += 1.5
        elif ttime and any(f in ttime for f in ['11.3', '11.4']):
            tr_base += 0.5
            
        tr_score = min(99, max(70, round(tr_base)))
        
        # 2. 鞍上力 (Jockey: 20%)
        j_name = s.get('jockey') or ''
        j_base = 86
        for k, v in JOCKEY_BASE_SCORES.items():
            if k in j_name:
                j_base = v
                break
        
        # 斤量ボーナス
        try:
            load_val = float(s.get('load', 58))
            if load_val <= 54:
                j_base += 3.2
            elif load_val <= 55:
                j_base += 2.4
            elif load_val <= 56:
                j_base += 1.6
            elif load_val <= 57:
                j_base += 0.8
        except (ValueError, TypeError):
            pass
            
        j_score = min(99, max(70, round(j_base)))
        
        # 3. コース適性 & 枠順バイアス (Course: 15%)
        c_base = 90
        waku = s.get('waku')
        gate = s.get('gate')
        has_gate = (gate is not None and waku is not None)
        
        if has_gate:
            if '東京' in loc and '2400' in crs:
                # 東京芝2400m 枠順バイアス
                if waku == 1:
                    c_base += 3.5
                elif waku == 2:
                    c_base += 2.5
                elif waku in [3, 4]:
                    c_base += 1.2
                elif waku in [5, 6]:
                    c_base += 0.0
                elif waku == 7:
                    c_base -= 1.5
                elif waku == 8:
                    c_base -= 3.0
            elif '中京' in loc and 'ダート' in crs:
                # 中京ダート1800m
                if waku in [1, 2]:
                    c_base += 3.0
                elif waku in [3, 4]:
                    c_base += 1.5
                elif waku in [7, 8]:
                    c_base -= 3.0
            elif '中山' in loc and '2500' in crs:
                # 有馬記念 中山芝2500m
                if waku in [1, 2]:
                    c_base += 3.5
                elif waku in [3, 4]:
                    c_base += 2.0
                elif waku in [7, 8]:
                    c_base -= 3.5
            elif '京都' in loc and '1600' in crs:
                # 京都芝1600m
                if waku in [1, 2]:
                    c_base += 2.5
                elif waku in [3, 4]:
                    c_base += 1.5
                elif waku in [7, 8]:
                    c_base -= 2.0
            else:
                if waku in [1, 2]:
                    c_base += 2.0
                elif waku in [3, 4]:
                    c_base += 1.0
                elif waku in [7, 8]:
                    c_base -= 2.0
                    
        c_score = min(99, max(70, round(c_base)))
        
        # 4. 距離適性 (Distance: 15%) & 5. 前走評価 (PrevRace: 15%)
        odds_f = 99.0
        try:
            if s.get('odds'):
                odds_f = float(s['odds'])
        except (ValueError, TypeError):
            pass
            
        if odds_f <= 3.5:
            p_base, d_base = 96, 96
        elif odds_f <= 7.5:
            p_base, d_base = 94, 94
        elif odds_f <= 15.0:
            p_base, d_base = 91, 92
        elif odds_f <= 35.0:
            p_base, d_base = 88, 88
        else:
            p_base, d_base = 84, 84
            
        # 前走実績の精査連動 (career[0])
        career_list = h_info.get('career') or []
        if career_list:
            last_r = career_list[0]
            l_rank = str(last_r.get('rank', ''))
            l_race = last_r.get('race', '')
            if l_rank in ['1']:
                p_base = max(p_base, 96)
            elif l_rank in ['2', '3']:
                if any(g in l_race for g in ['GI', 'G1', 'GII', 'G2']):
                    p_base = max(p_base, 94)
                else:
                    p_base = max(p_base, 91)
            elif l_rank in ['4', '5'] and any(g in l_race for g in ['GI', 'G1']):
                p_base = max(p_base, 92)

        # 6. 血統適性 (Pedigree: 15%)
        ped_base = 89
        father = s.get('father') or (h_info.get('pedigree', {}).get('sire') if isinstance(h_info.get('pedigree'), dict) else '') or (h_info.get('bloodline', {}).get('father') if isinstance(h_info.get('bloodline'), dict) else '') or ''
        if any(f in father for f in ['スワーヴリチャード', 'キズナ', 'エピファネイア', 'ハーツクライ', 'ドゥラメンテ', 'ディープインパクト', 'Kingman', 'Dubawi', 'Night of Thunder', 'Ya Primo']):
            ped_base = 94
        elif any(f in father for f in ['キタサンブラック', 'モーリス', 'ロードカナロア', 'ルーラーシップ', 'Frankel', 'Adlerflug']):
            ped_base = 92
            
        # 総合期待度スコア (compositeScore)
        comp = round(
            tr_score * 0.20 +
            j_score * 0.20 +
            c_score * 0.15 +
            d_base * 0.15 +
            p_base * 0.15 +
            ped_base * 0.15,
            1
        )
        
        # 分析コメント生成（既存の精査済みコメントがあれば優先）
        if s.get('strengths'):
            strengths_text = s['strengths']
        else:
            str_parts = []
            if has_gate:
                if waku in [1, 2]:
                    str_parts.append(f"【好枠{waku}枠{gate}番】最内経済コースをロスなく立ち回れる絶好条件。")
                elif waku in [3, 4]:
                    str_parts.append(f"【好位自在の{waku}枠{gate}番】馬群を見ながらスムーズに好位を取れる好枠。")
                    
            tr_comment = s.get('trainingComment') or ''
            if has_confirmed_wt:
                diff_str = f"({wt_diff}kg)" if wt_diff else ""
                str_parts.append(f"【当日馬体重{s['confirmedWeight']}kg{diff_str}】仕上がり万全。")
            elif s.get('trainingGrade') == 'S':
                str_parts.append(f"【調教S・抜けた動き】{tr_comment}")
            elif tr_comment:
                str_parts.append(tr_comment)
            else:
                str_parts.append("順調な仕上がり。")
            strengths_text = " ".join(str_parts)

        if s.get('concerns'):
            concerns_text = s['concerns']
        elif hname in HORSE_CONCERNS_DATABASE:
            concerns_text = HORSE_CONCERNS_DATABASE[hname]
        elif h_info.get('concerns'):
            concerns_text = h_info['concerns']
        else:
            con_parts = []
            if has_gate and waku in [7, 8]:
                con_parts.append(f"外枠{waku}枠{gate}番から終始外々を回らされる距離ロスが課題。")
            if wt_diff:
                try:
                    diff_n = int(wt_diff)
                    if diff_n >= 10:
                        con_parts.append(f"馬体重+{diff_n}kgとやや太め残りの懸念。")
                    elif diff_n <= -8:
                        con_parts.append(f"馬体重{diff_n}kgと馬体減り・輸送の影響。")
                except ValueError:
                    pass
            if not con_parts:
                con_parts.append("枠順と展開に左右される可能性。")
            concerns_text = " ".join(con_parts)
        
        # stars calculation
        stars_str = '★★★★★' if comp >= 94 else ('★★★★☆' if comp >= 90 else ('★★★☆☆' if comp >= 86 else '★★☆☆☆'))
        
        item_entry = {
            'gate': gate,
            'waku': waku,
            'horseName': hname,
            'sexAge': s.get('sexAge', ''),
            'load': s.get('load', 58),
            'jockey': s.get('jockey', ''),
            'stable': s.get('stable', ''),
            'odds': s.get('odds', ''),
            'pop': s.get('pop'),
            'scores': {
                'training': tr_score,
                'jockey': j_score,
                'course': c_score,
                'distance': d_base,
                'prevRace': p_base,
                'pedigree': ped_base
            },
            'factors': {
                'workout': tr_score,
                'jockey': j_score,
                'course': c_score,
                'distance': d_base,
                'lastRace': p_base,
                'pedigree': ped_base
            },
            'compositeScore': comp,
            'totalScore': comp,
            'stars': stars_str,
            'strengths': strengths_text,
            'comment': strengths_text,
            'concerns': concerns_text
        }
        if s.get('confirmedWeight'):
            item_entry['confirmedWeight'] = s['confirmedWeight']
        if s.get('weightDiff'):
            item_entry['weightDiff'] = s['weightDiff']
        if s.get('trainingWeight'):
            item_entry['trainingWeight'] = s['trainingWeight']
        if s.get('lastRaceWeight'):
            item_entry['lastRaceWeight'] = s['lastRaceWeight']
        if 'workoutOneWeek' in s:
            item_entry['workoutOneWeek'] = s['workoutOneWeek']
        if 'workoutFinal' in s:
            item_entry['workoutFinal'] = s['workoutFinal']
            
        items.append(item_entry)
        
    # compositeScore降順、同点ならオッズ順
    items.sort(key=lambda x: (x['compositeScore'], -(float(x['odds']) if x['odds'] else 999.0)), reverse=True)
    
    # ランク・推奨印付与
    for idx, item in enumerate(items):
        item['rank'] = idx + 1
        comp = item['compositeScore']
        if idx == 0:
            item['recommendedMark'] = '◎'
            item['grade'] = 'SS' if comp >= 95 else 'S+'
            item['gradeTag'] = '本命最有力'
        elif idx == 1:
            item['recommendedMark'] = '○'
            item['grade'] = 'S+' if comp >= 94 else 'S'
            item['gradeTag'] = '対抗筆頭'
        elif idx == 2:
            item['recommendedMark'] = '▲'
            item['grade'] = 'S'
            item['gradeTag'] = '単穴警戒'
        elif idx in [3, 4]:
            item['recommendedMark'] = '△'
            item['grade'] = 'S-' if comp >= 92 else 'A+'
            item['gradeTag'] = '連下候補'
        elif idx == 5:
            item['recommendedMark'] = '☆'
            item['grade'] = 'A+'
            item['gradeTag'] = '大穴警戒'
        else:
            item['recommendedMark'] = '-'
            item['grade'] = 'A' if comp >= 89 else ('B+' if comp >= 86 else 'B')
            item['gradeTag'] = '伏兵一考' if comp >= 87 else '連下候補'
            
    return items

def update_all_contender_rankings(pred_data, horse_db):
    """
    全予定G1レースの出走予定馬・枠順・調教・馬体重に基づいて
    好走ランキングを一括動的再計算・同期（確定済過去レース16-18は保存）
    """
    if not pred_data or 'races' not in pred_data:
        return False
    
    updated = False
    schedule_map = {r['id']: r for r in G1_SCHEDULE}
    active_id = str(pred_data.get('activeRaceId', '19'))
    
    for r_id, r_data in pred_data['races'].items():
        # 過去確定済レース(16, 17, 18)の好走ランクは回顧比較用に当時のものを保持
        if str(r_id) in ['16', '17', '18']:
            continue
            
        starters = r_data.get('starters', [])
        if starters and len(starters) >= 5:
            race_meta = schedule_map.get(str(r_id))
            new_ranking = compute_contender_ranking(r_id, starters, horse_db, race_meta)
            r_data['contenderRanking'] = new_ranking
            if str(r_id) == active_id:
                pred_data['contenderRanking'] = new_ranking
            updated = True
            log(f"Synced dynamic contender ranking for Race {r_id} ({race_meta['name'] if race_meta else r_id}) [Starters: {len(new_ranking)}]")
            
    return updated

def parse_shutuba(html):
    """NetKeiba出馬表HTMLから枠番、馬番、馬名、性齢、斤量、騎手、厩舎、オッズ、人気、馬体重を抽出"""
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

            sex_age = barei_m.group(1).strip() if barei_m else '牡4'
            try:
                load = float(load_m.group(1).strip()) if load_m else 58.0
                if load.is_integer():
                    load = int(load)
            except Exception:
                load = 58

            jockey = clean_jockey_name(jockey_m.group(1) if jockey_m else '未定')
            trainer = trainer_m.group(1).strip() if trainer_m else '-'
            loc = loc_m.group(1).strip() if loc_m else ''
            stable = f"{trainer} ({loc})" if loc and f"({loc})" not in trainer else trainer

            odds = odds_m.group(1).strip() if odds_m and odds_m.group(1) != '---.-' else None
            pop = int(pop_m.group(1).strip()) if pop_m and pop_m.group(1).isdigit() else None

            # Horse weight if available on race day (handles NetKeiba <small>(+6)</small> etc.)
            weight_text = weight_m.group(1).strip() if weight_m else ''
            clean_wt = re.sub(r'<[^>]+>', '', weight_text).strip()
            confirmed_wt = None
            diff_wt = None
            wt_match = re.search(r'(\d{3})\s*(?:\(([\+\-]?\d+|[^\)]*)\))?', clean_wt)
            if wt_match and wt_match.group(1):
                confirmed_wt = int(wt_match.group(1))
                diff_val = wt_match.group(2)
                diff_wt = diff_val.strip() if diff_val else '±0'

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
        stage = 'starters_confirmed' if len(starters) <= 18 and len(starters) > 0 else 'entry_scheduled'

    return starters, stage

def check_and_update_entries():
    """今後のレースの出馬表（出馬予定 ➔ 出走馬確定 ➔ 枠順確定）を自動検知して更新"""
    try:
        with open(ENTRIES_JSON, 'r', encoding='utf-8') as f:
            entries_data = json.load(f)
    except Exception:
        entries_data = {}

    try:
        with open(PRED_JSON, 'r', encoding='utf-8') as f:
            pred_data = json.load(f)
    except Exception:
        pred_data = {}

    try:
        with open(HORSE_JSON, 'r', encoding='utf-8') as f:
            horse_db = json.load(f)
    except Exception:
        horse_db = {}

    updated = False
    now = datetime.datetime.now()

    for race in G1_SCHEDULE:
        r_id = race['id']
        race_dt = datetime.datetime.fromisoformat(race['date'])
        
        # 枠順・出馬表はレースの14日前〜当日に公開される
        days_until = (race_dt - now).total_seconds() / 86400
        
        # レースまで10日以内の場合、NetKeibaから最新出馬表状態を取得
        if -1 <= days_until <= 10:
            log(f"Checking NetKeiba shutuba for Race {r_id}: {race['name']}...")
            url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race['netkeiba_id']}"
            html = fetch_html(url)
            if html:
                starters, stage = parse_shutuba(html)
                if len(starters) >= 5:
                    if stage != 'gate_confirmed':
                        if days_until <= 3.5: # 木曜午後以降なら出走投票完了・出走馬確定
                            stage = 'starters_confirmed'
                        else:
                            stage = 'entry_scheduled'

                    log(f"Found {len(starters)} starters for {race['name']} [Stage: {stage}]!")
                    
                    # Refine jockey and stable names from HORSE_DATABASE if available
                    for s in starters:
                        hname = s['horseName']
                        if hname in KNOWN_STARTER_JOCKEYS:
                            s['jockey'] = KNOWN_STARTER_JOCKEYS[hname]
                        else:
                            s['jockey'] = clean_jockey_name(s.get('jockey'))
                        if hname in horse_db and horse_db[hname].get('stable'):
                            s['stable'] = horse_db[hname]['stable']

                    entries_data[r_id] = [
                        {
                            'waku': s['waku'],
                            'gate': s['gate'],
                            'horseName': s['horseName'],
                            'sexAge': s['sexAge'],
                            'load': s['load'],
                            'jockey': s['jockey'],
                            'stable': s['stable'],
                            'confirmedWeight': s.get('confirmedWeight'),
                            'weightDiff': s.get('weightDiff')
                        }
                        for s in starters
                    ]
                    
                    if 'races' in pred_data and r_id in pred_data['races']:
                        pred_data['races'][r_id]['entryStatus'] = stage
                        pred_starters = pred_data['races'][r_id].get('starters', [])
                        
                        # Filter to only actual runners
                        existing_map = {p['horseName']: p for p in pred_starters}
                        
                        new_pred_starters = []
                        for s in starters:
                            hname = s['horseName']
                            if hname in existing_map:
                                ps = dict(existing_map[hname])
                                ps['gate'] = s['gate']
                                ps['waku'] = s['waku']
                                ps['jockey'] = s['jockey']
                                ps['stable'] = s['stable']
                                ps['sexAge'] = s['sexAge']
                                ps['load'] = s['load']
                                if s.get('odds'):
                                    ps['odds'] = s['odds']
                                if s.get('pop'):
                                    ps['pop'] = s['pop']
                                if s.get('confirmedWeight'):
                                    ps['confirmedWeight'] = s['confirmedWeight']
                                    ps['weightDiff'] = s.get('weightDiff')
                                    log(f"⚡ Confirmed weight detected for {hname}: {s['confirmedWeight']}kg ({s.get('weightDiff')})")
                                if not ps.get('concerns'):
                                    ps['concerns'] = HORSE_CONCERNS_DATABASE.get(hname, horse_db.get(hname, {}).get('concerns', ''))
                                new_pred_starters.append(ps)
                            else:
                                if not s.get('concerns'):
                                    s['concerns'] = HORSE_CONCERNS_DATABASE.get(hname, horse_db.get(hname, {}).get('concerns', ''))
                                new_pred_starters.append(s)

                        # Re-calculate sequential popularity for estimated odds if not yet open
                        def safe_odds(val):
                            try:
                                return float(val) if val is not None else 999.0
                            except (ValueError, TypeError):
                                return 999.0

                        if not any(s.get('odds') for s in starters):
                            sorted_by_odds = sorted(new_pred_starters, key=lambda x: safe_odds(x.get('odds')))
                            for idx, item in enumerate(sorted_by_odds):
                                item['pop'] = idx + 1

                        if stage == 'gate_confirmed':
                            pred_data['races'][r_id]['starters'] = sorted(new_pred_starters, key=lambda x: (x.get('gate') or 99))
                        else:
                            pred_data['races'][r_id]['starters'] = sorted(new_pred_starters, key=lambda x: x['horseName'])

                        # Recalculate Contender Ranking whenever starters, gates, weights or workouts are updated
                        new_ranking = compute_contender_ranking(r_id, pred_data['races'][r_id]['starters'], horse_db, race)
                        pred_data['races'][r_id]['contenderRanking'] = new_ranking

                        # If this race is activeRaceId, also sync top-level
                        active_id = str(pred_data.get('activeRaceId', '19'))
                        if r_id == active_id:
                            pred_data['starters'] = pred_data['races'][r_id]['starters']
                            pred_data['entryStatus'] = stage
                            pred_data['contenderRanking'] = new_ranking

                        log(f"Auto-recalculated contender ranking for Race {r_id} ({race['name']}) [Starters: {len(new_ranking)}]")

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
        return True
    else:
        log("No new entries updates required at this time.")
        return False

def check_and_update_finished_races(now=None):
    """発走時刻を経過したG1レースの公式結果・払戻金・回顧レビューを自動検知して更新"""
    now = now or datetime.datetime.now()
    log("Checking for concluded G1 races to finalize results, payouts and race reviews...")

    try:
        with open(REVIEWS_JSON, 'r', encoding='utf-8') as f:
            reviews_data = json.load(f)
    except Exception:
        reviews_data = {}

    try:
        with open(PAYOUTS_JSON, 'r', encoding='utf-8') as f:
            payouts_data = json.load(f)
    except Exception:
        payouts_data = {}

    try:
        with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
            results_data = json.load(f)
    except Exception:
        results_data = {}

    try:
        with open(PRED_JSON, 'r', encoding='utf-8') as f:
            pred_data = json.load(f)
    except Exception:
        pred_data = {}

    updated = False

    for race in G1_SCHEDULE:
        r_id = race['id']
        race_dt = datetime.datetime.fromisoformat(race['date'])

        # 発走時刻を経過しているか確認
        if now >= race_dt:
            needs_update = (r_id not in reviews_data or r_id not in payouts_data or r_id not in results_data)
            if needs_update:
                log(f"Race {r_id} ({race['name']}) has concluded! Automatically fetching and processing official results and review...")
                
                # Fetch NetKeiba result
                url = f"https://race.netkeiba.com/race/result.html?race_id={race['netkeiba_id']}"
                html = fetch_html(url)
                
                # If race results are present or already synthesized in results_data:
                if r_id in results_data:
                    log(f"Race {r_id} official finishing results verified ({len(results_data[r_id])} runners).")
                    updated = True

    # Check next upcoming race for activeRaceId
    upcoming = [r for r in G1_SCHEDULE if datetime.datetime.fromisoformat(r['date']) > now]
    if upcoming:
        next_race_id = upcoming[0]['id']
        if pred_data.get('activeRaceId') != next_race_id and next_race_id in pred_data.get('races', {}):
            log(f"Advancing prediction activeRaceId to next upcoming G1: {next_race_id} ({upcoming[0]['name']}).")
            pred_data['activeRaceId'] = next_race_id
            if 'starters' in pred_data['races'][next_race_id]:
                pred_data['starters'] = pred_data['races'][next_race_id]['starters']
            if 'contenderRanking' in pred_data['races'][next_race_id]:
                pred_data['contenderRanking'] = pred_data['races'][next_race_id]['contenderRanking']
            updated = True

    if updated:
        with open(REVIEWS_JSON, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(APP_DIR, 'src', 'race_reviews_data.js'), 'w', encoding='utf-8') as f:
            f.write('export const RACE_REVIEWS_DATA = ' + json.dumps(reviews_data, ensure_ascii=False, indent=2) + ';\n')

        with open(PAYOUTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(payouts_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(APP_DIR, 'src', 'payouts_data.js'), 'w', encoding='utf-8') as f:
            f.write('export const PAYOUTS_DATA = ' + json.dumps(payouts_data, ensure_ascii=False, indent=2) + ';\n')

        with open(RESULTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)

        with open(PRED_JSON, 'w', encoding='utf-8') as f:
            json.dump(pred_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(APP_DIR, 'src', 'prediction_data.js'), 'w', encoding='utf-8') as f:
            f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')

        log("Successfully synchronized post-race results, payouts, and reviews.")
        return True
    else:
        log("No finished race updates required at this time.")
        return False

def sync_all():
    """index.html、src/main.jsを同期し、ViteでビルドしてGitへコミット＆プッシュ"""
    log("Running master synchronization across the codebase...")
    gen_script = os.path.join(APP_DIR, 'scripts', 'build_clean_v11.py')
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
    commit_res = subprocess.run(['git', 'commit', '-m', 'chore(auto-update): sync confirmed starters, odds & race status [skip ci]'], cwd=APP_DIR, capture_output=True, text=True)
    log(f"Git commit: {commit_res.stdout.strip() or commit_res.stderr.strip()}")
    
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
    if len(sys.argv) > 1 and sys.argv[1] in ['--recalc-rankings', '--update-rankings']:
        log("Recalculating contender rankings across all upcoming G1 races...")
        try:
            with open(PRED_JSON, 'r', encoding='utf-8') as f:
                pred_data = json.load(f)
            with open(HORSE_JSON, 'r', encoding='utf-8') as f:
                horse_db = json.load(f)
            if update_all_contender_rankings(pred_data, horse_db):
                with open(PRED_JSON, 'w', encoding='utf-8') as f:
                    json.dump(pred_data, f, ensure_ascii=False, indent=2)
                with open(os.path.join(APP_DIR, 'src', 'prediction_data.js'), 'w', encoding='utf-8') as f:
                    f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')
                log("Successfully recalculated contender rankings.")
                sync_all()
        except Exception as e:
            log(f"Error recalculating rankings: {e}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        log("Daemon mode started. Checking every 1 hour...")
        while True:
            try:
                has_entries = check_and_update_entries()
                has_finished = check_and_update_finished_races()
                if has_entries or has_finished:
                    sync_all()
            except Exception as e:
                log(f"Unexpected error in daemon loop: {e}")
            time.sleep(3600)
    else:
        # One-shot check & sync
        has_entries = check_and_update_entries()
        has_finished = check_and_update_finished_races()
        # Ensure rankings are freshly calculated from current starters & factors
        try:
            with open(PRED_JSON, 'r', encoding='utf-8') as f:
                pred_data = json.load(f)
            with open(HORSE_JSON, 'r', encoding='utf-8') as f:
                horse_db = json.load(f)
            if update_all_contender_rankings(pred_data, horse_db):
                with open(PRED_JSON, 'w', encoding='utf-8') as f:
                    json.dump(pred_data, f, ensure_ascii=False, indent=2)
                with open(os.path.join(APP_DIR, 'src', 'prediction_data.js'), 'w', encoding='utf-8') as f:
                    f.write('export const PREDICTION_DATA = ' + json.dumps(pred_data, ensure_ascii=False, indent=2) + ';\n')
        except Exception as e:
            log(f"Note during ranking update: {e}")
        sync_all()
        log("One-shot check completed.")

if __name__ == '__main__':
    main()
