from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
import datetime

import chromedriver_binary
import time
import os

# 体温を36.1~36.7の中からランダムで選ぶ
body_temp = str(36 + random.randint(0, 7) / 10)

# 送信したいフォームのURLを指定

url = "ここにURLを指定する"

# Chromeで自動動作
driver = webdriver.Chrome()
driver.implicitly_wait(5)

# URLに遷移
driver.get(url)

# ログをCriticalまで表示させない
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,1024")

# メールアドレス指定
login_id = "メールアドレス"
email_form = driver.find_element_by_name("identifier")
email_form.send_keys(login_id)
email_form.send_keys(Keys.ENTER)
time.sleep(1)

# パスワード指定
login_pw = "パスワード"
passwd_form = driver.find_element_by_name("password")
passwd_form.send_keys(login_pw)
passwd_form.send_keys(Keys.ENTER)
time.sleep(1)

# GoogleFromの送信ボタンを押す
submit_button = driver.find_element_by_class_name("exportButtonContent")
submit = driver.find_element_by_class_name("appsMaterialWizButtonPaperbuttonLabel")
time.sleep(1)
submit.click()

# スクショ
driver.save_screenshot("temp.png")

# 画像に文字を入れる関数
def img_add_msg(img, message):
    font_path = "C:\Windows\Fonts\meiryo.ttc"  # Windowsのフォントファイルへのパス
    font_size = 24  # フォントサイズ
    font = ImageFont.truetype(font_path, font_size)  # PILでフォントを定義
    img = Image.fromarray(img)  # cv2(NumPy)型の画像をPIL型に変換
    draw = ImageDraw.Draw(img)  # 描画用のDraw関数を用意

    draw.text(
        (50, 500), message, font=font, fill=(0, 0, 0, 0)
    )  # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
    img = np.array(img)  # PIL型の画像をcv2(NumPy)型に変換
    return img  # 文字入りの画像をリターン


img2 = cv2.imread("temp.png", 1)  # 画像読み込み
cr = "\n"
mail = "メール: "
dt_now = datetime.datetime.now()  # 時刻取得
char1 = "送信時間: "
char2 = " ℃で送信しました。"
message = (
    mail
    + login_id
    + cr
    + char1
    + dt_now.strftime("%Y年%m月%d日 %H:%M:%S\n")
    + (body_temp)
    + char2
)  # 画像に入れる文章
img = img_add_msg(img2, message)  # img_add_msgを実行


cv2.imwrite(("./a.png"), img)  # 画像書き込み
cv2.waitKey(0)
cv2.destroyAllWindows()

os.rename("./a.png", "{0:%Y%m%d_%H%M%S}.png".format(dt_now))  # 時刻にリネーム
os.remove("temp.png")  # 一時ファイルを削除

driver.close()
driver.quit()

exit()