# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)
LOG = create_logger(app)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(
    'LtaiVqgIXfWz8+aHrYQ3FxtQrCdN5BIlY8zkiAbbdX9RkOhQdBNbFuEPkYNb5aZvdUAvoMmROd8e1xmpkFMBH97E6NXfA25TXxc+345T6TLNod7e9qKybOaL9zwrf3l+D/aYXwdZakF6t7JYECkx7AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7a0220aa2cebcbddab251a145ea08d62')

# 接收 LINE 的資訊


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    LOG.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


if __name__ == "__main__":
    app.run()
