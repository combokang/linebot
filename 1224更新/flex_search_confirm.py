def confirm_json(unit_result, food_name_result, kal_result):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"每{unit_result}{food_name_result}含有{kal_result}卡的熱量，確定要把這餐的熱量紀錄下來嗎？",
                    "wrap": True,
                    "color": "#000000"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "確定",
                        "text": "[確定紀錄]"
                    },
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "取消",
                        "text": "[取消紀錄]"
                    },
                    "height": "sm"
                }
            ],
            "paddingAll": "xs",
            "paddingTop": "xs",
            "paddingBottom": "xs",
            "paddingStart": "xs",
            "paddingEnd": "xs"
        }
    }
