# 平均フォント — 229書体のピクセル平均

日本語オープンライセンス書体 **229書体** のグリフをビットマップ描画して
ピクセル平均した「平均フォント」（v2。v1は100書体、旧TTFは `AverageFont-Regular-v1-100fonts.ttf` に保存）。
**v3（2026-11-06）**: 漢字を常用漢字2136字フルセットに拡張し全2290字、
見えづらい漢字のための適応しきい値つき。TTF は
`AverageFont-Regular-v3-229fonts-2290chars.ttf`。v2 の `AverageFont-Regular.ttf` は残してある。
**v4（2026-11-07）**: 漢字を JIS X 0213 全10050字（第1〜第4水準）に拡張し、
濁点つき仮名・小さい仮名・長音記号・繰り返し記号・句読点・記号も追加して全10305字。
TTF は `AverageFont-Regular-v4-229fonts-10305chars.ttf`。v2・v3 の TTF も残してある。
**v5（2026-11-08）**: 文字セットを「229書体のうち20書体以上がグリフを持つ可視文字」
（proper20）で定義し直し、半角句読点・全角英数字・ギリシア・キリル・ラテン拡張・
矢印・数学記号・囲み文字・JIS X 0212漢字・CJK拡張の一部まで入れて全18414字。
TTF は `AverageFont-Regular-v5-229fonts-18414chars.ttf`（7.5MB）。v2・v3・v4 の TTF も残してある。
`AverageFont-Regular.ttf` は v4 のまま（v5への差し替えは未実施）。

## 成果物

| ファイル | 内容 |
|---|---|
| `AverageFont-Regular-v5-229fonts-18414chars.ttf` | **v5**: 平均グリフをベクター化したTTF（18414字＋スペース）。インストールして使える |
| `out/viewer_v5.html` | v5の文字ごとの平均グリフを並べたビューワー（ブラウザで開く） |
| `out/glyphs_v5/*.png` | v5の平均グリフ18414枚（256×256px、グレースケール） |
| `out/contact_sheet_v5.png` | v5全18414字のコンタクトシート |
| `out/contact_sheet_v5_*.png` | v5グループ別コンタクトシート（漢字は水準別＋JIS X 0212・CJK拡張別） |
| `out/faint_before_after_v5.png` | 見えづらい漢字24字の調整前後比較（平均PNG｜固定128二値化｜適応しきい値二値化） |
| `out/fewest_before_after_v5.png` | 寄与書体が最も少ない24字の前後比較（寄与20書体の字中心） |
| `out/ttf_test_v5.png` | v5のTTFで実際に組版したテスト画像（半角英文・全角・ギリシア・キリル・JIS X 0212漢字・囲み・矢印・数学記号・拡張Bの文つき） |
| `out/stats_v5.json` | v5の各文字の寄与書体数・平均インク最大値・しきい値・JIS水準・人名用漢字フラグなどの集計 |
| `work/v5_proper_sets.json` | v5の文字セット定義（proper20: 18414字、proper50: 17692字） |
| `work/jisx0212_chars.json` | JIS X 0212 文字一覧（全6067字） |
| `AverageFont-Regular-v4-229fonts-10305chars.ttf` | **v4**: 平均グリフをベクター化したTTF（10305字＋スペース）。インストールして使える |
| `out/viewer_v4.html` | v4の文字ごとの平均グリフを並べたビューワー（ブラウザで開く） |
| `out/glyphs_v4/*.png` | v4の平均グリフ10305枚（256×256px、グレースケール） |
| `out/contact_sheet_v4.png` | v4全10305字のコンタクトシート |
| `out/contact_sheet_v4_*.png` | v4グループ別コンタクトシート（ひらがな／カタカナ／句読点／数字／英字／漢字は水準別） |
| `out/faint_before_after_v4.png` | 見えづらい漢字24字の調整前後比較（平均PNG｜固定128二値化｜適応しきい値二値化） |
| `out/fewest_before_after_v4.png` | 寄与書体が最も少ない24字の前後比較（第3・第4水準のレア漢字中心） |
| `out/ttf_test_v4.png` | v4のTTFで実際に組版したテスト画像（「じ」「太陽」「重要」など追加字の文つき） |
| `out/stats_v4.json` | v4の各文字の寄与書体数・平均インク最大値・しきい値・JIS水準・人名用漢字フラグなどの集計 |
| `work/jisx0213_kanji.txt` / `work/jisx0213_kanji.json` | JIS X 0213 漢字一覧（全10050字、水準別） |
| `work/jinmeiyo_kanji.txt` | 人名用漢字一覧（（一）634字種＋（二）212字種＝846字種、2026年6月現在864字体） |
| `AverageFont-Regular-v3-229fonts-2290chars.ttf` | **v3**: 平均グリフをベクター化したTTF（2290字＋スペース）。インストールして使える |
| `AverageFont-Regular.ttf` | v2のTTF（174字＋スペース）。残してある |
| `out/viewer_v3.html` | v3の文字ごとの平均グリフを並べたビューワー（ブラウザで開く） |
| `out/glyphs_v3/*.png` | v3の平均グリフ2290枚（256×256px、グレースケール） |
| `out/contact_sheet_v3.png` | v3全2290字のコンタクトシート |
| `out/contact_sheet_v3_*.png` | v3グループ別コンタクトシート（ひらがな／カタカナ／数字／英字／漢字） |
| `out/faint_before_after_v3.png` | 見えづらい漢字24字の調整前後比較（平均PNG｜固定128二値化｜適応しきい値二値化） |
| `out/ttf_test_v3.png` | v3のTTFで実際に組版したテスト画像（見えづらい漢字24字の行つき） |
| `out/stats_v3.json` | v3の各文字の寄与書体数・平均インク最大値・しきい値などの集計 |
| `out/viewer.html` | v2のビューワー（以下 v2の成果物） |
| `out/glyphs/*.png` | v2の平均グリフ174枚（256×256px、グレースケール） |
| `out/contact_sheet.png` | v2全174字のコンタクトシート |
| `out/contact_sheet_*.png` | v2グループ別コンタクトシート（ひらがな／カタカナ／数字／英字／漢字） |
| `out/ttf_test.png` | v2のTTFで実際に組版したテスト画像 |
| `out/stats.json` | v2の各文字の寄与書体数などの集計 |
| `SOURCES.md` | 元書体229書体の出所URL・ライセンス一覧 |
| `fonts/` | 元フォント190ファイル・約1.1GB（可変フォント5ファイルをウェイト展開して229書体分） |
| `work/` | 再現用スクリプト（ダウンロード／平均化／シート／TTF化） |

## 手法

1. **収集**: v1は Google Fonts の `google/fonts` リポジトリから OFL の日本語フォントを
   ダウンロード（`work/download_fonts.py`）。v2（2026-11-05）は google/fonts 未収録の
   ディスプレイ系・ドット系・レトロ系（Dela Gothic One、Rampart One、Zen Dots、だるまドロップなど）と、
   Source Han Sans/Serif JP、IPAex、Takao、VLゴシック、MigMix、Migu、UmePlus、
   Koruri、HackGen、UDEV Gothic、Moralerspace、PlemolJP、Cica、源柔ゴシック、源真ゴシック、
   源流明朝を追加（`work/download_fonts_v2.py`）。可変フォントは1ファイルから
   複数ウェイトを描画し、ウェイト違いを別書体として数えた（内訳は下記）。
2. **描画**: 各書体で対象文字を 256×256px のグレースケール画像に描画
   （フォントサイズ 200px、文字をキャンバス中央に配置 `anchor="mm"`）。
   可変フォントは Pillow の `set_variation_by_axes` でウェイトを指定。
3. **平均**: 文字ごとに、全書体の画素値を合計して寄与書体数で割った。
   欠けているグリフがある書体はその文字の平均から除外する設計。
   v2では **かな・英数字は229書体、漢字は227書体が寄与**（だるまドロップは漢字なし、
   Zen Dotsはかな・漢字なしのため、その文字の平均からは除外）。
   平均画像は `255 - 平均インク量` で白地に黒字として保存。
4. **TTF化**: 平均ビットマップを二値化し、OpenCV の輪郭抽出
   （`RETR_CCOMP`、穴も保持）＋ `approxPolyDP` で多角形化して、
   fontTools で TTF のグリフ（直線セグメントのみ）として書き込んだ。
   テンプレートは DotGothic16（表組みのみ流用、アウトラインは全て平均由来）。
   ベースラインはグループごとにシフトで調整（下記「制限」参照）。
   v2は固定しきい値（インク量50% = 128）だったが、**v3はグリフごとの
   適応しきい値**（`しきい値 = 0.40 × そのグリフの平均インク最大値`、
   8〜128にクランプ）に変更。理由と効果は下記「v3 で変わったこと」を参照。

## 文字セット（v5: 18414字）

- 定義（proper20）: 全Unicodeのうち、Unicodeカテゴリが Cc/Cf/Cs/Co/Cn/Zl/Zp/Zs/
  Mn/Me/Mc でない可視文字で、229書体（ウェイト展開込み）のうち20書体以上が
  グリフを持つもの。リストは `work/v5_proper_sets.json` の `proper20`。
  v4の10305字をすべて含み、新規8109字を追加。
- 内訳: 漢字13962字（JIS X 0213 全10050字＋JIS X 0212 3058字＋CJK互換漢字326字＋
  CJK拡張A 38字・B 51字・C 1字・D 25字・F 4字＋JIS外CJK 409字）、
  ひらがな91字（清音46＋濁音20＋半濁音5＋小さい仮名9＋繰り返し記号2＋
  ゐゑゔゕゖゎ゛゜ゟ 9字）、カタカナ95字（清音46＋濁音20＋半濁音5＋
  小さい仮名9＋長音記号ー＋繰り返し記号2＋ヰヱヴヵヶヮ゠ヷヸヹヺヿ 12字）、
  小さいカタカナ16字（ㇰㇱㇲㇳㇴㇵㇶㇷㇸㇹㇺㇻㇼㇽㇾㇿ）、
  数字0–9、英字A–Z、英字a–z、
  半角句読点32字（! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~）、
  全角英数字・記号91字（Ａ–Ｚ ａ–ｚ ０–９ ！＂＃＄％＆＇＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～ ￠￡￥￦ など）、
  半角カタカナ121字（ｱ–ﾝ・ﾞﾟなど）、ラテン1補助92字（À–ÿ・©®°±×÷ など）、
  ラテン拡張336字、ラテン拡張追加256字、IPA・音声記号233字、
  ギリシア文字120字、ギリシア拡張233字、キリル文字260字、ヘブライ文字35字、
  記号1173字（罫線・ブロック・幾何学図形・通貨・句読点など）、
  矢印95字、数学記号188字、囲み文字895字（①–⑳・㉑–㊿・Ⓐ–Ⓩ・Ⅰ–Ⅻ・㈱など）、
  句読点・記号28字（v4から継続）。
- TTFにはさらにスペース（U+0020、空グリフ・送り500）を追加。
  アラビア文字・アルメニア文字は proper20 に0字（20書体以上持つ書体がないため）。

## 文字セット（v4: 10305字）

- ひらがな82字（清音46＋濁音20＋半濁音5＋小さい仮名9＋繰り返し記号 ゝゞ 2）、
  カタカナ83字（清音46＋濁音20＋半濁音5＋小さい仮名9＋長音記号ー＋繰り返し記号 ヽヾ 2）、
  数字0–9、 英字A–Z、 英字a–z、
  漢字10050字（JIS X 0213 第1水準2965＋第2水準3390＋第3水準1259＋第4水準2436。
  常用漢字2136字・人名用漢字846字種はすべて含まれる）、
  句読点・記号28字（、。・「」『』（）〔〕【】！？…―〜：；－／＼＝＋×÷％）
- TTFにはさらにスペース（U+0020、空グリフ・送り500）を追加。
  JIS X 0213 の非漢字（ギリシア文字・丸付き数字など）や JIS X 0212・
  CJK統合漢字拡張B以降の漢字は**未収録**（豆腐になる）。

## 文字セット（v3: 2290字）

- ひらがな46字、 カタカナ46字、 数字0–9、 英字A–Z、 英字a–z、
  漢字2136字（常用漢字フルセット。v2の20字を含む）
- TTFにはさらにスペース（U+0020、空グリフ・送り500）を追加。
  句読点・濁点つき仮名・小さい仮名・長音記号・常用漢字以外の漢字は
  **未収録**（豆腐になる）。v4で全て収録済み。

## v3 で変わったこと（174字 → 2290字、2026-11-06）

- **漢字を常用漢字2136字フルセットに拡張**（v2の20字 → 2136字）。
  常用漢字リストは Wikipedia「常用漢字一覧」（文化庁の表）の全2136字。
  2010年に削除された5字（勺錘銑脹匁）は表の下部に併記されているため除外し、
  異体字で載っていた 𠮟（U+20B9F、Unicode追加面）は公式形の 叱（U+53F1）に
  置き換えた。全2136字が BMP（U+4E00〜U+9FFF）内であることを確認済み。
  リストは `work/joyo_kanji.txt` に保存。v2の174字はすべて残してある。
- **見えづらい漢字の調整 — 適応しきい値**（`work/build_ttf_v3.py`）:
  原因を実測で特定した。寄与フォント不足ではなかった（常用漢字は全字
  200〜227書体が寄与）し、平均インクの最大値も全字157以上（漢字の中央値251）。
  本当の原因は**インクの拡散**で、同じ画でも書体ごとに置くピクセルが少しずつ
  違うため、平均は芯のまわりに滲んだハローになる。固定128では芯しか残らず、
  見えるインク（画素値64以上）のうち残るのは中央値で55%、最悪の字
  （言・二・吉・士など）では約31%しか残らなかった。特に横画だけの
  一・二・三（最大値180〜195）は固定128だと骨だけになっていた。
  v3はグリフごとに `しきい値 = 0.40 × 平均インク最大値（8〜128にクランプ）`
  とし、濃い字は102前後（v2の128に近い見た目）、薄い字は20〜40台まで
  下げることで、画の芯が残るようにした。寄与フォント数での正規化は
  v2からすでに行っており（平均＝合計÷寄与数）、v3でも同じ。
- **効果（実測）**: 薄い字28字（平均インク最大値210未満）の二値化後インク量は
  固定128比で大幅に増えた。例: ニ 929px → 11009px（しきい値62.8）、
  一 2273px → 5029px（72.2）、二 3074px → 8510px（74.0）、
  乞は固定128だと縦画1本しか残らなかったが適応後は字形が読める。
  目視の証拠は `out/faint_before_after_v3.png`（薄い24字を
  平均PNG｜固定128｜適応しきい値の3列で並べたもの）と
  `out/ttf_test_v3.png`（薄い24字の行を v3 TTF で組版）。
  代償として v3 の画は v2 より太めになる（ハローを拾うため）。
  画同士がくっつき気味の字もあるが、読めることを優先した。
- **計算量**: 229書体 × 2290字の描画で約23分（v2は174字で24秒）。
  平均の合計値は float32 で2290字分・約600MBになるため、RAM（約8GB・空き僅か）
  には載せず numpy の memmap ファイル（`work/v3_acc.dat`、完了後削除）で処理した。
- **旧版の保存**: v2のTTF（`AverageFont-Regular.ttf`、174字）と
  v2の `out/` 成果物（`stats.json`・`glyphs/`・コンタクトシート・`ttf_test.png`・
  `viewer.html`）はすべて残してある。v3の成果物はすべて `_v3` サフィックスつき。

## v4 で変わったこと（2290字 → 10305字、2026-11-07）

- **漢字を JIS X 0213 全10050字に拡張**（常用2136字 → 第1水準2965＋
  第2水準3390＋第3水準1259＋第4水準2436）。第4水準まで入れたので、
  当初の「第3水準まで＋余力があれば第4水準」も両方達成。
  漢字リストは Wikipedia「JIS X 0213漢字一覧の1面・2面」
  （JIS X 0213:2004、水準分類つき）から抽出し、字数
  2965／3390／1259／2436・重複0を検証済み。
  リストは `work/jisx0213_kanji.txt`（水準別）と
  `work/jisx0213_kanji.json`（面区点・水準つき）に保存。
  注意点として、euc_jis_2004 コーデックで区だけから水準を決める方法は
  使えない（第3水準は1面85〜94区だけでなく1面14区など保留セルにも散らばり、
  2004年追加の10字もそこに入る）。水準は一覧表の分類をそのまま使った。
  常用漢字のうち剝・塡・頰の3字は第1・第2水準ではなく第3水準側にある。
- **人名用漢字も内包**: 人名用漢字（（一）634字種＋（二）212字種＝846字種、
  2026年6月現在864字体。出典は Wikipedia「人名用漢字一覧」、
  `work/jinmeiyo_kanji.txt` に保存）は全て JIS X 0213 の中に含まれることを
  確認済み。2026年6月に追加された勒（U+52D2）も第2水準として収録済み。
  常用2136字＋人名用漢字863字＝2999字という当初の目標も、
  JIS X 0213 の部分集合として達成している。
- **仮名をフルセット化**: 濁音（が行・ざ行・だ行・ば行、ひらがな・カタカナ各20字）、
  半濁音（ぱ行・パ行、各5字）、小さい仮名（ぁぃぅぇぉっゃゅょ・ァィゥェォッャュョ、各9字）、
  長音記号ー、繰り返し記号ゝゞヽヾを追加。計73字。
  濁点つき仮名を持たない書体もあるが、寄与数はひらがな最小227・カタカナ最小208
  （ヾが208で最少、他は227〜228）と十分で、薄い字対策の適応しきい値も同じ。
  「じ」が打てないという v3 の残課題は解消。
- **句読点・記号28字を追加**: 、。・「」『』（）〔〕【】！？…―〜：；－／＼＝＋×÷％。
  寄与数は最小202・中央値228。
- **非BMP文字の対応**: 第3・第4水準には CJK統合漢字拡張Bの文字が303字ある。
  TTF の cmap を format 4 だけでなく format 12（UCS-4、platform 3 / encoding 10）
  も併記し、303字すべて cmap に入れた。寄与数は非BMPでも最小100。
- **寄与0の字は0字**: 10305字すべてに94書体以上が寄与したため、
  TTF からの除外は1字も発生しなかった（build 時の除外ロジックは用意したが未発動）。
  最も寄与が少ないのは第4水準の歺（94書体）。
- **計算量**: 229書体 × 10305字の描画で約89分（v3は2290字で約23分）。
  合計値は float32 で10305字分・約2.7GBになるため v3 と同じく numpy memmap
  （`work/v4_acc.dat`）で処理した。さらに v4 ではチャンク単位（512字）で
  進捗を `work/v4_progress.json` に書き、途中終了しても再開できる作りにした。
  実際、初回実行が178/229書体でプロセスごと止まったが、再開して残り51書体だけ
  描画して完了した（止まった原因は不明・ログにエラーなし）。
- **テスト文の反省を修正**: v3のテスト文は収録字だけに直してごまかしていたため、
  v4のテスト文は追加字をちゃんと打てる文にした（「じゅうようなじじつ：太陽は
  東から昇る。」「ウィークエンドにパーティーへ行く。ちょっと待って！」
  「『重要』なことは、もう一度言う。――太陽が昇る。」など）。
  `work/make_sheets_v4.py` はテスト文の全文字が cmap にあり輪郭が空でないことを
  assert で検証し、豆腐があればスクリプトごと失敗する（今回は0件）。
- **旧版の保存**: v3のTTF（`AverageFont-Regular-v3-229fonts-2290chars.ttf`、2290字）と
  v3の `out/` 成果物（`stats_v3.json`・`glyphs_v3/`・コンタクトシート・`ttf_test_v3.png`・
  `viewer_v3.html`）はすべて残してある。v2・v1のTTFも残してある。
  v4の成果物はすべて `_v4` サフィックスつき。

## v5 で変わったこと（10305字 → 18414字、2026-11-08）

- **文字セットの定義を変えた**: v4までは「JIS X 0213漢字＋かな＋記号28字」という
  日本語中心の決め方で、半角句読点・全角英数字・ギリシア・キリル・丸数字などが
  欠けていた（2026-11-08 本人指摘「重大」）。v5は「229書体のうち20書体以上が
  グリフを持つ可視文字」（proper20、Unicodeカテゴリ Cc/Cf/Cs/Co/Cn/Zl/Zp/Zs/
  Mn/Me/Mc を除く）で定義し直し、全Unicodeを走査して18414字を選んだ。
  JIS X 0213非漢字＋JIS X 0212はすべて含まれる。
- **除外は時間の問題ではなく手法の問題**: 20書体未満の字は、拡張B 42720字中
  42366字・拡張A 6592字中6390字・ハングル11172字全てなどで、実態は
  1ファミリー（5〜9ウェイト）だけが持つものが大半。1書体のコピーを
  「229書体の平均」と呼ぶのは不正確なので、描画に何時間かかろうと入れない。
  時間無制限の指示があったが、それでも平均にならない字は入れていない。
  10〜19書体の帯1133字も今回は見送り、v6検討事項として記録する。
  結合文字・不可視文字（Zs/Mn等）は単独描画できないため除外。
- **v4は描画し直さない**: `out/glyphs_v4/*.png` を `out/glyphs_v5/` にコピーし、
  新規8109字だけ平均化した（229書体 × 8109字、約25分、チャンク単位で再開可能）。
  v4の10305字の順序・ファイル名はそのまま維持。
- **寄与数**: 全18414字で min 20・中央値122・max 229。寄与0の字は0字。
  グループ別（新規分）: 漢字3912（min 21・中央値86）、記号1173、囲み895、
  ラテン拡張336、キリル260、ラテン拡張追加256、IPA 233、ギリシア拡張233、
  数学188、半角121、ギリシア120、矢印95、ラテン1 92、全角91、ヘブライ35、
  半角句読点32、仮名拡張16、カタカナ12、ひらがな9。
  薄い字（max_ink<210）は373字。横線系（═ ¯ ◜ ＾ – — ‐ ˉ ˜ -）が最も薄く、
  固定128だと0pxしか残らない字もあるが、適応しきい値で拾っている
  （例: ═ は0px → 13815px）。
- **目視で気づいたクセ**: 全角＠は小さめに潰れて見える、ローマ数字ⅠⅡⅢや
  括弧（）〔〕【】は細い。これは平均化の結果で、豆腐ではない。
  `out/ttf_test_v5.png` で目視確認済み。
- **旧版の保存**: v4のTTF（`AverageFont-Regular-v4-229fonts-10305chars.ttf`、10305字）と
  v4の `out/` 成果物（`stats_v4.json`・`glyphs_v4/`・コンタクトシート・`ttf_test_v4.png`・
  `viewer_v4.html`）はすべて残してある。`AverageFont-Regular.ttf` は v4 のまま。
  v5の成果物はすべて `_v5` サフィックスつき。

## v2 で変わったこと（100書体 → 229書体）

- **きつい書体枠を追加**: Dela Gothic One、Rampart One、Reggae One、RocknRoll One、
  Potta One、Mochiy Pop One/P One、Hachi Maru Pop、だるまドロップ、Zen Dots、
  Yuji 系、New Tegomin、しっぽりアンティーク、Murecho、M PLUS 1 ほか、
  太い・デコラティブ・ドット・レトロ系をまとめて投入。
- **平均への影響**: 太字・ディスプレイ系の比率が上がり、v2の平均は全体的に
  インク量が増えて（平均グリフの濃度 27.35/255 ≒ 10.7%）少し太く・黒くなった。
  ただし平均化でクセは相殺されるため、ドットの粒や極太の角はぼんやりした滲みに留まる。
  漢字は227書体寄与（だるまドロップ・Zen Dotsは漢字グリフなし）。
- **旧版の保存**: v1のTTFは `AverageFont-Regular-v1-100fonts.ttf` として残してある。

## 元書体229書体の内訳

- 可変フォント（ウェイト展開）: Noto Sans JP 9、Noto Serif JP 8、M PLUS 2 9、
  Murecho 9、M PLUS 1 9 ＝ 44書体
- google/fonts スタティック（v1: 80 ＋ v2追加 21）: Zen 角ゴ New 5、Zen 丸ゴ 5、
  Zen Old 明朝 3、Zen 角ゴ Antique 5、M PLUS 1p 7、M PLUS Rounded 1c 7、
  しっぽり明朝 5、しっぽり明朝 B1 5、BIZ UDゴシック 2、BIZ UDP明朝 2、BIZ UD明朝 2、
  BIZ UDPゴシック 2、Kaisei Decol 3、Kaisei Tokumin 4、Kaisei HarunoUmi 3、Kaisei Opti 3、
  Hina 明朝 1、DotGothic16 1、さわらびゴシック 1、さわらび明朝 1、Yusei Magic 1、
  Zen Kurenaido 1、Zen Antique 1、Zen Antique Soft 1、Stick 1、
  Dela Gothic One 1、Rampart One 1、Reggae One 1、RocknRoll One 1、Potta One 1、
  Mochiy Pop One 1、Mochiy Pop P One 1、Hachi Maru Pop 1、だるまドロップ 1、Zen Dots 1、
  Yuji Syuku 1、Yuji Mai 1、Yuji Boku 1、New Tegomin 1、しっぽりアンティーク 1、
  しっぽりアンティーク B1 1、Yomogi 1、Kiwi 丸 3、Klee One 2、IBM Plex Sans JP 7 ＝ 101書体
- google/fonts以外: Source Han Sans JP 7、Source Han Serif JP 7、IPAexゴシック 1、
  IPAex明朝 1、Takaoゴシック 1、Takao Pゴシック 1、Takao明朝 1、Takao P明朝 1、
  VLゴシック 1、VL Pゴシック 1、MigMix 8、Migu 8、UmePlusゴシック 1、UmePlus Pゴシック 1、
  Koruri 3、HackGen 4、UDEV Gothic 4、Moralerspace（Neon/Argon）4、PlemolJP 4、
  Cica 4、源柔ゴシック 7、源真ゴシック 7、源流明朝 JP 7 ＝ 84書体
- 全一覧（出所URL・ライセンス付き）は `SOURCES.md` を参照。

| # | 書体 | ファイル |
|---:|---|---|
| 1 | Noto Sans JP 100 | `NotoSansJP[wght].ttf` |
| 2 | Noto Sans JP 200 | `NotoSansJP[wght].ttf` |
| 3 | Noto Sans JP 300 | `NotoSansJP[wght].ttf` |
| 4 | Noto Sans JP 400 | `NotoSansJP[wght].ttf` |
| 5 | Noto Sans JP 500 | `NotoSansJP[wght].ttf` |
| 6 | Noto Sans JP 600 | `NotoSansJP[wght].ttf` |
| 7 | Noto Sans JP 700 | `NotoSansJP[wght].ttf` |
| 8 | Noto Sans JP 800 | `NotoSansJP[wght].ttf` |
| 9 | Noto Sans JP 900 | `NotoSansJP[wght].ttf` |
| 10 | Noto Serif JP 200 | `NotoSerifJP[wght].ttf` |
| 11 | Noto Serif JP 300 | `NotoSerifJP[wght].ttf` |
| 12 | Noto Serif JP 400 | `NotoSerifJP[wght].ttf` |
| 13 | Noto Serif JP 500 | `NotoSerifJP[wght].ttf` |
| 14 | Noto Serif JP 600 | `NotoSerifJP[wght].ttf` |
| 15 | Noto Serif JP 700 | `NotoSerifJP[wght].ttf` |
| 16 | Noto Serif JP 800 | `NotoSerifJP[wght].ttf` |
| 17 | Noto Serif JP 900 | `NotoSerifJP[wght].ttf` |
| 18 | M PLUS 2 100 | `MPLUS2[wght].ttf` |
| 19 | M PLUS 2 200 | `MPLUS2[wght].ttf` |
| 20 | M PLUS 2 300 | `MPLUS2[wght].ttf` |
| 21 | M PLUS 2 400 | `MPLUS2[wght].ttf` |
| 22 | M PLUS 2 500 | `MPLUS2[wght].ttf` |
| 23 | M PLUS 2 600 | `MPLUS2[wght].ttf` |
| 24 | M PLUS 2 700 | `MPLUS2[wght].ttf` |
| 25 | M PLUS 2 800 | `MPLUS2[wght].ttf` |
| 26 | M PLUS 2 900 | `MPLUS2[wght].ttf` |
| 27 | Zen Kaku Gothic New Light | `ZenKakuGothicNew-Light.ttf` |
| 28 | Zen Kaku Gothic New Regular | `ZenKakuGothicNew-Regular.ttf` |
| 29 | Zen Kaku Gothic New Medium | `ZenKakuGothicNew-Medium.ttf` |
| 30 | Zen Kaku Gothic New Bold | `ZenKakuGothicNew-Bold.ttf` |
| 31 | Zen Kaku Gothic New Black | `ZenKakuGothicNew-Black.ttf` |
| 32 | Zen Maru Gothic Light | `ZenMaruGothic-Light.ttf` |
| 33 | Zen Maru Gothic Regular | `ZenMaruGothic-Regular.ttf` |
| 34 | Zen Maru Gothic Medium | `ZenMaruGothic-Medium.ttf` |
| 35 | Zen Maru Gothic Bold | `ZenMaruGothic-Bold.ttf` |
| 36 | Zen Maru Gothic Black | `ZenMaruGothic-Black.ttf` |
| 37 | Zen Old Mincho Regular | `ZenOldMincho-Regular.ttf` |
| 38 | Zen Old Mincho Bold | `ZenOldMincho-Bold.ttf` |
| 39 | Zen Old Mincho Black | `ZenOldMincho-Black.ttf` |
| 40 | Zen Kaku Gothic Antique Light | `ZenKakuGothicAntique-Light.ttf` |
| 41 | Zen Kaku Gothic Antique Regular | `ZenKakuGothicAntique-Regular.ttf` |
| 42 | Zen Kaku Gothic Antique Medium | `ZenKakuGothicAntique-Medium.ttf` |
| 43 | Zen Kaku Gothic Antique Bold | `ZenKakuGothicAntique-Bold.ttf` |
| 44 | Zen Kaku Gothic Antique Black | `ZenKakuGothicAntique-Black.ttf` |
| 45 | M PLUS 1p Thin | `MPLUS1p-Thin.ttf` |
| 46 | M PLUS 1p Light | `MPLUS1p-Light.ttf` |
| 47 | M PLUS 1p Regular | `MPLUS1p-Regular.ttf` |
| 48 | M PLUS 1p Medium | `MPLUS1p-Medium.ttf` |
| 49 | M PLUS 1p Bold | `MPLUS1p-Bold.ttf` |
| 50 | M PLUS 1p ExtraBold | `MPLUS1p-ExtraBold.ttf` |
| 51 | M PLUS 1p Black | `MPLUS1p-Black.ttf` |
| 52 | M PLUS Rounded 1c Thin | `MPLUSRounded1c-Thin.ttf` |
| 53 | M PLUS Rounded 1c Light | `MPLUSRounded1c-Light.ttf` |
| 54 | M PLUS Rounded 1c Regular | `MPLUSRounded1c-Regular.ttf` |
| 55 | M PLUS Rounded 1c Medium | `MPLUSRounded1c-Medium.ttf` |
| 56 | M PLUS Rounded 1c Bold | `MPLUSRounded1c-Bold.ttf` |
| 57 | M PLUS Rounded 1c ExtraBold | `MPLUSRounded1c-ExtraBold.ttf` |
| 58 | M PLUS Rounded 1c Black | `MPLUSRounded1c-Black.ttf` |
| 59 | Shippori Mincho Regular | `ShipporiMincho-Regular.ttf` |
| 60 | Shippori Mincho Medium | `ShipporiMincho-Medium.ttf` |
| 61 | Shippori Mincho SemiBold | `ShipporiMincho-SemiBold.ttf` |
| 62 | Shippori Mincho Bold | `ShipporiMincho-Bold.ttf` |
| 63 | Shippori Mincho ExtraBold | `ShipporiMincho-ExtraBold.ttf` |
| 64 | Shippori Mincho B1 Regular | `ShipporiMinchoB1-Regular.ttf` |
| 65 | Shippori Mincho B1 Medium | `ShipporiMinchoB1-Medium.ttf` |
| 66 | Shippori Mincho B1 Bold | `ShipporiMinchoB1-Bold.ttf` |
| 67 | IBM Plex Sans JP Thin | `IBMPlexSansJP-Thin.ttf` |
| 68 | IBM Plex Sans JP ExtraLight | `IBMPlexSansJP-ExtraLight.ttf` |
| 69 | IBM Plex Sans JP Light | `IBMPlexSansJP-Light.ttf` |
| 70 | IBM Plex Sans JP Regular | `IBMPlexSansJP-Regular.ttf` |
| 71 | IBM Plex Sans JP Medium | `IBMPlexSansJP-Medium.ttf` |
| 72 | IBM Plex Sans JP SemiBold | `IBMPlexSansJP-SemiBold.ttf` |
| 73 | IBM Plex Sans JP Bold | `IBMPlexSansJP-Bold.ttf` |
| 74 | Kiwi Maru Light | `KiwiMaru-Light.ttf` |
| 75 | Kiwi Maru Regular | `KiwiMaru-Regular.ttf` |
| 76 | Kiwi Maru Medium | `KiwiMaru-Medium.ttf` |
| 77 | Klee One Regular | `KleeOne-Regular.ttf` |
| 78 | Klee One SemiBold | `KleeOne-SemiBold.ttf` |
| 79 | BIZ UDGothic Regular | `BIZUDGothic-Regular.ttf` |
| 80 | BIZ UDGothic Bold | `BIZUDGothic-Bold.ttf` |
| 81 | BIZ UDPMincho Regular | `BIZUDPMincho-Regular.ttf` |
| 82 | BIZ UDPMincho Bold | `BIZUDPMincho-Bold.ttf` |
| 83 | BIZ UDMincho Regular | `BIZUDMincho-Regular.ttf` |
| 84 | BIZ UDMincho Bold | `BIZUDMincho-Bold.ttf` |
| 85 | Kaisei Decol Regular | `KaiseiDecol-Regular.ttf` |
| 86 | Kaisei Decol Medium | `KaiseiDecol-Medium.ttf` |
| 87 | Kaisei Decol Bold | `KaiseiDecol-Bold.ttf` |
| 88 | Kaisei Tokumin Regular | `KaiseiTokumin-Regular.ttf` |
| 89 | Kaisei Tokumin Medium | `KaiseiTokumin-Medium.ttf` |
| 90 | Kaisei Tokumin Bold | `KaiseiTokumin-Bold.ttf` |
| 91 | Kaisei Tokumin ExtraBold | `KaiseiTokumin-ExtraBold.ttf` |
| 92 | Kaisei HarunoUmi Regular | `KaiseiHarunoUmi-Regular.ttf` |
| 93 | Kaisei HarunoUmi Medium | `KaiseiHarunoUmi-Medium.ttf` |
| 94 | Kaisei HarunoUmi Bold | `KaiseiHarunoUmi-Bold.ttf` |
| 95 | Kaisei Opti Regular | `KaiseiOpti-Regular.ttf` |
| 96 | Kaisei Opti Medium | `KaiseiOpti-Medium.ttf` |
| 97 | Kaisei Opti Bold | `KaiseiOpti-Bold.ttf` |
| 98 | Hina Mincho | `HinaMincho-Regular.ttf` |
| 99 | DotGothic16 | `DotGothic16-Regular.ttf` |
| 100 | さわらびゴシック | `SawarabiGothic-Regular.ttf` |
| 101 | さわらび明朝 | `SawarabiMincho-Regular.ttf` |
| 102 | Yusei Magic | `YuseiMagic-Regular.ttf` |
| 103 | Zen Kurenaido | `ZenKurenaido-Regular.ttf` |
| 104 | Zen Antique | `ZenAntique-Regular.ttf` |
| 105 | Zen Antique Soft | `ZenAntiqueSoft-Regular.ttf` |
| 106 | Stick | `Stick-Regular.ttf` |
| 107 | Dela Gothic One | `DelaGothicOne-Regular.ttf` |
| 108 | Rampart One | `RampartOne-Regular.ttf` |
| 109 | Reggae One | `ReggaeOne-Regular.ttf` |
| 110 | RocknRoll One | `RocknRollOne-Regular.ttf` |
| 111 | Potta One | `PottaOne-Regular.ttf` |
| 112 | Mochiy Pop One | `MochiyPopOne-Regular.ttf` |
| 113 | Mochiy Pop P One | `MochiyPopPOne-Regular.ttf` |
| 114 | Hachi Maru Pop | `HachiMaruPop-Regular.ttf` |
| 115 | Darumadrop One | `DarumadropOne-Regular.ttf` |
| 116 | Zen Dots | `ZenDots-Regular.ttf` |
| 117 | Yuji Syuku | `YujiSyuku-Regular.ttf` |
| 118 | Yuji Mai | `YujiMai-Regular.ttf` |
| 119 | Yuji Boku | `YujiBoku-Regular.ttf` |
| 120 | New Tegomin | `NewTegomin-Regular.ttf` |
| 121 | Shippori Antique | `ShipporiAntique-Regular.ttf` |
| 122 | Shippori Antique B1 | `ShipporiAntiqueB1-Regular.ttf` |
| 123 | Yomogi | `Yomogi-Regular.ttf` |
| 124 | Murecho 100 | `Murecho[wght].ttf` |
| 125 | Murecho 200 | `Murecho[wght].ttf` |
| 126 | Murecho 300 | `Murecho[wght].ttf` |
| 127 | Murecho 400 | `Murecho[wght].ttf` |
| 128 | Murecho 500 | `Murecho[wght].ttf` |
| 129 | Murecho 600 | `Murecho[wght].ttf` |
| 130 | Murecho 700 | `Murecho[wght].ttf` |
| 131 | Murecho 800 | `Murecho[wght].ttf` |
| 132 | Murecho 900 | `Murecho[wght].ttf` |
| 133 | M PLUS 1 100 | `MPLUS1[wght].ttf` |
| 134 | M PLUS 1 200 | `MPLUS1[wght].ttf` |
| 135 | M PLUS 1 300 | `MPLUS1[wght].ttf` |
| 136 | M PLUS 1 400 | `MPLUS1[wght].ttf` |
| 137 | M PLUS 1 500 | `MPLUS1[wght].ttf` |
| 138 | M PLUS 1 600 | `MPLUS1[wght].ttf` |
| 139 | M PLUS 1 700 | `MPLUS1[wght].ttf` |
| 140 | M PLUS 1 800 | `MPLUS1[wght].ttf` |
| 141 | M PLUS 1 900 | `MPLUS1[wght].ttf` |
| 142 | BIZ UDPGothic Regular | `BIZUDPGothic-Regular.ttf` |
| 143 | BIZ UDPGothic Bold | `BIZUDPGothic-Bold.ttf` |
| 144 | Shippori Mincho B1 SemiBold | `ShipporiMinchoB1-SemiBold.ttf` |
| 145 | Shippori Mincho B1 ExtraBold | `ShipporiMinchoB1-ExtraBold.ttf` |
| 146 | Source Han Sans JP ExtraLight | `SourceHanSansJP-ExtraLight.otf` |
| 147 | Source Han Sans JP Light | `SourceHanSansJP-Light.otf` |
| 148 | Source Han Sans JP Normal | `SourceHanSansJP-Normal.otf` |
| 149 | Source Han Sans JP Regular | `SourceHanSansJP-Regular.otf` |
| 150 | Source Han Sans JP Medium | `SourceHanSansJP-Medium.otf` |
| 151 | Source Han Sans JP Bold | `SourceHanSansJP-Bold.otf` |
| 152 | Source Han Sans JP Heavy | `SourceHanSansJP-Heavy.otf` |
| 153 | Source Han Serif JP ExtraLight | `SourceHanSerifJP-ExtraLight.otf` |
| 154 | Source Han Serif JP Light | `SourceHanSerifJP-Light.otf` |
| 155 | Source Han Serif JP Regular | `SourceHanSerifJP-Regular.otf` |
| 156 | Source Han Serif JP Medium | `SourceHanSerifJP-Medium.otf` |
| 157 | Source Han Serif JP SemiBold | `SourceHanSerifJP-SemiBold.otf` |
| 158 | Source Han Serif JP Bold | `SourceHanSerifJP-Bold.otf` |
| 159 | Source Han Serif JP Heavy | `SourceHanSerifJP-Heavy.otf` |
| 160 | IPAexゴシック | `IPAexGothic.ttf` |
| 161 | IPAex明朝 | `IPAexMincho.ttf` |
| 162 | Takaoゴシック | `TakaoGothic.ttf` |
| 163 | Takao Pゴシック | `TakaoPGothic.ttf` |
| 164 | Takao明朝 | `TakaoMincho.ttf` |
| 165 | Takao P明朝 | `TakaoPMincho.ttf` |
| 166 | VLゴシック | `VLGothic-Regular.ttf` |
| 167 | VL Pゴシック | `VLPGothic-Regular.ttf` |
| 168 | MigMix 1P Regular | `MigMix-1P-Regular.ttf` |
| 169 | MigMix 1P Bold | `MigMix-1P-Bold.ttf` |
| 170 | MigMix 2P Regular | `MigMix-2P-Regular.ttf` |
| 171 | MigMix 2P Bold | `MigMix-2P-Bold.ttf` |
| 172 | MigMix 1M Regular | `MigMix-1M-Regular.ttf` |
| 173 | MigMix 1M Bold | `MigMix-1M-Bold.ttf` |
| 174 | MigMix 2M Regular | `MigMix-2M-Regular.ttf` |
| 175 | MigMix 2M Bold | `MigMix-2M-Bold.ttf` |
| 176 | Migu 1M Regular | `Migu-1M-Regular.ttf` |
| 177 | Migu 1M Bold | `Migu-1M-Bold.ttf` |
| 178 | Migu 1C Regular | `Migu-1C-Regular.ttf` |
| 179 | Migu 1C Bold | `Migu-1C-Bold.ttf` |
| 180 | Migu 1P Regular | `Migu-1P-Regular.ttf` |
| 181 | Migu 1P Bold | `Migu-1P-Bold.ttf` |
| 182 | Migu 2M Regular | `Migu-2M-Regular.ttf` |
| 183 | Migu 2M Bold | `Migu-2M-Bold.ttf` |
| 184 | UmePlusゴシック | `UmePlus-Gothic.ttf` |
| 185 | UmePlus Pゴシック | `UmePlus-P-Gothic.ttf` |
| 186 | Koruri Regular | `Koruri-Regular.ttf` |
| 187 | Koruri Bold | `Koruri-Bold.ttf` |
| 188 | Koruri Semibold | `Koruri-Semibold.ttf` |
| 189 | HackGen Regular | `HackGen-Regular.ttf` |
| 190 | HackGen Bold | `HackGen-Bold.ttf` |
| 191 | HackGen Console Regular | `HackGenConsole-Regular.ttf` |
| 192 | HackGen Console Bold | `HackGenConsole-Bold.ttf` |
| 193 | UDEV Gothic Regular | `UDEVGothic-Regular.ttf` |
| 194 | UDEV Gothic Bold | `UDEVGothic-Bold.ttf` |
| 195 | UDEV Gothic 35 Regular | `UDEVGothic35-Regular.ttf` |
| 196 | UDEV Gothic 35 Bold | `UDEVGothic35-Bold.ttf` |
| 197 | Moralerspace Neon Regular | `MoralerspaceNeon-Regular.ttf` |
| 198 | Moralerspace Neon Bold | `MoralerspaceNeon-Bold.ttf` |
| 199 | Moralerspace Argon Regular | `MoralerspaceArgon-Regular.ttf` |
| 200 | Moralerspace Argon Bold | `MoralerspaceArgon-Bold.ttf` |
| 201 | PlemolJP Regular | `PlemolJP-Regular.ttf` |
| 202 | PlemolJP Bold | `PlemolJP-Bold.ttf` |
| 203 | PlemolJP Console Regular | `PlemolJPConsole-Regular.ttf` |
| 204 | PlemolJP Console Bold | `PlemolJPConsole-Bold.ttf` |
| 205 | Cica Regular | `Cica-Regular.ttf` |
| 206 | Cica Bold | `Cica-Bold.ttf` |
| 207 | Cica Bold Italic | `Cica-BoldItalic.ttf` |
| 208 | Cica Regular Italic | `Cica-RegularItalic.ttf` |
| 209 | GenJyuuGothic ExtraLight | `GenJyuuGothic-ExtraLight.ttf` |
| 210 | GenJyuuGothic Light | `GenJyuuGothic-Light.ttf` |
| 211 | GenJyuuGothic Normal | `GenJyuuGothic-Normal.ttf` |
| 212 | GenJyuuGothic Regular | `GenJyuuGothic-Regular.ttf` |
| 213 | GenJyuuGothic Medium | `GenJyuuGothic-Medium.ttf` |
| 214 | GenJyuuGothic Bold | `GenJyuuGothic-Bold.ttf` |
| 215 | GenJyuuGothic Heavy | `GenJyuuGothic-Heavy.ttf` |
| 216 | GenShinGothic ExtraLight | `GenShinGothic-ExtraLight.ttf` |
| 217 | GenShinGothic Light | `GenShinGothic-Light.ttf` |
| 218 | GenShinGothic Normal | `GenShinGothic-Normal.ttf` |
| 219 | GenShinGothic Regular | `GenShinGothic-Regular.ttf` |
| 220 | GenShinGothic Medium | `GenShinGothic-Medium.ttf` |
| 221 | GenShinGothic Bold | `GenShinGothic-Bold.ttf` |
| 222 | GenShinGothic Heavy | `GenShinGothic-Heavy.ttf` |
| 223 | GenRyuMin JP ExtraLight | `GenRyuMin2JP-ExtraLight.otf` |
| 224 | GenRyuMin JP Light | `GenRyuMin2JP-Light.otf` |
| 225 | GenRyuMin JP Regular | `GenRyuMin2JP-Regular.otf` |
| 226 | GenRyuMin JP Medium | `GenRyuMin2JP-Medium.otf` |
| 227 | GenRyuMin JP SemiBold | `GenRyuMin2JP-SemiBold.otf` |
| 228 | GenRyuMin JP Bold | `GenRyuMin2JP-Bold.otf` |
| 229 | GenRyuMin JP Heavy | `GenRyuMin2JP-Heavy.otf` |

## ライセンス

- 元書体の大半は **SIL Open Font License 1.1 (OFL)**。
  ただし IPAex／Takao は IPAフォントライセンス、VLゴシックは VLゴシックライセンス、
  MigMix／Migu は Migu・MigMixライセンス、UmePlus は梅フォント派生ライセンスと、
  OFL以外のオープンライセンスの書体も含む（詳細は `SOURCES.md` のライセンス欄）。
  各ライセンスの条件（ライセンス文の同梱・改変時の改名など）に従うこと。
- 平均グリフ画像・TTF は229書体の画素統計から生成した派生物。
  「Average Font」という名前で新規フォントとして配布する場合は、
  OFL の Reserved Font Name（例：「Noto」「M PLUS」など）を使っていないことを確認済み。
  商用利用の可否は最終的に利用者の責任で確認すること。

## 制限・正直なところ

- **滲み**: 平均化の当然の結果として、グリフはぼやける。特に筆画の多い漢字や
  明朝・ゴシックが混ざる文字は輪郭が二重に見える。これはバグではなく手法の特性。
- **ベースライン**: 描画時に文字を中央揃えしたため、TTF化の際にグループ別に
  シフトで補正した（かな・漢字 −60、数字・大文字 −150、小文字 −250 単位）。
  完全なベースライン一致ではないので、本文組版には向かない。見出し・実験用途向け。
- **TTFの輪郭**: ベジェ曲線ではなく直線の多角形近似（`approxPolyDP`、許容誤差1.5px）。
  拡大するとカクつきが見える。ヒンティング・カーニングなし。
- **ndot jp について**: 依頼の「ndot jp（DotGothic16系、GitHubのndotjp）」は
  GitHub 上に `ndotjp` ユーザー／組織が存在せず、配布元が特定できる
  オープンライセンスの「Ndot JP」も見つからなかったため、ドットフォント枠は
  同じドット系で OFL の **DotGothic16** で代替した（詳細は `SOURCES.md`）。
- **小杉フォント**: google/fonts に未収録で、配布元（GitHub）の公式リリースも
  特定できなかったため今回は含めていない。
- **さざなみフォント**: 配布元（OSDN）のダウンロードURLが特定できず今回は見送った。
- **Koku 明朝／Koku ゴシック**: GitHubリポジトリが見つからず今回は含めていない。
- **文字数**: v5は18414字＋スペース。定義は proper20（20書体以上が持つ可視文字）。
  除外したのは20書体未満の字（拡張B 42720字中42366字・拡張A 6592字中6390字・
  ハングル11172字全てなど、1ファミリーだけのコピーになるため）と
  結合文字・不可視文字。10〜19書体の帯1133字も見送り（v6検討事項）。
  v4は10305字＋スペース、v3は2290字＋スペース、v2は174字＋スペースのみだった。

## 再現方法

```sh
cd work
python3 download_fonts.py   # v1: 83ファイルを fonts/ に取得（約390MB）
python3 download_fonts_v2.py  # v2: 追加107ファイルを fonts/ に取得（計190ファイル・約1.1GB）
python3 render_average.py   # 平均PNG174枚を out/glyphs/ に生成
python3 make_sheets.py      # コンタクトシート生成
python3 make_viewer.py      # out/viewer.html 生成
./venv/bin/python build_ttf.py  # TTF生成（work/venv に opencv＋fontTools が必要）

# v3（常用漢字2136字・2290字、適応しきい値）
./venv/bin/python render_average_v3.py  # 平均PNG2290枚を out/glyphs_v3/ に生成（約23分）
./venv/bin/python build_ttf_v3.py       # 適応しきい値で AverageFont-Regular-v3-229fonts-2290chars.ttf を生成
./venv/bin/python make_sheets_v3.py     # コンタクトシート・前後比較・組版テスト・viewer_v3.html 生成

# v4（JIS X 0213漢字10050字・10305字、適応しきい値＋format-12 cmap）
./venv/bin/python render_average_v4.py  # 平均PNG10305枚を out/glyphs_v4/ に生成（約89分、チャンク単位で再開可能）
./venv/bin/python build_ttf_v4.py       # 適応しきい値で AverageFont-Regular-v4-229fonts-10305chars.ttf を生成
./venv/bin/python make_sheets_v4.py     # コンタクトシート・前後比較・組版テスト（豆腐assertつき）・viewer_v4.html 生成

# v5（proper20・18414字、v4のPNGを流用し新規8109字だけ描画）
./venv/bin/python render_average_v5.py  # 平均PNG8109枚を out/glyphs_v5/ に追加生成（約25分、チャンク単位で再開可能）
./venv/bin/python build_ttf_v5.py       # 適応しきい値で AverageFont-Regular-v5-229fonts-18414chars.ttf を生成
./venv/bin/python make_sheets_v5.py     # コンタクトシート・前後比較・組版テスト（豆腐assertつき）・viewer_v5.html 生成
```

## 検証

- 平均化（v2）：229書体 × 174字、寄与数 min 227 / max 229
  （かな92字は228、英数字62字は229、漢字20字は227）。
- TTF（v2）：fontTools で再読込し、グリフ176個（.notdef＋space＋174字）、
  cmap 175エントリを確認。Pillow でテスト組版し、目視で文字が読めることを確認
  （`out/ttf_test.png`）。
- 平均化（v3）：229書体 × 2290字、寄与数 min 200 / max 229
  （かな92字は228、英数字62字は229、漢字2136字は200〜227）。
  平均インク最大値は全字157以上（漢字の中央値251）。
  薄い字28字（最大値210未満）を `out/stats_v3.json` の `faint` に記録。
- TTF（v3）：fontTools で再読込し、グリフ2292個
  （.notdef＋space＋2290字）、cmap 2291エントリを確認。
  空グリフ0個、常用漢字2136字の欠落0字、v2の174字の欠落0字。
  アウトライン点数はグリフあたり11〜243点（中央値124）。
  Pillow でテスト組版し、豆腐なし・薄い24字の行も含めて目視で読めることを確認
  （`out/ttf_test_v3.png`）。前後比較は `out/faint_before_after_v3.png` で目視確認済み。
- 平均化（v4）：229書体 × 10305字、寄与数 min 94 / max 229
  （ひらがな82字は227〜228、カタカナ83字は208〜228、句読点28字は202〜229、
  漢字10050字は94〜228。水準別： 第1水準 min 217・中央値227、
  第2水準 min 179・中央値216、第3水準 min 110・中央値123、
  第4水準 min 94・中央値120。非BMP 303字も min 100）。
  寄与0の字は0字。平均インク最大値は全字145以上。
  薄い字64字（最大値210未満）を `out/stats_v4.json` の `faint` に記録。
- TTF（v4）：fontTools で再読込し、グリフ10307個
  （.notdef＋space＋10305字）、cmap 10306エントリを確認。
  cmap は format 4＋format 12 の2副表で、非BMP 303字も cmap にある。
  空グリフ0個、v3の2290字の欠落0字、v4の10305字の欠落0字。
  アウトライン点数はグリフあたり9〜309点（中央値144）。
  Pillow でテスト組版し、追加字の文（「じ」「太陽」「重要」・濁音・小さい仮名・
  長音・繰り返し記号・句読点・第3／第4水準漢字・人名用漢字）を含めて
  豆腐なし・目視で読めることを確認（`out/ttf_test_v4.png`）。
  豆腐チェックはスクリプト内の assert でも0件。
  前後比較は `out/faint_before_after_v4.png`・
  `out/fewest_before_after_v4.png` で目視確認済み。
- 平均化（v5）：229書体 × 新規8109字、寄与数 min 20 / max 229
  （全18414字では min 20・中央値122・max 229）。
  グループ別（新規分）: 漢字3912（min 21・中央値86）、記号1173、囲み895、
  ラテン拡張336、キリル260、ラテン拡張追加256、IPA 233、ギリシア拡張233、
  数学188、半角121、ギリシア120、矢印95、ラテン1 92、全角91、ヘブライ35、
  半角句読点32、仮名拡張16、カタカナ12、ひらがな9。
  寄与0の字は0字。薄い字（max_ink<210）は373字。
- TTF（v5）：fontTools で再読込し、グリフ18416個
  （.notdef＋space＋18414字）、cmap 18415エントリを確認。
  cmap は format 4（17741エントリ・BMP）＋format 12（18415エントリ・全字）の2副表で、
  非BMP 674字も cmap にある。
  空グリフ0個、v4の10305字の欠落0字、新規8109字の欠落0字。
  Pillow でテスト組版し、追加字の文（半角英文・全角・ギリシア・キリル・
  JIS X 0212漢字・囲み・矢印・数学記号・拡張B）を含めて
  豆腐なし・目視で読めることを確認（`out/ttf_test_v5.png`）。
  豆腐チェックはスクリプト内の assert でも0件。
  前後比較は `out/faint_before_after_v5.png`・
  `out/fewest_before_after_v5.png` で目視確認済み。
