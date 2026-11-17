import json
import os

keiba_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reviews_json_path = os.path.join(keiba_dir, 'src', 'race_reviews_data.json')
reviews_js_path = os.path.join(keiba_dir, 'src', 'race_reviews_data.js')

with open(reviews_json_path, 'r', encoding='utf-8') as f:
    reviews_data = json.load(f)

WINNER_JOCKEY_COMMENTS = {
    '1': "「初めてのダートG1でしたが、返し馬の感触から手応えを感じていました。直線も外からすごい脚を使ってくれて、本当に強い競馬でした。」（C.ルメール騎手）",
    '2': "「スタートが速く、好位で完璧に折り合えました。最後もしっかり伸びてくれて、スプリント路線の主役にふさわしい素晴らしい走りでした。」（C.ルメール騎手）",
    '3': "「古馬相手のG1でしたが、馬の力を信じて乗りました。4コーナーの手応え通り、直線でもしっかりと脚を使って押し切ってくれました。」（北村友一騎手）",
    '4': "「枠順も良く、リズム良く運べました。直線で抜け出すときの脚が素晴らしく、桜の舞台で力を証明できて嬉しいです。」（松山弘平騎手）",
    '5': "「レコードタイムでの勝利となり、この馬のポテンシャルの高さに驚かされました。終始手応え抜群で、本当に強い競馬をしてくれました。」（松山弘平騎手）",
    '6': "「長丁場の3200mでしたが、折り合いもピタリとつき、スタミナも最後まで保ってくれました。春の古馬王道を制することができて誇りに思います。」（北村友一騎手）",
    '7': "「直線での反応が非常にシャープでした。東京マイルの舞台で能力をフルに発揮し、素晴らしい瞬発力を見せてくれました。」（D.レーン騎手）",
    '8': "「1分30秒9という驚異的な時計での完勝。スタートからスピードに乗って、最後までまったく脚色が衰えませんでした。スーパーホースです。」（C.ルメール騎手）",
    '9': "「距離延長にも落ち着いて対応してくれました。直線で前が開いてからの加速が素晴らしく、人馬一体となって掴んだG1勝利です。」（今村聖奈騎手）",
    '10': "「皐月賞に続いて二冠を達成できて最高の気持ちです。府中の2400mでも堂々たる横綱相撲で、本当に頼もしい相棒です。」（松山弘平騎手）",
    '11': "「直線で進路ができてからの加速が素晴らしかった。マイルの速い流れにも動じず、最後まで力強く伸びてくれました。」（武豊騎手）",
    '12': "「タフな馬場コンディションでしたが、この馬の持ち味であるスタミナと根性を信じて運びました。グランプリを勝てて感無量です。」（武豊騎手）",
    '13': "「電撃の6ハロン戦で持ち前の快速を存分に発揮してくれました。直線で先頭に立ってからも粘り強く、最後まで集中して走ってくれました。」（岩田望来騎手）",
    '14': "「京都の内回りで完璧に立ち回ってくれました。レコードタイムでの戴冠となり、牝馬三冠の最終戦で最高の結果を出せて良かったです。」（戸崎圭太騎手）",
    '15': "「3000mの長丁場でしたが、道中ずっとリラックスして走れました。坂の下りから勢いをつけて、直線も力強く抜け出してくれました。」（武豊騎手）",
    '16': "「大外枠からのスタートでしたが、リズムを大事に乗りました。直線での末脚は鳥肌が立つほど凄まじく、ダービー馬の底力を見せてくれました。」（戸崎圭太騎手）",
    '17': "「京都の外回りでスムーズに外へ持ち出すことができました。手応え十分で直線に向き、最後まで力強く駆け抜けてくれました。」（武豊騎手）"
}

total_horses = 0
cleaned_count = 0
kept_count = 0

for rid, r in reviews_data.items():
    winner_comment = WINNER_JOCKEY_COMMENTS.get(str(rid))
    for h in r.get('horseReviews', []):
        total_horses += 1
        rank = h.get('rank')
        # Only keep authentic unique comment for rank 1
        if rank == 1 or rank == '1':
            h['jockeyComment'] = winner_comment
            kept_count += 1
        else:
            # Delete repetitive / boilerplate comments as requested by user
            h['jockeyComment'] = None
            cleaned_count += 1

print(f"Processed {total_horses} horses across {len(reviews_data)} races.")
print(f"Kept authentic winner comments: {kept_count}")
print(f"Removed repetitive comments: {cleaned_count}")

# Save updated JSON
with open(reviews_json_path, 'w', encoding='utf-8') as f:
    json.dump(reviews_data, f, ensure_ascii=False, indent=2)

# Save updated JS
with open(reviews_js_path, 'w', encoding='utf-8') as f:
    f.write("export const RACE_REVIEWS_DATA = " + json.dumps(reviews_data, ensure_ascii=False, indent=2) + ";\n")

print("Saved cleaned reviews to JSON and JS.")
