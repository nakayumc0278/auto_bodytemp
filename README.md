# auto_bodytemp

## はじめに
みなさんこんにちは、最近どんどん寒くなりますね。
コロナ真っただ中ですが、私の学校では毎日検温し、その結果を毎朝フォームに送信することになっています。
ですが、最近どうも最近送信率が低いらしく、先生がこんなことを言い始めました。

__「毎日検温の結果を送らないと授業を欠席扱いにする」__

私は普段朝6時30分に起き、そのまま着替えを済まして急いで7時に駅に向かうので検温をする暇なんてありません。
もっと早く早起きすればいい話ですが早く起きてフォームで送信なんかしたくない...
__(ちゃんと検温はしています)__

なので朝7時くらいに、__高すぎない普通の体温__で指定のフォームに自動で入力して送信してくれるプログラムを作りました。

## この記事の概要
* Windows で動作させる。
* Anaconda3 の pipを用いてライブラリのインストールをする。
* タスクスケジューラで毎日7時に起動させる。
* ログインが必要なGoogleフォームで送信する。
* PillowとOpenCVを使って送信時刻と体温を画像で出力させる。

## 自分の環境
* OS: Windows10 Pro 64ビット (Version 20H2)
* CPU: Intel Core i7-6700
* メモリ: 16GB

## 使用したアプリ
* Anaconda3-2020.10
* Visual Studio Code
* Google Chrome 87.0.4280.66（Official Build)

## 使用するライブラリ
* selenium 3.141.0
* chromedriver-binary 87.0.4280.20.0
* opencv-python 4.4.0.46
* pillow 8.0.1

## Anaconda Prompt (管理者)を起動する
pipのアップデートがあるか確認

```bash:pipの更新
pip install --upgrade pip
```

ブラウザの操作を自動化するseleniumをインストールします。

```bash:seleniumのインストール
pip install selenium
```

## chromeバージョン更新と確認

なるべく更新してほしいのですが、[chrome://settings/help](chrome://settings/help) で確認してください。
![無題.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/a1ca1937-8959-3972-200b-713fb951ce2e.png)

更新したくない場合[chrome://version](chrome://version/)で確認できます。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/6a475aa7-9df3-230f-8591-fd8e0cc61b6c.png)

今回の私の環境でのバージョンは「87.0.4280.66」でした。
なのでこの「87.0.4280.66」を使ってインストールしていきます。

```bash:WebDriverのインストール
#バージョンによってこの数字を変える 
pip install chromedriver-binary==87.0.4280.66
```

するとこんなエラーが出ました。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/0b7bb048-946b-5516-1a4a-34c4164057ae.png)
そんなバージョンなんてないぞ と怒られてしまいました。

なのでこの赤文字の中から青線で囲った一番最新のバージョンを指定します。
__更新していない方はそのバージョンに一番近いものを選んでください。__

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/fc817bfe-69dd-0b3a-4e95-85c2c7f32442.png)
インストールできたら環境構築完了です。

##Seleniumを使ってフォームを送信させる

Google Formはフォームに各質問を識別させる番号ありURLの最後にパラメータを付加させることで質問の値を入力した状態でURLを開くことができます。

このフォームではメールアドレスを取得しない設定なのでこのフォームでスクリプトを試す場合は __下欄のログイン処理の箇所をコメントアウト__ してください。

https://docs.google.com/forms/d/e/1FAIpQLSf82M_QmbdzwphCwID2WyTwQAXbTlep89z5Lj-uB0NDX3ZFVQ/viewform?entry.366340186=36.

上記リンクを開くとわかるように、```entry.366340186=36.```を付け足すことで、最初から入力できていると思います。

黒枠で囲ったところが識別番号です。F12キーを押し検証画面で質問のdivを探し、以下のような番号を探します。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/5ce25bea-c3b4-ebf4-0944-15f9d495cb8a.png)

番号が探せたら```entry.識別番号=値```の形でパラメータを付加させます。これを応用させて、seleniumを使って毎日ランダムで温度を送信できるようにします。

## コードの意味

```py:体温をランダムで選択
# 体温を36.1~36.7の中からランダムで選ばせる
bodytemp = str(36 + random.randint(0, 7) / 10)

# 送信したいフォームのURLを指定
url = 'https://docs.google.com/forms/d/e/1FAIpQLSf82M_QmbdzwphCwID2WyTwQAXbTlep89z5Lj-uB0NDX3ZFVQ/viewform?entry.366340186=' + bodytemp
```

URLが完成したら、あとはSeleniumでURLを開いて送信ボタンを押してもらうだけですね。

なお、ログインが必要なフォームな場合は毎回ログインが必要なので自動でログインする機能も実装しています。
__ログインする必要がないフォームの場合は、これらをコメントアウトしてください__

```py:ログイン処理
# メールアドレス指定
login_id = "メールアドレス" #ここに入力する
email_form = driver.find_element_by_name("identifier")
email_form.send_keys(login_id)
email_form.send_keys(Keys.ENTER)
time.sleep(1)

# パスワード指定
login_pw = "パスワード" #ここに入力する
passwd_form = driver.find_element_by_name("password")
passwd_form.send_keys(login_pw)
passwd_form.send_keys(Keys.ENTER)
time.sleep(1)
```

## 送信した時刻と体温を画像に出力させる
ちゃんと動作して送信できていても、毎日送信できているか心配ですよね...
なので送れているのかを確認するために、送信完了画面のキャプチャを撮ってもらい、OpenCVとPILを使って時刻と送信時の体温を入力する機能を実装しました。画像がなければ何かしらのエラーが起きていて、送れていないことがわかります。

```py:日付と送信体温を入れる
# スクショ
driver.save_screenshot("temp.png")

# 画像に文字を入れる関数
def img_add_msg(img, message):
    font_path = "C:\Windows\Fonts\meiryo.ttc"  # Windowsのフォントファイルへのパス
    font_size = 24  # フォントサイズ
    font = ImageFont.truetype(font_path, font_size)  # PILでフォントを定義
    img = Image.fromarray(img)  # cv2(NumPy)型の画像をPIL型に変換
    draw = ImageDraw.Draw(img)  # 描画用のDraw関数を用意

    # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
    draw.text((50, 500), message, font=font, fill=(0, 0, 0, 0))  
    img = np.array(img)  # PIL型の画像をcv2(NumPy)型に変換
    return img  # 文字入りの画像をリターン

img2 = cv2.imread("temp.png", 1)  # 画像読み込み
cr = "\n"
mail = "メール: "
dt_now = datetime.datetime.now()  # 時刻取得
char1 = "送信時間: "
char2 = " ℃で送信しました。"
message = (char1 + dt_now.strftime("%Y年%m月%d日 %H:%M:%S\n") + (body_temp) + char2)  # 画像に入れる文章
img = img_add_msg(img2, message)  # img_add_msgを実行

cv2.imwrite(("./a.png"), img)  # 画像書き込み
cv2.waitKey(0)
cv2.destroyAllWindows()

os.rename("./a.png", "{0:%Y%m%d_%H%M%S}.png".format(dt_now))  # 時刻にリネーム
os.remove("temp.png")  # 一時ファイルを削除
```
正常に送れるとこのような画像ができあがりました。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/256a2e2e-a83d-3851-d38a-d35bbbb02b32.png)

## タイムスケジューラで7時～8時までにランダムで起動

プログラムも正常に動いたら、いよいよタイムスケジューラで自動的に起動して送信してもらいます。

[Win]+[R]を押して「control schedtasks」と入力を押して、[OK]を押します。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/e5e4175a-5b25-a842-ad13-22051c652543.png)

起動できたら左側の「タスクスケジューラライブラリ」に移動して、右の「基本タスク作成」をクリックします。
![10キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/bfc03550-2ea6-fa3c-6a0d-2c4c2378870a.png)

基本タスクの作成画面が出たら、適当に名前をつけてください。

![キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/f8f76401-98b9-a67f-08f4-fbd50b948a35.png)

毎日送るので、[毎日(D)] にします。

![1キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/f7a1c48f-28d3-0b3c-8637-f6794277cc66.png)

これは何もいじらず次へ

![2キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/cde0ae78-e60b-e5bf-a04c-0e99f279fcf7.png)

これも次へ

![3キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/dca4fed6-8923-9d56-4634-99ddb9ade027.png)

これは、PATHが通っていれば[python.exe]です。通っていない方は、pythonの場所を指定してください。

![4キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/2ca3e0a0-6deb-1461-0642-c5c40b3dcc76.png)

今回私は Desktop に体温というフォルダーを作り、その中に実行プログラムが置いてあります。

![a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/bcbcbe8a-520c-87ba-a5ba-bb676bc84b5f.png)

なので、引数と開始は

```:引数
#プログラムファイルを指定
C:\Users\ユーザ名\Desktop\体温\auto_bodytemp.py
```

```:開始
#そのプログラムがあるフォルダを指定
C:\Users\ユーザ名\Desktop\体温
```

になります。

まだ設定することがあるので、
__[完了]をクリックしたときに、このタスクの[プロパティ]ダイアログを開く__
をクリックしてから完了をクリックしてください。

![5キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/0bc43375-7d91-4143-71cb-66909538c7ad.png)

するとこの画面が出てきます。

![6キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/664f5e22-f54f-8fd3-34fb-71ec0228abe7.png)

[トリガー]タブに移動して、編集(E)をクリックします。

![7キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/cb373d02-a2a1-97f8-a5c5-27f4ec00d365.png)

設定項目ですが、

* タスクの開始は [スケジュールに従う] 
* 設定が [毎日]、開始が今日にして、7時に起動するので [7:00:00] にする
* 間隔は [1日] にする
* 詳細設定の [遅延時間を指定する(ランダム)] にチェックを入れて、[1時間] に設定する
* [有効] にチェックを入れないと詳細設定が動きません。

すべてできたらOKを押します。

![8キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/857c3a2a-0986-9935-e2fb-5a447f1983a1.png)

次は、[設定] タブに移動して、これらを設定してください。

* タスク要求時に実行する
* スケジュールっされた時刻にタスクを開始できなかった場合、すぐにタスクを実行する
* タスクが失敗した場合の再起動の間隔 は1分間で再起動試行の最大数は5回
* タスクを停止するまでの時間は1時間
* 要求時に実行中のタスクが終了しない場合、タスクを強制的に停止する

これらが設定が出来たら終了です！　[完了]をクリックしてください。

![9キャプチャ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/533305c2-2287-aced-9043-ed981a01762a.png)

いよいよタスクを実行します！
新しく出来たタスクを右クリックして[実行する]をクリックしたら動作することを確認してください。

![11無題.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/545468/c3d3d0df-9792-db92-50fc-f5dfb18dc921.png)
