import json
import os

keiba_app_dir = '/Users/ooshita/.gemini/antigravity/scratch/keiba-app'
entries_json_path = os.path.join(keiba_app_dir, 'src', 'entries_data.json')
entries_js_path = os.path.join(keiba_app_dir, 'src', 'entries_data.js')
pred_json_path = os.path.join(keiba_app_dir, 'src', 'prediction_data.json')
pred_js_path = os.path.join(keiba_app_dir, 'src', 'prediction_data.js')

# Load existing entries & prediction data
with open(entries_json_path, 'r', encoding='utf-8') as f:
    entries_data = json.load(f)

with open(pred_json_path, 'r', encoding='utf-8') as f:
    pred_data = json.load(f)

# Ensure races dict in pred_data
if 'races' not in pred_data:
    pred_data['races'] = {}

# ----------------------------------------------------
# 17: エリザベス女王杯 (2026.11.15 京都芝2200m) - Already compiled, verify & refine
# ----------------------------------------------------
r17_starters = [
  {"waku": 1, "gate": 1, "horseName": "レーゼドラマ", "sexAge": "牝4", "load": 56, "jockey": "松若風馬", "stable": "杉山晴紀 (栗東)", "odds": "18.2", "placeOdds": "4.2 - 6.5", "pop": 7, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.8 - 38.0 - 24.5 - 12.1 (馬なり)", "trainingComment": "坂路で素軽さ満点。距離延長にもスムーズに対応可能な気配。", "trainingWeight": 472, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "ラヴァンダ", "sexAge": "牝4", "load": 56, "jockey": "岩田望来", "stable": "中村直也 (栗東)", "odds": "12.4", "placeOdds": "2.8 - 4.1", "pop": 5, "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "82.4 - 66.2 - 51.5 - 36.8 - 11.4 (強め)", "trainingComment": "CWで鋭伸。京都外回りの差し脚勝負にドンピシャの仕上がり。", "trainingWeight": 480, "lastRaceWeight": 476, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "クイーンズウォーク", "sexAge": "牝4", "load": 56, "jockey": "C.デムーロ", "stable": "中内田充正 (栗東)", "odds": "4.2", "placeOdds": "1.5 - 2.1", "pop": 2, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "81.2 - 65.4 - 50.8 - 36.1 - 11.2 (馬なり)", "trainingComment": "迫力満点のフットワーク。短期免許C.デムーロ騎手への勝負乗り替わりで戴冠へ視界良好。", "trainingWeight": 524, "lastRaceWeight": 518, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "カムニャック", "sexAge": "牝4", "load": 56, "jockey": "川田将雅", "stable": "友道康夫 (栗東)", "odds": "3.5", "placeOdds": "1.4 - 1.9", "pop": 1, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "80.8 - 65.0 - 50.4 - 35.8 - 11.0 (一杯)", "trainingComment": "前走以上の活気。川田騎手が付きっ切りで調整しラスト11.0秒。古馬牝馬王道へ死角なし。", "trainingWeight": 508, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "セキトバイースト", "sexAge": "牝4", "load": 56, "jockey": "浜中俊", "stable": "四位洋文 (栗東)", "odds": "24.6", "placeOdds": "5.2 - 8.0", "pop": 9, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "53.0 - 38.2 - 24.6 - 12.2 (馬なり)", "trainingComment": "果敢にハナを主張する構え。京都外回りでマイペースに持ち込めれば一発も。", "trainingWeight": 466, "lastRaceWeight": 462, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "チェルヴィニア", "sexAge": "牝4", "load": 56, "jockey": "C.ルメール", "stable": "木村哲也 (美浦)", "odds": "4.8", "placeOdds": "1.6 - 2.3", "pop": 3, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "82.0 - 66.0 - 51.2 - 36.4 - 11.1 (強め)", "trainingComment": "美浦Wで圧巻の伸び脚。ルメール騎手との黄金タッグで京都芝2200m適性は最高峰。", "trainingWeight": 492, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 7, "horseName": "ステレンボッシュ", "sexAge": "牝4", "load": 56, "jockey": "戸崎圭太", "stable": "国枝栄 (美浦)", "odds": "5.6", "placeOdds": "1.8 - 2.6", "pop": 4, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "83.1 - 66.8 - 51.6 - 36.7 - 11.3 (馬なり)", "trainingComment": "天皇賞秋を制した戸崎騎手を背に軽快な動き。大舞台での勝負強さは折り紙付き。", "trainingWeight": 476, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 8, "horseName": "ジュウリョクピエロ", "sexAge": "牝4", "load": 56, "jockey": "今村聖奈", "stable": "寺島良 (栗東)", "odds": "14.8", "placeOdds": "3.2 - 4.8", "pop": 6, "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "82.6 - 66.5 - 51.8 - 36.9 - 11.5 (馬なり)", "trainingComment": "オークス上位の底力。今村聖奈騎手との強い絆で外回り下り坂からのロングスパートを狙う。", "trainingWeight": 468, "lastRaceWeight": 464, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 9, "horseName": "コガネノソラ", "sexAge": "牝4", "load": 56, "jockey": "丹内祐次", "stable": "菊沢隆徳 (美浦)", "odds": "28.5", "placeOdds": "6.0 - 9.5", "pop": 10, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "84.0 - 67.4 - 52.2 - 37.1 - 11.8 (馬なり)", "trainingComment": "素軽さ十分。インコースで脚を溜めて上位進出を伺う。", "trainingWeight": 458, "lastRaceWeight": 454, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 10, "horseName": "サフィラ", "sexAge": "牝4", "load": 56, "jockey": "北村友一", "stable": "池添学 (栗東)", "odds": "32.0", "placeOdds": "7.1 - 11.0", "pop": 11, "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "53.5 - 38.6 - 24.9 - 12.4 (強め)", "trainingComment": "良血馬の血が騒ぐ。長丁場で折り合いがつけば怖い存在。", "trainingWeight": 464, "lastRaceWeight": 460, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 11, "horseName": "ニシノティアモ", "sexAge": "牝4", "load": 56, "jockey": "津村明秀", "stable": "上原博之 (美浦)", "odds": "45.0", "placeOdds": "9.5 - 15.0", "pop": 12, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "84.5 - 67.8 - 52.6 - 37.4 - 11.9 (馬なり)", "trainingComment": "調教自体は順調。展開がハマれば浮上の余地あり。", "trainingWeight": 486, "lastRaceWeight": 482, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 12, "horseName": "マリアイリダータ", "sexAge": "牝4", "load": 56, "jockey": "坂井瑠星", "stable": "矢作芳人 (栗東)", "odds": "22.0", "placeOdds": "4.8 - 7.5", "pop": 8, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.8 - 66.6 - 51.9 - 36.8 - 11.6 (強め)", "trainingComment": "矢作厩舎＆坂井瑠星の勝負気配。好位から積極的な競馬を演出。", "trainingWeight": 474, "lastRaceWeight": 470, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 13, "horseName": "ジョスラン", "sexAge": "牝4", "load": 56, "jockey": "武豊", "stable": "鹿戸雄一 (美浦)", "odds": "48.0", "placeOdds": "10.0 - 16.0", "pop": 13, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "84.2 - 67.6 - 52.4 - 37.2 - 11.8 (馬なり)", "trainingComment": "レジェンド武豊騎手の手綱捌きに注目。淀の外回りは知り尽くしている舞台。", "trainingWeight": 470, "lastRaceWeight": 466, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 14, "horseName": "ケリフレッドアスク", "sexAge": "牝4", "load": 56, "jockey": "吉田隼人", "stable": "矢作芳人 (栗東)", "odds": "62.0", "placeOdds": "12.5 - 20.0", "pop": 14, "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "53.8 - 39.0 - 25.1 - 12.5 (馬なり)", "trainingComment": "タフな馬場やハイペースになれば渋太く脚を伸ばす。", "trainingWeight": 488, "lastRaceWeight": 484, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 15, "horseName": "エストゥペンダ", "sexAge": "牝4", "load": 56, "jockey": "荻野極", "stable": "高柳瑞樹 (美浦)", "odds": "78.0", "placeOdds": "15.0 - 24.0", "pop": 15, "trainingGrade": "B-", "trainingCourse": "美浦W", "trainingTime": "85.1 - 68.2 - 53.0 - 37.8 - 12.1 (馬なり)", "trainingComment": "大外枠からの競馬。後方待機から直線一気の勝負。", "trainingWeight": 462, "lastRaceWeight": 458, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 16, "horseName": "エセルフリーダ", "sexAge": "牝4", "load": 56, "jockey": "武藤雅", "stable": "武藤善則 (美浦)", "odds": "95.0", "placeOdds": "18.0 - 28.0", "pop": 16, "trainingGrade": "B-", "trainingCourse": "美浦W", "trainingTime": "54.2 - 39.4 - 25.5 - 12.6 (強め)", "trainingComment": "相手関係は強化されるが、状態はキープ。", "trainingWeight": 454, "lastRaceWeight": 450, "confirmedWeight": None, "weightDiff": None}
]

pred_data['races']['17']['starters'] = r17_starters
entries_data['17'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r17_starters]

# ----------------------------------------------------
# 18: マイルチャンピオンシップ (2026.11.22 京都芝1600m)
# ----------------------------------------------------
r18_starters = [
  {"waku": 1, "gate": 1, "horseName": "ソウルラッシュ", "sexAge": "牡8", "load": 58, "jockey": "団野大成", "stable": "池江泰寿 (栗東)", "odds": "3.8", "placeOdds": "1.4 - 2.0", "pop": 1, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "80.2 - 64.8 - 50.1 - 35.6 - 11.0 (馬なり)", "trainingComment": "8歳でも衰え知らず。連覇へ向けてCWで抜群の推進力とキレを披露。", "trainingWeight": 514, "lastRaceWeight": 512, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "ブレイディヴェーグ", "sexAge": "牝5", "load": 56, "jockey": "C.ルメール", "stable": "宮田敬介 (美浦)", "odds": "4.2", "placeOdds": "1.5 - 2.2", "pop": 2, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "81.6 - 65.5 - 50.8 - 36.2 - 11.1 (強め)", "trainingComment": "マイルへの距離短縮は吉。美浦Wで僚馬を一瞬で置き去りにする鬼脚。", "trainingWeight": 478, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "チャリン", "sexAge": "牡5", "load": 58, "jockey": "R.ムーア", "stable": "R.ヴェリアン (海外)", "odds": "4.9", "placeOdds": "1.6 - 2.4", "pop": 3, "trainingGrade": "A", "trainingCourse": "京都芝", "trainingTime": "64.2 - 49.5 - 35.8 - 11.3 (馬なり)", "trainingComment": "欧州マイル王が電撃来日。時計の速い日本の芝にも難なく対応するフットワーク。", "trainingWeight": 506, "lastRaceWeight": 502, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "ナミュール", "sexAge": "牝6", "load": 56, "jockey": "C.デムーロ", "stable": "高野友和 (栗東)", "odds": "6.1", "placeOdds": "2.0 - 2.9", "pop": 4, "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "52.4 - 37.8 - 24.2 - 11.8 (馬なり)", "trainingComment": "淀外回りはベスト舞台。C.デムーロとの相性も抜群で直線一気に賭ける。", "trainingWeight": 458, "lastRaceWeight": 454, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "ジュンブロッサム", "sexAge": "牡7", "load": 58, "jockey": "戸崎圭太", "stable": "友道康夫 (栗東)", "odds": "8.5", "placeOdds": "2.4 - 3.5", "pop": 5, "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "82.1 - 66.0 - 51.2 - 36.5 - 11.2 (一杯)", "trainingComment": "富士S勝ち馬の切れ味健在。天皇賞秋からの連闘ローテでも活気十分。", "trainingWeight": 474, "lastRaceWeight": 476, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "セリフォス", "sexAge": "牡6", "load": 58, "jockey": "川田将雅", "stable": "中内田充正 (栗東)", "odds": "10.2", "placeOdds": "2.7 - 3.9", "pop": 6, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.8 - 66.5 - 51.5 - 36.8 - 11.4 (強め)", "trainingComment": "マイルCS過去優勝馬の底力。折り合いがつけば終い確実に伸びてくる。", "trainingWeight": 490, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 7, "horseName": "エルトンバローズ", "sexAge": "牡6", "load": 58, "jockey": "西村淳也", "stable": "杉山晴紀 (栗東)", "odds": "14.5", "placeOdds": "3.5 - 5.0", "pop": 7, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "53.2 - 38.4 - 24.8 - 12.0 (馬なり)", "trainingComment": "マイル適性高く、好位インで立ち回れれば粘り込みが期待できる。", "trainingWeight": 516, "lastRaceWeight": 518, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 8, "horseName": "ウインマーベル", "sexAge": "牡6", "load": 58, "jockey": "松山弘平", "stable": "深山雅史 (美浦)", "odds": "18.0", "placeOdds": "4.2 - 6.2", "pop": 8, "trainingGrade": "B+", "trainingCourse": "美浦W", "trainingTime": "83.0 - 66.8 - 51.8 - 37.0 - 11.5 (強め)", "trainingComment": "スプリント重賞常連がマイルへ。先行力を活かして粘り強い競馬を。", "trainingWeight": 482, "lastRaceWeight": 478, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 9, "horseName": "フィアスプライド", "sexAge": "牝6", "load": 56, "jockey": "坂井瑠星", "stable": "国枝栄 (美浦)", "odds": "22.5", "placeOdds": "5.0 - 7.5", "pop": 9, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "83.8 - 67.2 - 52.1 - 37.3 - 11.7 (馬なり)", "trainingComment": "ヴィクトリアマイル2着の実力派。坂井瑠星の強気な騎乗で波乱を呼ぶ。", "trainingWeight": 486, "lastRaceWeight": 484, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 10, "horseName": "オフトレイル", "sexAge": "牡4", "load": 57, "jockey": "武豊", "stable": "吉村圭司 (栗東)", "odds": "26.0", "placeOdds": "5.8 - 8.5", "pop": 10, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "83.5 - 67.0 - 52.0 - 37.2 - 11.6 (強め)", "trainingComment": "レジェンド武豊とのコンビ。直線勝負に徹すれば上位争いも。", "trainingWeight": 470, "lastRaceWeight": 466, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 11, "horseName": "マテンロウスカイ", "sexAge": "牡6", "load": 58, "jockey": "横山典弘", "stable": "松永幹夫 (栗東)", "odds": "34.0", "placeOdds": "7.5 - 11.5", "pop": 11, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "84.0 - 67.5 - 52.4 - 37.5 - 11.8 (馬なり)", "trainingComment": "中山記念馬。自分のリズムで運べれば侮れない持続力を持つ。", "trainingWeight": 488, "lastRaceWeight": 484, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 12, "horseName": "アルナシーム", "sexAge": "牡6", "load": 58, "jockey": "藤岡佑介", "stable": "橋口慎介 (栗東)", "odds": "42.0", "placeOdds": "9.0 - 14.0", "pop": 12, "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "53.6 - 38.8 - 25.0 - 12.3 (馬なり)", "trainingComment": "中京記念勝ちの実績。好調キープでマイペースなら。", "trainingWeight": 460, "lastRaceWeight": 458, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 13, "horseName": "ニヒロベルム", "sexAge": "牡4", "load": 57, "jockey": "岩田望来", "stable": "木村哲也 (美浦)", "odds": "55.0", "placeOdds": "11.0 - 17.0", "pop": 13, "trainingGrade": "B-", "trainingCourse": "美浦W", "trainingTime": "84.6 - 68.0 - 52.9 - 37.8 - 12.0 (馬なり)", "trainingComment": "大舞台の経験を積んで成長中。一角崩しを狙う。", "trainingWeight": 492, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 14, "horseName": "レイベリング", "sexAge": "牡5", "load": 58, "jockey": "津村明秀", "stable": "鹿戸雄一 (美浦)", "odds": "68.0", "placeOdds": "13.0 - 20.0", "pop": 14, "trainingGrade": "B-", "trainingCourse": "美浦W", "trainingTime": "85.0 - 68.2 - 53.2 - 38.0 - 12.2 (強め)", "trainingComment": "朝日杯FS3着の実績。仕上がり順調でスムーズな先行を。", "trainingWeight": 502, "lastRaceWeight": 498, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 15, "horseName": "バルサムノート", "sexAge": "牡5", "load": 58, "jockey": "北村友一", "stable": "高野友和 (栗東)", "odds": "85.0", "placeOdds": "16.0 - 25.0", "pop": 15, "trainingGrade": "B-", "trainingCourse": "栗東坂路", "trainingTime": "54.0 - 39.2 - 25.4 - 12.5 (馬なり)", "trainingComment": "坂路で入念に乗り込み。展開の恩恵を待ちたい。", "trainingWeight": 498, "lastRaceWeight": 494, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 16, "horseName": "コムストックロード", "sexAge": "牝6", "load": 56, "jockey": "幸英明", "stable": "中野栄治 (美浦)", "odds": "110.0", "placeOdds": "20.0 - 32.0", "pop": 16, "trainingGrade": "C", "trainingCourse": "美浦W", "trainingTime": "85.8 - 69.0 - 53.8 - 38.5 - 12.5 (馬なり)", "trainingComment": "状態は維持。無欲の追い込みでどこまで迫れるか。", "trainingWeight": 466, "lastRaceWeight": 462, "confirmedWeight": None, "weightDiff": None}
]

r18_occult = [
  {"id": 1, "title": "🌍 欧州最強マイラー「チャリン」参戦！外車無双と京都高速芝の法則", "badge": "海外超強豪", "source": "X・競馬考察トレンド", "content": "欧州マイルG1を連勝中のチャリンが電撃参戦！英国馬がマイルCSに参戦するのは異例中の異例。京都競馬場の馬場造園課が手掛ける超高速芝は、欧州の重い芝とは対極ながら、チャリンの圧倒的巡航スピードは日本のマイラーを圧倒する可能性があるとXで大激論！", "targets": [{"gate": 3, "waku": 2, "name": "チャリン"}]},
  {"id": 2, "title": "👑 マイルCS名物「リピーターの法則」ソウルラッシュVSセリフォス", "badge": "リピーター神話", "source": "競馬データ班", "content": "マイルCSは過去ダイタクヘリオス、デュランダル、グランアレグリアと『同じ馬が何度も馬券に絡む』伝統のレース。8歳になっても衰えぬソウルラッシュと中内田厩舎のセリフォス。この2頭のBOXは秋の黄金パターン！", "targets": [{"gate": 1, "waku": 1, "name": "ソウルラッシュ"}, {"gate": 6, "waku": 3, "name": "セリフォス"}]},
  {"id": 3, "title": "✨ ルメール×宮田厩舎「ブレイディヴェーグ」距離短縮の勝算サイン", "badge": "ルメールマジック", "source": "SNSサイン研究会", "content": "マイルへの短縮挑戦となるエリ女覇者ブレイディヴェーグ。ルメール騎手が『マイルのスピードに対応できる』と太鼓判を押す背景には、秋のマイル路線の牝馬戴冠トレンドが存在。白い帽子1枠からのイン強襲が噂されています。", "targets": [{"gate": 2, "waku": 1, "name": "ブレイディヴェーグ"}]}
]

entries_data['18'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r18_starters]
pred_data['races']['18'] = {
  "raceId": "18",
  "raceName": "第43回 マイルチャンピオンシップ",
  "date": "2026年11月22日(日) 15:40発走",
  "venue": "京都競馬場 芝1600m (外回り)",
  "starters": r18_starters,
  "occultSigns": r18_occult
}

# ----------------------------------------------------
# 19: ジャパンカップ (2026.11.29 東京芝2400m)
# ----------------------------------------------------
r19_starters = [
  {"waku": 1, "gate": 1, "horseName": "ドウデュース", "sexAge": "牡6", "load": 58, "jockey": "武豊", "stable": "友道康夫 (栗東)", "odds": "2.8", "placeOdds": "1.3 - 1.7", "pop": 1, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "79.8 - 64.2 - 49.8 - 35.2 - 10.9 (馬なり)", "trainingComment": "日本競馬の総大将。ラストイヤー有終の秋古馬三冠へ向けて究極の仕上がり。", "trainingWeight": 508, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "オーギュストロダン", "sexAge": "牡5", "load": 58, "jockey": "R.ムーア", "stable": "A.オブライエン (海外)", "odds": "3.5", "placeOdds": "1.4 - 1.9", "pop": 2, "trainingGrade": "S", "trainingCourse": "東京芝", "trainingTime": "65.0 - 50.2 - 36.1 - 11.2 (馬なり)", "trainingComment": "ディープインパクト最終世代の世界的最高傑作。引退花道へ東京芝2400mは運命の舞台。", "trainingWeight": 472, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "チェルヴィニア", "sexAge": "牝4", "load": 54, "jockey": "C.ルメール", "stable": "木村哲也 (美浦)", "odds": "4.5", "placeOdds": "1.6 - 2.2", "pop": 3, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "81.8 - 65.6 - 51.0 - 36.3 - 11.1 (強め)", "trainingComment": "オークス馬の東京2400m適性。斤量54kgの恩恵は絶大で古馬撃破を狙う。", "trainingWeight": 490, "lastRaceWeight": 488, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "ゴリアット", "sexAge": "セ5", "load": 58, "jockey": "C.スミヨン", "stable": "F.グラファール (海外)", "odds": "6.8", "placeOdds": "2.1 - 3.2", "pop": 4, "trainingGrade": "A", "trainingCourse": "東京芝", "trainingTime": "65.5 - 50.8 - 36.4 - 11.4 (強め)", "trainingComment": "英キングジョージ圧勝の超強豪。欧州トップクラスのロングスパート能力。", "trainingWeight": 486, "lastRaceWeight": 482, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "スターズオンアース", "sexAge": "牝6", "load": 56, "jockey": "川田将雅", "stable": "高柳瑞樹 (美浦)", "odds": "8.2", "placeOdds": "2.4 - 3.6", "pop": 5, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "82.5 - 66.2 - 51.4 - 36.6 - 11.3 (馬なり)", "trainingComment": "ジャパンC3着の実績。東京コースで崩れたことがない抜群の安定感。", "trainingWeight": 496, "lastRaceWeight": 492, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "ジャスティンパレス", "sexAge": "牡6", "load": 58, "jockey": "坂井瑠星", "stable": "杉山晴紀 (栗東)", "odds": "11.0", "placeOdds": "2.8 - 4.2", "pop": 6, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.8 - 66.5 - 51.8 - 36.8 - 11.5 (強め)", "trainingComment": "東京芝2400mで真価発揮。坂井瑠星のアグレッシブな騎乗で上位食い込み。", "trainingWeight": 472, "lastRaceWeight": 470, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 7, "horseName": "シンエンペラー", "sexAge": "牡4", "load": 56, "jockey": "吉田豊", "stable": "矢作芳人 (栗東)", "odds": "14.5", "placeOdds": "3.5 - 5.1", "pop": 7, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.6 - 38.0 - 24.6 - 12.1 (馬なり)", "trainingComment": "愛チャンピオンS3着から凱旋門賞を経て帰国。世界基準の先行力を持つ。", "trainingWeight": 488, "lastRaceWeight": 485, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 8, "horseName": "ブローザホーン", "sexAge": "牡6", "load": 58, "jockey": "菅原明良", "stable": "吉岡辰弥 (栗東)", "odds": "17.0", "placeOdds": "3.9 - 5.8", "pop": 8, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "53.2 - 38.6 - 24.9 - 12.2 (一杯)", "trainingComment": "宝塚記念覇者。タフな展開になればなるほど驚異的なスタミナを発揮。", "trainingWeight": 432, "lastRaceWeight": 428, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 9, "horseName": "ソールオリエンス", "sexAge": "牡5", "load": 58, "jockey": "横山武史", "stable": "手塚貴久 (美浦)", "odds": "21.0", "placeOdds": "4.6 - 6.8", "pop": 9, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "83.4 - 67.0 - 52.0 - 37.0 - 11.6 (馬なり)", "trainingComment": "皐月賞馬の豪脚。直線の長い東京コースで末脚一閃のシーンも。", "trainingWeight": 468, "lastRaceWeight": 464, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 10, "horseName": "ファンタスティックムーン", "sexAge": "牡5", "load": 58, "jockey": "R.ピーヒュレク", "stable": "S.シュタインベルク (海外)", "odds": "28.0", "placeOdds": "6.0 - 9.0", "pop": 10, "trainingGrade": "B", "trainingCourse": "東京芝", "trainingTime": "66.0 - 51.2 - 37.0 - 11.8 (馬なり)", "trainingComment": "独ダービー馬。良馬場の軽い芝を求めての日本遠征。", "trainingWeight": 462, "lastRaceWeight": 460, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 11, "horseName": "シュトルーヴェ", "sexAge": "セ6", "load": 58, "jockey": "佐々木大輔", "stable": "堀宣行 (美浦)", "odds": "35.0", "placeOdds": "7.5 - 11.5", "pop": 11, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "84.0 - 67.5 - 52.4 - 37.4 - 11.8 (強め)", "trainingComment": "東京芝2500m重賞連勝の実績。長い直線での持続力は上位。", "trainingWeight": 476, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 12, "horseName": "ドゥレッツァ", "sexAge": "牡5", "load": 58, "jockey": "戸崎圭太", "stable": "尾関知人 (美浦)", "odds": "38.0", "placeOdds": "8.0 - 12.5", "pop": 12, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "84.5 - 67.8 - 52.6 - 37.6 - 11.9 (馬なり)", "trainingComment": "菊花賞馬。英国インターナショナルS好走からの復調気配。", "trainingWeight": 470, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 13, "horseName": "ディープボンド", "sexAge": "牡8", "load": 58, "jockey": "幸英明", "stable": "大久保龍志 (栗東)", "odds": "52.0", "placeOdds": "10.5 - 16.0", "pop": 13, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "83.8 - 67.2 - 52.2 - 37.3 - 12.0 (馬なり)", "trainingComment": "8歳でも元気一杯。スタミナ勝負に持ち込めば大ベテランの意地を見せる。", "trainingWeight": 512, "lastRaceWeight": 510, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 14, "horseName": "カラテ", "sexAge": "牡9", "load": 58, "jockey": "杉原誠人", "stable": "音無秀孝 (栗東)", "odds": "88.0", "placeOdds": "18.0 - 28.0", "pop": 14, "trainingGrade": "C", "trainingCourse": "栗東坂路", "trainingTime": "54.5 - 39.8 - 25.8 - 12.7 (馬なり)", "trainingComment": "9歳でも無事に出走。ファンを沸かせる激走を。", "trainingWeight": 530, "lastRaceWeight": 526, "confirmedWeight": None, "weightDiff": None}
]

r19_occult = [
  {"id": 1, "title": "🕊️ ディープインパクト最後の最高傑作「オーギュストロダン」引退の花道サイン", "badge": "世界遺産級サイン", "source": "X・海外競馬トレンド", "content": "世界的名将オブライエン調教師が『ディープインパクトの子で日本を制する』ために引退レースに選んだジャパンカップ。東京競馬場のディープインパクト像の前で、息子が世界の頂点に立つという競馬の神様が描く奇跡のシナリオにX競馬民が熱狂！", "targets": [{"gate": 2, "waku": 1, "name": "オーギュストロダン"}]},
  {"id": 2, "title": "⚔️ レジェンド武豊「ドウデュース」ラストイヤー秋古馬三冠王手サイン", "badge": "英雄伝説", "source": "競馬サイン考察班", "content": "天皇賞（秋）で見せた異次元の末脚。秋古馬三冠（天皇賞秋・JC・有馬記念）の偉業へ王手をかけたドウデュース。武豊騎手×ジャパンカップの勝率は過去圧倒的で、白帽子1枠での激走サインが点灯中！", "targets": [{"gate": 1, "waku": 1, "name": "ドウデュース"}]},
  {"id": 3, "title": "🇫🇷 英キングジョージ覇者「ゴリアット」スミヨン鞍上の破壊力", "badge": "欧州超特急", "source": "JRAサイン攻略室", "content": "キングジョージで欧州最強馬たちを一蹴したゴリアット。日本を知り尽くす名手スミヨン騎手とのコンビは、かつてのエピファネイアを彷彿とさせる圧勝劇の予兆と囁かれています。", "targets": [{"gate": 4, "waku": 2, "name": "ゴリアット"}]}
]

entries_data['19'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r19_starters]
pred_data['races']['19'] = {
  "raceId": "19",
  "raceName": "第46回 ジャパンカップ",
  "date": "2026年11月29日(日) 15:40発走",
  "venue": "東京競馬場 芝2400m",
  "starters": r19_starters,
  "occultSigns": r19_occult
}

# ----------------------------------------------------
# 20: チャンピオンズカップ (2026.12.06 中京ダート1800m)
# ----------------------------------------------------
r20_starters = [
  {"waku": 1, "gate": 1, "horseName": "レモンポップ", "sexAge": "牡7", "load": 58, "jockey": "坂井瑠星", "stable": "田中博康 (美浦)", "odds": "2.2", "placeOdds": "1.2 - 1.5", "pop": 1, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "80.4 - 64.5 - 49.8 - 35.5 - 11.2 (馬なり)", "trainingComment": "国内ダート無敗の絶対王者。引退レースとなる中京1800m逃げ切り連覇へ万全の仕上げ。", "trainingWeight": 520, "lastRaceWeight": 516, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "ウィルソンテソーロ", "sexAge": "牡6", "load": 58, "jockey": "川田将雅", "stable": "小手川準 (美浦)", "odds": "3.8", "placeOdds": "1.4 - 2.0", "pop": 2, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "82.0 - 65.8 - 50.8 - 36.4 - 11.4 (強め)", "trainingComment": "JBCクラシック圧勝の勢いそのまま。中京の小回りを川田が完璧にエスコート。", "trainingWeight": 490, "lastRaceWeight": 486, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "ペプチドナイル", "sexAge": "牡6", "load": 58, "jockey": "藤岡佑介", "stable": "武英智 (栗東)", "odds": "6.5", "placeOdds": "1.9 - 2.8", "pop": 3, "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "51.8 - 37.4 - 24.0 - 11.9 (馬なり)", "trainingComment": "フェブラリーS覇者。坂路で破格の時計を連発し状態ピーク。", "trainingWeight": 532, "lastRaceWeight": 528, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "クラウンプライド", "sexAge": "牡6", "load": 58, "jockey": "横山武史", "stable": "新谷功一 (栗東)", "odds": "8.0", "placeOdds": "2.2 - 3.4", "pop": 4, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.5 - 66.2 - 51.5 - 36.8 - 11.5 (強め)", "trainingComment": "コリアカップ連覇の強豪。先行力と粘り腰は世界基準。", "trainingWeight": 504, "lastRaceWeight": 500, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "セラフィックコール", "sexAge": "牡5", "load": 58, "jockey": "C.デムーロ", "stable": "寺島良 (栗東)", "odds": "10.5", "placeOdds": "2.7 - 4.0", "pop": 5, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.0 - 65.6 - 51.0 - 36.3 - 11.3 (一杯)", "trainingComment": "鋭い末脚が武器。C.デムーロ騎手の手腕で中京の直線を切り裂く。", "trainingWeight": 524, "lastRaceWeight": 520, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "サンライズジパング", "sexAge": "牡4", "load": 57, "jockey": "武豊", "stable": "音無秀孝 (栗東)", "odds": "13.2", "placeOdds": "3.2 - 4.8", "pop": 6, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.8 - 38.0 - 24.6 - 12.1 (馬なり)", "trainingComment": "みやこS勝ち馬。3歳ダート戦線のトップホースが古馬の壁に挑む。", "trainingWeight": 510, "lastRaceWeight": 506, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 7, "horseName": "ハギノアレグリアス", "sexAge": "牡8", "load": 58, "jockey": "岩田望来", "stable": "四位洋文 (栗東)", "odds": "16.8", "placeOdds": "3.8 - 5.6", "pop": 7, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "83.2 - 66.8 - 51.8 - 37.0 - 11.6 (馬なり)", "trainingComment": "シリウスS連覇の実力派。ベテランの味を活かしてイン強襲。", "trainingWeight": 492, "lastRaceWeight": 490, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 8, "horseName": "ドゥラエレーデ", "sexAge": "牡5", "load": 58, "jockey": "北村友一", "stable": "池添学 (栗東)", "odds": "19.5", "placeOdds": "4.2 - 6.2", "pop": 8, "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "53.0 - 38.4 - 24.8 - 12.2 (強め)", "trainingComment": "2年連続チャンピオンズC3着のリピーター。この舞台での安定感抜群。", "trainingWeight": 516, "lastRaceWeight": 514, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 9, "horseName": "メイショウハリオ", "sexAge": "牡8", "load": 58, "jockey": "浜中俊", "stable": "岡田稲男 (栗東)", "odds": "24.0", "placeOdds": "5.0 - 7.5", "pop": 9, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "83.6 - 67.0 - 52.0 - 37.2 - 11.8 (馬なり)", "trainingComment": "帝王賞連覇の古豪。展開が向いた時の破壊力は健在。", "trainingWeight": 512, "lastRaceWeight": 508, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 10, "horseName": "ミックファイア", "sexAge": "牡5", "load": 58, "jockey": "矢野貴之", "stable": "渡邉和雄 (地方)", "odds": "29.0", "placeOdds": "6.0 - 9.0", "pop": 10, "trainingGrade": "B", "trainingCourse": "大井", "trainingTime": "65.8 - 51.0 - 37.2 - 12.0 (強め)", "trainingComment": "南関無敗3冠馬の意地。JRAダートG1奪取へ勝負気配。", "trainingWeight": 498, "lastRaceWeight": 494, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 11, "horseName": "ガイアフォース", "sexAge": "牡6", "load": 58, "jockey": "長岡禎仁", "stable": "杉山晴紀 (栗東)", "odds": "35.0", "placeOdds": "7.5 - 11.5", "pop": 11, "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "53.4 - 38.6 - 25.0 - 12.3 (馬なり)", "trainingComment": "フェブラリーS2着の二刀流。スピードを活かして好位追走。", "trainingWeight": 498, "lastRaceWeight": 496, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 12, "horseName": "ヤマニンウルス", "sexAge": "牡4", "load": 57, "jockey": "団野大成", "stable": "斉藤崇史 (栗東)", "odds": "42.0", "placeOdds": "8.5 - 13.0", "pop": 12, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.8 - 66.4 - 51.6 - 36.7 - 11.5 (強め)", "trainingComment": "無敗で重賞制覇した超新星。初のG1挑戦でどこまでやれるか。", "trainingWeight": 580, "lastRaceWeight": 576, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 13, "horseName": "アーテルアストレア", "sexAge": "牝6", "load": 56, "jockey": "菱田裕二", "stable": "橋口慎介 (栗東)", "odds": "54.0", "placeOdds": "11.0 - 17.0", "pop": 13, "trainingGrade": "B-", "trainingCourse": "栗東坂路", "trainingTime": "53.8 - 39.0 - 25.2 - 12.4 (馬なり)", "trainingComment": "紅一点。牡馬相手でも末脚を活かして掲示板を狙う。", "trainingWeight": 462, "lastRaceWeight": 458, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 14, "horseName": "スレイマン", "sexAge": "牡7", "load": 58, "jockey": "西村淳也", "stable": "池添学 (栗東)", "odds": "68.0", "placeOdds": "13.5 - 21.0", "pop": 14, "trainingGrade": "B-", "trainingCourse": "栗東CW", "trainingTime": "84.5 - 67.8 - 52.6 - 37.8 - 12.1 (強め)", "trainingComment": "好位差しを得意とする堅実派。前が崩れれば浮上。", "trainingWeight": 538, "lastRaceWeight": 534, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 15, "horseName": "テーオードレフォン", "sexAge": "牡6", "load": 58, "jockey": "丸山元気", "stable": "梅田智之 (栗東)", "odds": "82.0", "placeOdds": "16.0 - 25.0", "pop": 15, "trainingGrade": "C", "trainingCourse": "栗東坂路", "trainingTime": "54.2 - 39.5 - 25.6 - 12.6 (馬なり)", "trainingComment": "先行争いが鍵。マイペースに持ち込みたい。", "trainingWeight": 502, "lastRaceWeight": 498, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 16, "horseName": "グロリアムンディ", "sexAge": "牡7", "load": 58, "jockey": "戸崎圭太", "stable": "大久保龍志 (栗東)", "odds": "95.0", "placeOdds": "18.0 - 28.0", "pop": 16, "trainingGrade": "C", "trainingCourse": "栗東CW", "trainingTime": "85.2 - 68.5 - 53.2 - 38.2 - 12.4 (馬なり)", "trainingComment": "ベテランの経験。大外からロスなく立ち回れるか。", "trainingWeight": 514, "lastRaceWeight": 510, "confirmedWeight": None, "weightDiff": None}
]

r20_occult = [
  {"id": 1, "title": "🍋 絶対王者「レモンポップ」引退ラストラン有終サイン", "badge": "有終の美サイン", "source": "X・ダート考察トレンド", "content": "国内ダートで一度も連対を外したことがないレモンポップの引退レース。中京ダート1800mの最内1枠1番からハナを奪って逃げ切る黄金シナリオは競馬ファンの共通認識。黄色枠（5枠）とのレモン枠連サインも急浮上！", "targets": [{"gate": 1, "waku": 1, "name": "レモンポップ"}]},
  {"id": 2, "title": "🌪️ 中京ダート1800m「最内1枠・先行馬」絶対優勢バイアスの法則", "badge": "コースバイアス", "source": "データ競馬研究室", "content": "スタートから1コーナーまでの距離が短く、外枠が極端に不利とされる中京ダート1800m。1枠のレモンポップ＆ウィルソンテソーロの2頭がそのままワンツーフィニッシュする可能性が極めて高いトラックバイアスです。", "targets": [{"gate": 1, "waku": 1, "name": "レモンポップ"}, {"gate": 2, "waku": 1, "name": "ウィルソンテソーロ"}]}
]

entries_data['20'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r20_starters]
pred_data['races']['20'] = {
  "raceId": "20",
  "raceName": "第27回 チャンピオンズカップ",
  "date": "2026年12月6日(日) 15:40発走",
  "venue": "中京競馬場 ダート1800m",
  "starters": r20_starters,
  "occultSigns": r20_occult
}

# ----------------------------------------------------
# 21: 阪神ジュベナイルフィリーズ (2026.12.13 京都芝1600m)
# ----------------------------------------------------
r21_starters = [
  {"waku": 1, "gate": 1, "horseName": "ブラウンラチェット", "sexAge": "牝2", "load": 55, "jockey": "C.ルメール", "stable": "手塚貴久 (美浦)", "odds": "2.6", "placeOdds": "1.3 - 1.7", "pop": 1, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "82.2 - 66.0 - 51.0 - 36.4 - 11.2 (強め)", "trainingComment": "アルテミスS無傷連勝。兄フォーエバーヤング譲りの抜群の勝負根性。", "trainingWeight": 444, "lastRaceWeight": 440, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "カムニャック", "sexAge": "牝2", "load": 55, "jockey": "川田将雅", "stable": "友道康夫 (栗東)", "odds": "3.4", "placeOdds": "1.4 - 1.9", "pop": 2, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "81.0 - 65.2 - 50.4 - 35.8 - 11.0 (一杯)", "trainingComment": "新馬戦で規格外の末脚。大器の呼び声高く2歳女王へ最短距離。", "trainingWeight": 504, "lastRaceWeight": 500, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "コートアリシアン", "sexAge": "牝2", "load": 55, "jockey": "菅原明良", "stable": "伊藤大士 (美浦)", "odds": "5.8", "placeOdds": "1.8 - 2.6", "pop": 3, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "83.0 - 66.8 - 51.8 - 36.8 - 11.4 (馬なり)", "trainingComment": "新潟2歳S上位。切れ味は世代上位で外回り差し脚にピッタリ。", "trainingWeight": 456, "lastRaceWeight": 452, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "ミッキージュエリー", "sexAge": "牝2", "load": 55, "jockey": "坂井瑠星", "stable": "矢作芳人 (栗東)", "odds": "7.5", "placeOdds": "2.2 - 3.2", "pop": 4, "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "52.4 - 37.8 - 24.4 - 12.0 (強め)", "trainingComment": "矢作厩舎期待の牝馬。坂井瑠星の手綱で果敢に先行。", "trainingWeight": 468, "lastRaceWeight": 464, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "マイエレメント", "sexAge": "牝2", "load": 55, "jockey": "横山武史", "stable": "福永祐一 (栗東)", "odds": "9.8", "placeOdds": "2.6 - 3.8", "pop": 5, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.5 - 66.2 - 51.5 - 36.9 - 11.5 (馬なり)", "trainingComment": "福永厩舎の素質馬。気性も素直で京都芝マイルに対応可能。", "trainingWeight": 472, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "クウネル", "sexAge": "牝2", "load": 55, "jockey": "武豊", "stable": "中内田充正 (栗東)", "odds": "13.0", "placeOdds": "3.2 - 4.8", "pop": 6, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "83.2 - 66.8 - 52.0 - 37.2 - 11.6 (強め)", "trainingComment": "武豊騎手を背に軽快な走り。外回りの下り坂をスムーズに下れば。", "trainingWeight": 460, "lastRaceWeight": 456, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 7, "horseName": "ランフォーヴァウ", "sexAge": "牝2", "load": 55, "jockey": "団野大成", "stable": "福永祐一 (栗東)", "odds": "18.5", "placeOdds": "4.2 - 6.5", "pop": 7, "trainingGrade": "B", "trainingCourse": "栗東坂路", "trainingTime": "53.2 - 38.6 - 25.0 - 12.2 (馬なり)", "trainingComment": "デイリー杯2歳S勝ち馬。レースセンス高く立ち回り上手。", "trainingWeight": 464, "lastRaceWeight": 460, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 8, "horseName": "カレンラップスター", "sexAge": "牝2", "load": 55, "jockey": "松山弘平", "stable": "安田翔伍 (栗東)", "odds": "24.0", "placeOdds": "5.2 - 8.0", "pop": 8, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "84.0 - 67.5 - 52.4 - 37.5 - 11.8 (馬なり)", "trainingComment": "追ってからの伸び脚確実。ハイペースなら上位進出。", "trainingWeight": 450, "lastRaceWeight": 446, "confirmedWeight": None, "weightDiff": None}
]

r21_occult = [
  {"id": 1, "title": "💎 フォーエバーヤング半妹「ブラウンラチェット」兄妹G1制覇サイン", "badge": "世界血統サイン", "source": "X・血統考察トレンド", "content": "世界を股にかけて大活躍するフォーエバーヤングの半妹ブラウンラチェット。ルメール騎手を背に無敗でアルテミスSを制した勝負強さは本物。偉大なる兄に続く兄妹同一年G1制覇の強力サインが発動！", "targets": [{"gate": 1, "waku": 1, "name": "ブラウンラチェット"}]},
  {"id": 2, "title": "🌸 京都外回り代替開催に伴う「外枠差し脚」連動サイン", "badge": "京都マイルの法則", "source": "コース傾向班", "content": "阪神競馬場改修により京都芝1600m外回りで施行される今年の阪神JF。3コーナーの坂を下ってからの直線平坦コースは、中団から末脚を伸ばす差し馬が連対独占するパターン。", "targets": [{"gate": 2, "waku": 1, "name": "カムニャック"}, {"gate": 3, "waku": 2, "name": "コートアリシアン"}]}
]

entries_data['21'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r21_starters]
pred_data['races']['21'] = {
  "raceId": "21",
  "raceName": "第78回 阪神ジュベナイルフィリーズ",
  "date": "2026年12月13日(日) 15:40発走",
  "venue": "京都競馬場 芝1600m (外回り)",
  "starters": r21_starters,
  "occultSigns": r21_occult
}

# ----------------------------------------------------
# 22: 朝日杯フューチュリティステークス (2026.12.20 京都芝1600m)
# ----------------------------------------------------
r22_starters = [
  {"waku": 1, "gate": 1, "horseName": "クロワデュノール", "sexAge": "牡2", "load": 56, "jockey": "北村友一", "stable": "斉藤崇史 (栗東)", "odds": "2.4", "placeOdds": "1.2 - 1.6", "pop": 1, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "80.6 - 64.8 - 50.2 - 35.6 - 11.0 (強め)", "trainingComment": "東スポ杯2歳S圧勝の怪物。キタサンブラック産駒らしい雄大な馬体と驚異の推進力。", "trainingWeight": 512, "lastRaceWeight": 508, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "パンジャタワー", "sexAge": "牡2", "load": 56, "jockey": "松山弘平", "stable": "橋口慎介 (栗東)", "odds": "3.8", "placeOdds": "1.5 - 2.1", "pop": 2, "trainingGrade": "S", "trainingCourse": "栗東坂路", "trainingTime": "51.6 - 37.2 - 24.0 - 11.8 (馬なり)", "trainingComment": "京王杯2歳S覇者。坂路で異次元のスピードを披露しマイル克服に自信。", "trainingWeight": 482, "lastRaceWeight": 478, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "アルテヴェローチェ", "sexAge": "牡2", "load": 56, "jockey": "武豊", "stable": "須貝尚介 (栗東)", "odds": "5.2", "placeOdds": "1.7 - 2.5", "pop": 3, "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "82.0 - 65.8 - 50.8 - 36.2 - 11.2 (馬なり)", "trainingComment": "サウジアラビアRCを鮮やかに制覇。レジェンド武豊との黄金タッグで戴冠へ。", "trainingWeight": 496, "lastRaceWeight": 492, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "サトノカルナバル", "sexAge": "牡2", "load": 56, "jockey": "佐々木大輔", "stable": "堀宣行 (美浦)", "odds": "7.8", "placeOdds": "2.2 - 3.4", "pop": 4, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "82.8 - 66.4 - 51.4 - 36.6 - 11.3 (強め)", "trainingComment": "函館2歳S勝ち馬。堀厩舎の綿密な仕上げでマイルにも対応可能。", "trainingWeight": 490, "lastRaceWeight": 486, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "エイシンワンド", "sexAge": "牡2", "load": 56, "jockey": "幸英明", "stable": "大久保龍志 (栗東)", "odds": "11.5", "placeOdds": "2.8 - 4.2", "pop": 5, "trainingGrade": "B+", "trainingCourse": "栗東坂路", "trainingTime": "52.8 - 38.2 - 24.6 - 12.0 (馬なり)", "trainingComment": "小倉2歳S勝ち馬。持ち前のスピードでハナを奪い粘り込みを図る。", "trainingWeight": 476, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "タイセイカレント", "sexAge": "牡2", "load": 56, "jockey": "横山武史", "stable": "矢作芳人 (栗東)", "odds": "15.0", "placeOdds": "3.5 - 5.2", "pop": 6, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "83.0 - 66.8 - 51.8 - 37.0 - 11.5 (強め)", "trainingComment": "矢作厩舎の勝負気配。混戦になれば勝負根性で上位へ食い込む。", "trainingWeight": 486, "lastRaceWeight": 482, "confirmedWeight": None, "weightDiff": None}
]

r22_occult = [
  {"id": 1, "title": "⚡ キタサンブラック後継「クロワデュノール」無敗戴冠の星", "badge": "新怪物伝説", "source": "X・血統トレンド", "content": "キタサンブラックの代表産駒としてクラシック最有力と謳われるクロワデュノール。東スポ杯で見せた異次元の瞬発力は2歳馬の域を超越。白枠1番からの戴冠劇が濃厚とSNSで大本命サイン！", "targets": [{"gate": 1, "waku": 1, "name": "クロワデュノール"}]},
  {"id": 2, "title": "👑 須貝厩舎×武豊「アルテヴェローチェ」2歳マイル王の系譜", "badge": "師弟コンビ", "source": "競馬サイン研究会", "content": "かつてのソダシやドルチェモアなど2歳重賞で無類の強さを誇る須貝厩舎。武豊騎手とのコンビで挑むマイル頂上決戦には、暮れの京都を締めくくる勝負気配が漂っています。", "targets": [{"gate": 3, "waku": 2, "name": "アルテヴェローチェ"}]}
]

entries_data['22'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r22_starters]
pred_data['races']['22'] = {
  "raceId": "22",
  "raceName": "第78回 朝日杯フューチュリティステークス",
  "date": "2026年12月20日(日) 15:40発走",
  "venue": "京都競馬場 芝1600m (外回り)",
  "starters": r22_starters,
  "occultSigns": r22_occult
}

# ----------------------------------------------------
# 23: ホープフルステークス (2026.12.26 中山芝2000m)
# ----------------------------------------------------
r23_starters = [
  {"waku": 1, "gate": 1, "horseName": "マスカレードボール", "sexAge": "牡2", "load": 56, "jockey": "戸崎圭太", "stable": "手塚貴久 (美浦)", "odds": "2.8", "placeOdds": "1.3 - 1.8", "pop": 1, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "81.8 - 65.6 - 50.8 - 36.2 - 11.1 (馬なり)", "trainingComment": "アイビーSで非凡な瞬発力を証明。中山芝2000mクラシック登竜門で主役。", "trainingWeight": 494, "lastRaceWeight": 490, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "ファイアンクランツ", "sexAge": "牡2", "load": 56, "jockey": "菅原明良", "stable": "堀宣行 (美浦)", "odds": "4.2", "placeOdds": "1.5 - 2.2", "pop": 2, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "82.6 - 66.2 - 51.4 - 36.6 - 11.3 (強め)", "trainingComment": "札幌2歳S上位。タフな中山の急坂でもしっかりと脚を伸ばせるパワー。", "trainingWeight": 486, "lastRaceWeight": 482, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "アスクシュタイン", "sexAge": "牡2", "load": 56, "jockey": "川田将雅", "stable": "藤原英昭 (栗東)", "odds": "5.6", "placeOdds": "1.8 - 2.6", "pop": 3, "trainingGrade": "A", "trainingCourse": "栗東CW", "trainingTime": "82.2 - 66.0 - 51.2 - 36.5 - 11.2 (馬なり)", "trainingComment": "先行力抜群。川田騎手が好位で立ち回れば粘り込み濃厚。", "trainingWeight": 476, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "ピコチャンブラック", "sexAge": "牡2", "load": 56, "jockey": "石川裕紀人", "stable": "上原佑紀 (美浦)", "odds": "7.5", "placeOdds": "2.2 - 3.4", "pop": 4, "trainingGrade": "B+", "trainingCourse": "美浦W", "trainingTime": "83.2 - 66.8 - 51.8 - 36.8 - 11.5 (強め)", "trainingComment": "新馬戦圧勝。キタサンブラック産駒のスケール感で上位進出を伺う。", "trainingWeight": 508, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "パープルレディ", "sexAge": "牡2", "load": 56, "jockey": "C.ルメール", "stable": "木村哲也 (美浦)", "odds": "10.0", "placeOdds": "2.6 - 4.0", "pop": 5, "trainingGrade": "B+", "trainingCourse": "美浦W", "trainingTime": "83.5 - 67.0 - 52.0 - 37.0 - 11.6 (馬なり)", "trainingComment": "ルメール騎手鞍上で勝負気配。中山の内回りを器用に立ち回る。", "trainingWeight": 470, "lastRaceWeight": 466, "confirmedWeight": None, "weightDiff": None}
]

r23_occult = [
  {"id": 1, "title": "🏛️ 有馬前日の中山芝2000m「手塚厩舎×クラシック」戴冠サイン", "badge": "中山直結サイン", "source": "X・2歳馬ウォッチャー", "content": "かつてソールオリエンスなど中山2000mで大仕事をやってのける手塚厩舎。マスカレードボールが年末のホープフルSを制し、翌年の皐月賞へ王手をかける黄金ローテが早くもXで話題騒然！", "targets": [{"gate": 1, "waku": 1, "name": "マスカレードボール"}]}
]

entries_data['23'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r23_starters]
pred_data['races']['23'] = {
  "raceId": "23",
  "raceName": "第43回 ホープフルステークス",
  "date": "2026年12月26日(土) 15:40発走",
  "venue": "中山競馬場 芝2000m",
  "starters": r23_starters,
  "occultSigns": r23_occult
}

# ----------------------------------------------------
# 24: 有馬記念 (2026.12.27 中山芝2500m) - グランプリ総決算
# ----------------------------------------------------
r24_starters = [
  {"waku": 1, "gate": 1, "horseName": "ドウデュース", "sexAge": "牡6", "load": 58, "jockey": "武豊", "stable": "友道康夫 (栗東)", "odds": "2.5", "placeOdds": "1.2 - 1.6", "pop": 1, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "79.2 - 63.8 - 49.5 - 35.0 - 10.8 (馬なり)", "trainingComment": "日本競馬の英雄、伝説のラストラン。中山2500mで有終の美を飾るため研ぎ澄まされた極上の仕上がり。", "trainingWeight": 506, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None},
  {"waku": 1, "gate": 2, "horseName": "ダノンデサイル", "sexAge": "牡5", "load": 58, "jockey": "戸崎圭太", "stable": "安田翔伍 (栗東)", "odds": "3.6", "placeOdds": "1.4 - 2.0", "pop": 2, "trainingGrade": "S", "trainingCourse": "栗東CW", "trainingTime": "80.5 - 64.6 - 50.0 - 35.5 - 11.0 (強め)", "trainingComment": "天皇賞秋覇者。ダービー馬の風格漂い、中山2500mでも先行からの鋭い抜け出しで頂点狙う。", "trainingWeight": 518, "lastRaceWeight": 516, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 3, "horseName": "レガレイラ", "sexAge": "牝5", "load": 56, "jockey": "C.ルメール", "stable": "木村哲也 (美浦)", "odds": "4.8", "placeOdds": "1.6 - 2.4", "pop": 3, "trainingGrade": "S", "trainingCourse": "美浦W", "trainingTime": "81.4 - 65.2 - 50.6 - 36.0 - 11.1 (馬なり)", "trainingComment": "ホープフルSを制した中山芝中距離は最高の適性。ルメール騎手との再コンビで大波乱を演出。", "trainingWeight": 494, "lastRaceWeight": 494, "confirmedWeight": None, "weightDiff": None},
  {"waku": 2, "gate": 4, "horseName": "アーバンシック", "sexAge": "牡4", "load": 57, "jockey": "横山武史", "stable": "武井亮 (美浦)", "odds": "6.2", "placeOdds": "2.0 - 2.9", "pop": 4, "trainingGrade": "A", "trainingCourse": "美浦W", "trainingTime": "82.0 - 65.8 - 51.0 - 36.3 - 11.2 (強め)", "trainingComment": "菊花賞圧勝の長距離適性。中山外回りから内回りへの勝負所でロングスパートを仕掛ける。", "trainingWeight": 512, "lastRaceWeight": 510, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 5, "horseName": "ブローザホーン", "sexAge": "牡6", "load": 58, "jockey": "菅原明良", "stable": "吉岡辰弥 (栗東)", "odds": "8.5", "placeOdds": "2.4 - 3.6", "pop": 5, "trainingGrade": "A", "trainingCourse": "栗東坂路", "trainingTime": "52.8 - 38.0 - 24.5 - 12.0 (一杯)", "trainingComment": "宝塚記念覇者。タフな冬の中山2500mはスタミナ満点のこの馬に絶好の舞台。", "trainingWeight": 432, "lastRaceWeight": 428, "confirmedWeight": None, "weightDiff": None},
  {"waku": 3, "gate": 6, "horseName": "ジャスティンパレス", "sexAge": "牡6", "load": 58, "jockey": "坂井瑠星", "stable": "杉山晴紀 (栗東)", "odds": "10.5", "placeOdds": "2.8 - 4.2", "pop": 6, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.5 - 66.2 - 51.5 - 36.8 - 11.4 (馬なり)", "trainingComment": "有単記念リピーター。坂井瑠星の積極騎乗で直線しぶとく食い下がる。", "trainingWeight": 474, "lastRaceWeight": 472, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 7, "horseName": "スターズオンアース", "sexAge": "牝6", "load": 56, "jockey": "川田将雅", "stable": "高柳瑞樹 (美浦)", "odds": "13.0", "placeOdds": "3.2 - 4.8", "pop": 7, "trainingGrade": "B+", "trainingCourse": "美浦W", "trainingTime": "83.0 - 66.5 - 51.8 - 36.9 - 11.5 (強め)", "trainingComment": "前年有馬記念2着。大外枠から激走した実績があり、中山適性に死角なし。", "trainingWeight": 498, "lastRaceWeight": 496, "confirmedWeight": None, "weightDiff": None},
  {"waku": 4, "gate": 8, "horseName": "ソールオリエンス", "sexAge": "牡5", "load": 58, "jockey": "松山弘平", "stable": "手塚貴久 (美浦)", "odds": "16.5", "placeOdds": "3.8 - 5.6", "pop": 8, "trainingGrade": "B+", "trainingCourse": "美浦W", "trainingTime": "83.2 - 66.8 - 52.0 - 37.0 - 11.6 (馬なり)", "trainingComment": "皐月賞馬の中山適性。冬のタフな馬場は大歓迎で一撃を秘める。", "trainingWeight": 470, "lastRaceWeight": 468, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 9, "horseName": "ベラジオオペラ", "sexAge": "牡5", "load": 58, "jockey": "横山和生", "stable": "上村洋行 (栗東)", "odds": "20.0", "placeOdds": "4.5 - 6.8", "pop": 9, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "83.5 - 67.0 - 52.2 - 37.2 - 11.7 (強め)", "trainingComment": "大阪杯覇者の先行力。インコースに潜り込んでロスなく立ち回れば。", "trainingWeight": 506, "lastRaceWeight": 504, "confirmedWeight": None, "weightDiff": None},
  {"waku": 5, "gate": 10, "horseName": "ネブラディスク", "sexAge": "牡4", "load": 57, "jockey": "岩田望来", "stable": "福永祐一 (栗東)", "odds": "24.0", "placeOdds": "5.2 - 8.0", "pop": 10, "trainingGrade": "B+", "trainingCourse": "栗東CW", "trainingTime": "82.8 - 66.4 - 51.6 - 36.8 - 11.4 (馬なり)", "trainingComment": "天皇賞秋2着の激走馬。福永厩舎の秘蔵っ子が中山グランプリでも波乱を巻き起こす。", "trainingWeight": 460, "lastRaceWeight": 458, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 11, "horseName": "メイショウタバル", "sexAge": "牡4", "load": 57, "jockey": "浜中俊", "stable": "石橋守 (栗東)", "odds": "32.0", "placeOdds": "7.0 - 11.0", "pop": 11, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "81.5 - 65.0 - 50.8 - 36.5 - 11.8 (一杯)", "trainingComment": "大逃げ宣言。中山2500mをハイペースで引っ張り場内を沸かせる。", "trainingWeight": 504, "lastRaceWeight": 500, "confirmedWeight": None, "weightDiff": None},
  {"waku": 6, "gate": 12, "horseName": "ヘデントール", "sexAge": "牡4", "load": 57, "jockey": "佐々木大輔", "stable": "木村哲也 (美浦)", "odds": "38.0", "placeOdds": "8.0 - 12.5", "pop": 12, "trainingGrade": "B", "trainingCourse": "美浦W", "trainingTime": "84.0 - 67.5 - 52.5 - 37.4 - 11.9 (強め)", "trainingComment": "菊花賞2着馬。スタミナ勝負は望むところで直線しぶとく迫る。", "trainingWeight": 490, "lastRaceWeight": 486, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 13, "horseName": "ディープボンド", "sexAge": "牡8", "load": 58, "jockey": "幸英明", "stable": "大久保龍志 (栗東)", "odds": "48.0", "placeOdds": "10.0 - 16.0", "pop": 13, "trainingGrade": "B", "trainingCourse": "栗東CW", "trainingTime": "84.2 - 67.8 - 52.8 - 37.6 - 12.0 (馬なり)", "trainingComment": "有馬記念4年連続出走。不屈の魂で今年も中山を全力疾走。", "trainingWeight": 514, "lastRaceWeight": 512, "confirmedWeight": None, "weightDiff": None},
  {"waku": 7, "gate": 14, "horseName": "アドマイヤテラ", "sexAge": "牡4", "load": 57, "jockey": "津村明秀", "stable": "友道康夫 (栗東)", "odds": "58.0", "placeOdds": "12.0 - 18.5", "pop": 14, "trainingGrade": "B-", "trainingCourse": "栗東CW", "trainingTime": "84.6 - 68.0 - 53.0 - 37.8 - 12.1 (馬なり)", "trainingComment": "菊花賞3着。友道厩舎の長距離砲として上位進出を伺う。", "trainingWeight": 478, "lastRaceWeight": 474, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 15, "horseName": "タガノデュード", "sexAge": "牡5", "load": 58, "jockey": "M.デムーロ", "stable": "宮徹 (栗東)", "odds": "68.0", "placeOdds": "14.0 - 22.0", "pop": 15, "trainingGrade": "B-", "trainingCourse": "栗東坂路", "trainingTime": "53.8 - 39.0 - 25.4 - 12.4 (強め)", "trainingComment": "天皇賞秋4着の実力派。ミルコ騎手の大胆な捲り一発に警戒。", "trainingWeight": 500, "lastRaceWeight": 498, "confirmedWeight": None, "weightDiff": None},
  {"waku": 8, "gate": 16, "horseName": "シンエンペラー", "sexAge": "牡4", "load": 57, "jockey": "坂井瑠星", "stable": "矢作芳人 (栗東)", "odds": "75.0", "placeOdds": "15.0 - 24.0", "pop": 16, "trainingGrade": "B-", "trainingCourse": "栗東坂路", "trainingTime": "54.0 - 39.2 - 25.5 - 12.5 (馬なり)", "trainingComment": "凱旋門賞・ジャパンCからの連戦。世界の強敵と戦った底力。", "trainingWeight": 486, "lastRaceWeight": 485, "confirmedWeight": None, "weightDiff": None}
]

r24_occult = [
  {"id": 1, "title": "🐴 レジェンド武豊×ドウデュース「ラストラン有馬記念」奇跡の再現サイン", "badge": "有終の伝説", "source": "X・日本全国トレンド1位", "content": "かつてのオグリキャップ、ディープインパクト、キタサンブラックの有終の美。そして今年、希代の名馬ドウデュースが武豊騎手と共にグランプリ有馬記念で現役生活にピリオドを打つ。競馬史に残る白帽子1番からの奇跡のラストランサインが点灯中！", "targets": [{"gate": 1, "waku": 1, "name": "ドウデュース"}]},
  {"id": 2, "title": "👑 天皇賞（秋）覇者「ダノンデサイル」vs 菊花賞馬「アーバンシック」頂上決戦", "badge": "世代頂上決戦", "source": "競馬データ班", "content": "ダービーと天皇賞秋を完勝したダノンデサイルと、圧倒的スタミナで菊花賞を制したアーバンシック。古馬VS3歳の最強激突は過去オルフェーヴルやエフフォーリアが勝利した黄金パターン。", "targets": [{"gate": 2, "waku": 1, "name": "ダノンデサイル"}, {"gate": 4, "waku": 2, "name": "アーバンシック"}]},
  {"id": 3, "title": "🎄 12/27開催「クリスマス有馬」と「白枠1枠・赤枠3枠」連動の法則", "badge": "世相サイン", "source": "オカルト競馬倶楽部", "content": "年の瀬の有馬記念といえば世相サイン。クリスマスカラーの『白（1枠）』と『赤（3枠）』の組み合わせは過去のクリスマス有馬で何度も超高配当を生み出した鉄板の法則！", "targets": [{"gate": 1, "waku": 1, "name": "ドウデュース"}, {"gate": 5, "waku": 3, "name": "ブローザホーン"}]}
]

entries_data['24'] = [{k: s[k] for k in ['waku', 'gate', 'horseName', 'sexAge', 'load', 'jockey', 'stable']} for s in r24_starters]
pred_data['races']['24'] = {
  "raceId": "24",
  "raceName": "第71回 有馬記念",
  "date": "2026年12月27日(日) 15:40発走",
  "venue": "中山競馬場 芝2500m",
  "starters": r24_starters,
  "occultSigns": r24_occult
}

# Save entries_data.json & entries_data.js
with open(entries_json_path, 'w', encoding='utf-8') as f:
    json.dump(entries_data, f, ensure_ascii=False, indent=2)

with open(entries_js_path, 'w', encoding='utf-8') as f:
    f.write("export const ENTRIES_DATA = " + json.dumps(entries_data, ensure_ascii=False, indent=2) + ";\n")

print(f"Updated entries_data.json and .js with all autumn races 16 to 24! Keys: {list(entries_data.keys())}")

# Save prediction_data.json & prediction_data.js
with open(pred_json_path, 'w', encoding='utf-8') as f:
    json.dump(pred_data, f, ensure_ascii=False, indent=2)

with open(pred_js_path, 'w', encoding='utf-8') as f:
    f.write("export const PREDICTION_DATA = " + json.dumps(pred_data, ensure_ascii=False, indent=2) + ";\n")

print(f"Updated prediction_data.json and .js with all autumn races! Pred keys: {list(pred_data['races'].keys())}")
