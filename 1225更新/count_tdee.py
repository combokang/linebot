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
'''

# 計算 tdee
# 辨認是男生或女生


def count_tdee(line_bot_api, conn, event, user_id, text, status):
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

    # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
    print(f"紀錄tdee：{gender_result}{activity_result}")
    if gender_result == "女":
        if activity_result == "低":
            tdee = (9.6*weight_result + 1.8 *
                    high_result - 4.7*age_result + 655)*1.2
        elif activity_result == "中":
            tdee = (9.6*weight_result + 1.8 *
                    high_result - 4.7*age_result + 655)*1.55
        else:  # =='高'
            tdee = (9.6*weight_result + 1.8 *
                    high_result - 4.7*age_result + 655)*1.9
    else:  # =='男'
        if activity_result == "低":
            tdee = (13.7*weight_result + 5 *
                    high_result - 6.8*age_result + 66)*1.2
        elif activity_result == "中":
            tdee = (13.7*weight_result + 5 *
                    high_result - 6.8*age_result + 66)*1.55
        else:  # =='高'
            tdee = (13.7*weight_result + 5 *
                    high_result - 6.8*age_result + 66)*1.9
    SQL_order = f'''
    UPDATE userinfo set tdee = {tdee}, today_kal_left = {tdee} ,status = '計算tdee' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:計算tdee 成功")
    # 如果是第一次設定，要將userid加入activities表中
    SQL_order = f'''
    SELECT userid from userinfo where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    user_id_in_activities = cursor.fetchone()
    if user_id_in_activities is None:
        SQL_order = f'''
        INSERT into activities(userid) VALUES('{user_id}');
        '''
        cursor.execute(SQL_order)
        conn.commit()
    print(f"更新後的tdee: {tdee}")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f"計算完成！您的TDEE為{tdee}卡"))
