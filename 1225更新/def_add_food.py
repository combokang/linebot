# 載入需要的模組
import os
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import psycopg2
import json
import flex_add_confirm

'''
參數：
line_bot_api:           line_bot_api物件
conn:                   資料庫連線
event:                  message_api事件
user_id:                使用者ID
text:                   使用者輸入內容
status                  使用者搜尋狀態
'''


# 定義涵式：新增食物
def add_food(line_bot_api, conn, event, user_id, text, status):
    # 更新使用者搜尋狀態為新增食物品項
    cursor = conn.cursor()
    print(f"輸入字串：{text}")
    SQL_order = f'''
    UPDATE userinfo set status = '定義食物名稱' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:定義食物名稱 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請輸入食物名稱")
    )


# 定義涵式：定義食物名稱
def food_name(line_bot_api, conn, event, user_id, text, status):
    cursor = conn.cursor()
    print(f"輸入字串：{text}")
    SQL_order = f'''
    UPDATE activities set food_name = '{text}' where userid = '{user_id}';
    UPDATE userinfo set status = '定義單位' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新activities表與userinfo狀態:定義單位 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請輸入每份食物的單位，如「份」、「100克」等等")
    )


# 定義涵式：定義單位
def food_unit(line_bot_api, conn, event, user_id, text, status):
    cursor = conn.cursor()
    print(f"輸入字串：{text}")
    SQL_order = f'''
    UPDATE activities set unit = '{text}' where userid like '%{user_id}%';
    UPDATE userinfo set status = '定義熱量' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新activities表與userinfo狀態:定義熱量 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請輸入每單位食物的熱量(卡數)，如100、200等等")
    )


# 定義涵式：定義熱量
def food_kal(line_bot_api, conn, event, user_id, text, status):
    try:
        kal = float(text)
        if kal > 0:
            cursor = conn.cursor()
            SQL_order = f'''
            UPDATE activities set kal = {kal} where userid = '{user_id}';
            UPDATE userinfo set status = '確認是否建立' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新activities表與userinfo狀態:確認是否建立 成功")
            SQL_order = f'''
            SELECT food_name, unit, kal from activities where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            [food_name_add, unit_add, kal_add] = cursor.fetchone()
            cursor.close()
            FlexMessage = flex_add_confirm.confirm_json(
                unit_add, food_name_add, kal_add)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage('search_confirm', FlexMessage)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="請輸入正值！"))
    except ValueError:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入數值！"))


# 定義涵式：確認是否建立
def confirm(line_bot_api, conn, event, user_id, text, status):
    if text == "[建立食物並扣除]":
        cursor = conn.cursor()
        SQL_order = f'''
        SELECT food_name, unit, kal from activities where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        [food_name_add, unit_add, kal_add] = cursor.fetchone()
        cursor.execute(SQL_order)
        SQL_order = f'''
        SELECT food_name, unit, kal from food_calories 
        where food_name = '{food_name_add}' and unit = '{unit_add}' and kal = {kal_add};
        '''
        cursor.execute(SQL_order)
        same_data_exist = cursor.fetchone()
        # 如果沒有這筆食物資料，建立他
        if same_data_exist is None:
            SQL_order = f'''
            INSERT into Food_Calories(food_name,unit,kal)
            VALUES('{food_name_add}','{unit_add}','{kal_add}');
            '''
            cursor.execute(SQL_order)
            conn.commit()
        SQL_order = f'''
        UPDATE userinfo set status = '輸入數量' where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新userinfo狀態:輸入數量 成功")
        cursor.close()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入食物數量"))
    elif text == "[建立食物]":
        cursor = conn.cursor()
        SQL_order = f'''
        SELECT food_name, unit, kal from activities where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        [food_name_add, unit_add, kal_add] = cursor.fetchone()
        cursor.execute(SQL_order)
        SQL_order = f'''
        SELECT food_name, unit, kal from food_calories 
        where food_name = '{food_name_add}' and unit = '{unit_add}' and kal = {kal_add};
        '''
        cursor.execute(SQL_order)
        same_data_exist = cursor.fetchone()
        # 如果沒有這筆食物資料，建立他
        if same_data_exist is None:
            SQL_order = f'''
            INSERT into Food_Calories(food_name,unit,kal)
            VALUES('{food_name_add}','{unit_add}','{kal_add}');
            '''
            cursor.execute(SQL_order)
            conn.commit()
        SQL_order = f'''
        UPDATE userinfo set status = '建立成功' where userid = '{user_id}';
        '''
        cursor.execute(SQL_order)
        conn.commit()
        print("SQL更新userinfo狀態:建立成功 成功")
        cursor.close()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="食物資料建立成功！"))


# 取消建立
def cancel(line_bot_api, conn, event, user_id, text, status):
    cursor = conn.cursor()
    SQL_order = f'''
    UPDATE userinfo set status = '建立失敗' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()
    print("SQL更新userinfo狀態:建立失敗 成功")
    cursor.close()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="已取消建立食物資料"))
