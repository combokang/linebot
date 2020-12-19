def confirm_json(unit_add, food_name_add, kal_add):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "您即將在資料庫建立以下的食物的資料：",
                    "wrap": True,
                    "color": "#000000",
                    "contents": [],
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": f"食物名稱：{food_name_add}",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"單位：{unit_add}",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"熱量：{kal_add} 卡",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "您確定要建立嗎？",
                    "margin": "md"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "建立並從今天的扣打扣除",
                        "text": "[建立食物並扣除]"
                    },
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "建立但「不」從今天的扣打扣除",
                        "text": "[建立食物]"
                    },
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "取消建立",
                        "text": "[取消建立]"
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
