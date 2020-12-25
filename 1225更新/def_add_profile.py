#!venv/bin/python

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
status                  使用者搜尋狀態
'''

# 定義涵式：記錄個人資料
def prfile_record(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為記錄個人資料
    cursor = conn.cursor()
    print(f"輸入字串：{text}")
    SQL_order = f'''
    select userid from userinfo where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    print("SQL搜尋 user_id 成功")
    search_result = cursor.fetchone()
    print(search_result)

    if search_result is None:
        # 更新使用者搜尋狀態為新增 user_id
        SQL_order = f'''
        insert into userinfo (userid) values ('{user_id}');
        update userinfo set status = '新增 user_id' where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新userinfo狀態:新增 user_id 成功")
        cursor.close()
        # 回傳訊息
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入性別（男/女）"))
    else:
        # 更新使用者搜尋狀態為更新 user_id
        SQL_order = f'''
        update userinfo set userid = '{user_id}' where userid = '{user_id}';
        update userinfo set status = '更新 user_id' where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新userinfo狀態:更新 user_id 成功")
        cursor.close()
        # 回傳訊息
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入性別（男/女）"))

def add_gender(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為記錄性別
    cursor = conn.cursor()
    gender = text
    print(f"輸入性別：{gender}")
    SQL_order = f'''
    update userinfo set gender = '{gender}' where userid = '{user_id}';
    update userinfo set status = '記錄性別' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:記錄性別 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入身高（只需數字）"))

def add_high(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為記錄身高
    cursor = conn.cursor()
    high = text
    print(f"輸入身高：{high}")
    SQL_order = f'''
    update userinfo set high = '{high}' where userid = '{user_id}';
    update userinfo set status = '記錄身高' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:記錄身高 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入體重（只需數字）"))

def add_weight(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為記錄體重
    cursor = conn.cursor()
    weight = text
    print(f"輸入體重：{weight}")
    SQL_order = f'''
    update userinfo set weight = '{weight}' where userid = '{user_id}';
    update userinfo set status = '記錄體重' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:記錄體重 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入年齡（只需數字）"))

def add_age(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為記錄年齡
    cursor = conn.cursor()
    age = text
    print(f"輸入年齡：{age}")
    SQL_order = f'''
    update userinfo set age = '{age}' where userid = '{user_id}';
    update userinfo set status = '記錄年齡' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:記錄年齡 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入你的活動量（低/中/高）"))

def add_activity(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為記錄活動量
    cursor = conn.cursor()
    activity = text
    print(f"輸入活動量：{activity}")
    SQL_order = f'''
    update userinfo set activity = '{activity}' where userid = '{user_id}';
    update userinfo set status = '記錄活動量' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:記錄活動量 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="是否開始計算 tdee?（請回覆：是）"))
