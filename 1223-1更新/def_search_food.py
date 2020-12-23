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


# 定義涵式：紀錄熱量
def kal_record(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為輸入關鍵字
    cursor = conn.cursor()
    print(f"輸入字串：{text}")
    SQL_order = f'''
    update userinfo set status = '輸入關鍵字' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:輸入關鍵字 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入食物名稱"))


# 定義涵式：輸入關鍵字
def search_food(line_bot_api, conn, event, user_id, text, status):
    cursor = conn.cursor()
    search_query = text
    print(f"搜尋字串: {search_query}")
    SQL_order = f'''
    select food_name,kal,unit from Food_Calories where food_name like '%{search_query}%';
    '''
    cursor.execute(SQL_order)
    print("SQL搜尋Food_Calories成功")
    search_result = cursor.fetchone()
    print(search_result)

    # 判斷資料庫是否已有此食物資料
    if search_result is None:
        # 更新使用者搜尋狀態為紀錄失敗
        SQL_order = f'''
        update userinfo set status = '紀錄失敗' where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新userinfo狀態:紀錄失敗 成功")
        cursor.close()
        FlexMessage = json.load(
            open('flex_cant_find.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('cant_find', FlexMessage))
    else:
        # 更新使用者搜尋狀態為搜尋成功
        [food_name_result, kal_result, unit_result] = search_result
        SQL_order = f'''
        update activities set food_name = '{food_name_result}', kal = '{kal_result}' where userid = '{user_id}';
        update userinfo set status = '搜尋成功' where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新activities資料、userinfo狀態:搜尋成功 成功")
        cursor.close()
        FlexMessage = flex_search_confirm.confirm_json(
            unit_result, food_name_result, kal_result)
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('search_confirm', FlexMessage))


# 定義涵式：確定紀錄
def confirm(line_bot_api, conn, event, user_id, text, status):
    cursor = conn.cursor()
    SQL_order = f'''
    update userinfo set status = '輸入數量' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:輸入數量 成功")
    cursor.close()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入食物數量"))


# 定義涵式：取消紀錄
def cancel(line_bot_api, conn, event, user_id, text, status):
    cursor = conn.cursor()
    SQL_order = f'''
    update userinfo set status = '紀錄失敗' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:紀錄失敗 成功")
    cursor.close()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="已取消紀錄熱量"))


# 定義涵式：紀錄數量
def quantity_record(line_bot_api, conn, event, user_id, text, status):
    # 還沒排除負數
    try:
        quantity = float(text)
        cursor = conn.cursor()
        SQL_order = f'''
        select kal from activities where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        kal_result = cursor.fetchone()[0]
        print(f"SQL搜詢成功，kal: {kal_result}")
        total_kal = kal_result * quantity
        SQL_order = f'''
        update userinfo set today_kal_left = today_kal_left - {total_kal},status = '紀錄成功' 
        where userid = '{user_id}';
        select today_kal_left from userinfo where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新userinfo狀態:紀錄成功 成功")
        today_kal_left = cursor.fetchone()[0]
        cursor.close()
        if today_kal_left >= 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"已成功紀錄熱量，您今日的熱量扣打剩餘{today_kal_left}卡"))
        else:
            kal_exceed = 0 - today_kal_left
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"已成功紀錄熱量，您已超過預定熱量上限{kal_exceed}卡了，不行再吃囉！"))
    except ValueError:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入數值"))
