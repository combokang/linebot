#!venv/bin/python

# 載入需要的模組
import os
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import psycopg2
import json


'''
參數：
line_bot_api:           line_bot_api物件
conn:                   資料庫連線
event:                  message_api事件
user_id:                使用者ID
text:                   使用者輸入內容
status                  使用者搜尋狀態
tdee                    紀錄tdee
'''

# 計算 tdee
# 辨認是男生或女生


def count_tdee(line_bot_api, conn, event, user_id, text, status):
    # 紀錄參數 tdee
    tdee = 0
    # 找出使用者的基礎資料
    cursor = conn.cursor()
    print("找出使用者的基礎資料")
    SQL_order = f'''
    select gender, high, weight, age, activity from userinfo where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    print("SQL找出使用者的基礎資料 成功")
    search_result = cursor.fetchone()
    print(search_result)
    [gender_result, high_result, weight_result,
        age_result, activity_result] = search_result

    if gender_result == "女":
        if activity_result == "低":
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender_result}{activity_result}")
            SQL_order = f'''
            update userinfo set tdee = ((9.6*{weight_result}) + (1.8*{high_result}) - (4.7*{age_result}) + 655)*1.2 where userid = '{user_id}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
        elif activity_result == "中":
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender_result}{activity_result}")
            SQL_order = f'''
            update userinfo set tdee = ((9.6*{weight_result}) + (1.8*{high_result}) - (4.7*{age_result}) + 655)*1.55 where userid = '{user_id}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
        else:
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender_result}{activity_result}")
            SQL_order = f'''
            update userinfo set tdee = ((9.6*{weight_result}) + (1.8*{high_result}) - (4.7*{age_result}) + 655)*1.9 where userid = '{user_id}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
    else:
        if activity_result == "低":
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender_result}{activity_result}")
            SQL_order = f'''
            update userinfo set tdee = ((13.7*{weight_result}) + (5*{high_result}) - (6.8*{age_result}) + 66)*1.2 where userid = '{user_id}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
        elif activity_result == "中":
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender_result}{activity_result}")
            SQL_order = f'''
            update userinfo set tdee = ((13.7*{weight_result}) + (5*{high_result}) - (6.8*{age_result}) + 66)*1.55 where userid = '{user_id}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
        else:
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫

            cursor = conn.cursor()
            print(f"紀錄tdee：{gender_result}{activity_result}")
            SQL_order = f'''
            update userinfo set tdee = ((13.7*{weight_result}) + (5*{high_result}) - (6.8*{age_result}) + 66)*1.9 where userid = '{user_id}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
    print("SQL更新userinfo狀態:計算tdee 成功")
    SQL_order = f'''
    select tdee from userinfo where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    tdee_result = cursor.fetchone()[0]
    print(f"更新後的tdee: {tdee_result}")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f"計算完成！您的TDEE為{tdee_result}"))
