from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError


app = Flask(__name__)
LOG = create_logger(app)


# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(
    'vnP2yeDIi1+tTKPF0pzTOJ5S3+L6jaOW6ybNEuT9gfLKopMtRL0wH2QzMEhtxnyNdUAvoMmROd8e1xmpkFMBH97E6NXfA25TXxc+345T6TI0QO4Xc8zxu9ZWTVaySfUsjWs7/TVl6hZ311ptx4G+kQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f7f8aac1d964528176d599b1923e3dad')

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
