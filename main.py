# 載入需要的模組
import os
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import configparser
import psycopg2
import def_search_food
import def_add_food

# 設定應用程式
app = Flask(__name__)
LOG = create_logger(app)
config = configparser.ConfigParser()
config.read("config.ini")

# 認證
line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
handler = WebhookHandler(config.get("line-bot", "channel_secret"))


# 根路由，測試用
@ app.route("/")
def hello():
    return "hello world"


# callback路由，和line連線
@ app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    LOG.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("400 error")
        abort(400)
    return "OK"


# 文字訊息事件
@ handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # 定義常用變數
    text = event.message.text
    user_id = event.source.user_id

    # 開啟資料庫連線
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen(
    #     "heroku config:get DATABASE_URL -a linebotforkal").read()[:-1]
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")

    # 首先要在登錄tdee時就insert userid到activities表，就不用每次判斷activities表裡面有沒有這個user)
    print("user_id:", user_id)
    cursor = conn.cursor()
    SQL_order = f'''
    select status from userinfo where userid = '{user_id}'
    '''
    cursor.execute(SQL_order)
    status = cursor.fetchone()[0]
    print(f"SQL搜尋成功，user的狀態: {status}")
    cursor.close()

    # 紀錄熱量
    if text == "[紀錄熱量]":
        def_search_food.kal_record(line_bot_api, conn, event,
                                   user_id, text, status)
    # 建立資料
    elif text == "[開始建立食物資料]":
        def_add_food.add_food(line_bot_api, conn, event,
                              user_id, text, status)
    # 輸入關鍵字
    elif status == "輸入關鍵字":
        def_search_food.search_food(line_bot_api, conn, event,
                                    user_id, text, status)
    # 確定或取消紀錄
    elif status == "搜尋成功":
        def_search_food.confirm(line_bot_api, conn, event, user_id,
                                text, status)
    # 輸入數量
    elif status == "輸入數量":
        def_search_food.quantity_record(
            line_bot_api, conn, event, user_id, text, status)
    # 定義食物名稱
    elif status == "定義食物名稱":
        def_add_food.food_name(
            line_bot_api, conn, event, user_id, text, status)
    # 定義單位
    elif status == "定義單位":
        def_add_food.food_unit(
            line_bot_api, conn, event, user_id, text, status)
    # 定義熱量
    elif status == "定義熱量":
        def_add_food.food_kal(
            line_bot_api, conn, event, user_id, text, status)
    elif status == "確認是否建立":
        def_add_food.confirm(
            line_bot_api, conn, event, user_id, text, status)
    conn.close()


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
