
# 載入需要的模組
import os
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import psycopg2

'''
參數：
line_bot_api:           line_bot_api物件
conn:                   資料庫連線
event:                  message_api事件
user_id:                使用者ID
text:                   使用者輸入內容

'''


# 定義涵式：今日結算
def newday(line_bot_api, conn, event, user_id):
    print("try succeed")

    # 更新使用者剩餘熱量為TDEE
    cursor = conn.cursor()
    SQL_order = f'''
    select today_kal_left from userinfo where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    yesterday_kal_left = cursor.fetchone()[0]
    print(f"取得剩餘熱量 {yesterday_kal_left}")

    SQL_order = f'''
    select tdee from userinfo where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    TDEE = cursor.fetchone()[0]
    print(f"TDEE取得 {TDEE}")

    
    SQL_order = f'''
    update userinfo set today_kal_left = {TDEE} where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    print("更新每日熱量")
    
    
    conn.commit()
    cursor.close()
    # 回傳訊息
    if yesterday_kal_left > 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"您今日的熱量扣打其實還有{yesterday_kal_left}卡，不過就在剛剛都幫你重置啦！新的一天又開始囉"))
    elif yesterday_kal_left == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"您今日攝取的熱量當好等於TDEE，太強了！新的一天開始了繼續保持吧！"))
    else:
        kal_exceed = 0 - yesterday_kal_left
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"您的熱量扣打已重置，不過您今天超過預定熱量上限{kal_exceed}卡了，新的一天要再加油！"))

