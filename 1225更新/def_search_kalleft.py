
# 載入需要的模組
import os
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import psycopg2
import json
import flex_search_confirm

'''
參數：
line_bot_api:           line_bot_api物件
conn:                   資料庫連線
event:                  message_api事件
user_id:                使用者ID
text:                   使用者輸入內容
status                  使用者搜尋狀態
'''

# 定義涵式：搜尋剩餘熱量


def kal_left(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為查詢剩餘熱量
    cursor = conn.cursor()
    # print(f"輸入字串：{search_kalleft}")
    SQL_order = f'''
    select today_kal_left from userinfo where userid = '{user_id}' ;
    '''
    cursor.execute(SQL_order)
    print("SQL搜尋today_kal_left成功")
    search_kalleft = cursor.fetchone()[0]
    print(search_kalleft)
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f"您今天剩餘的熱量額度為：{search_kalleft}卡"))
