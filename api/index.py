from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
import os
import time
import threading

line_bot_api = LineBotApi(os.getenv(“LINE_CHANNEL_ACCESS_TOKEN”))
line_handler = WebhookHandler(os.getenv(“LINE_CHANNEL_SECRET”))
working_status = os.getenv(“DEFALUT_TALKING”, default=“true”).lower() == “true”

app = Flask(**name**)
chatgpt = ChatGPT()

# 用於追蹤對話輪數

conversation_count = 0

@app.route(’/’)
def home():
return ‘Hello, World!’

@app.route(”/webhook”, methods=[‘POST’])
def callback():
signature = request.headers[‘X-Line-Signature’]
body = request.get_data(as_text=True)
app.logger.info(“Request body: “ + body)
try:
line_handler.handle(body, signature)
except InvalidSignatureError:
abort(400)
return ‘OK’

def send_messages_with_delay(user_id, messages, delay=2):
“”“分段發送訊息的函數”””
def send_delayed():
for i, msg in enumerate(messages):
if i > 0:  # 第一條訊息不延遲
time.sleep(delay)
line_bot_api.push_message(user_id, TextSendMessage(text=msg))

```
# 使用執行緒避免阻塞webhook
thread = threading.Thread(target=send_delayed)
thread.start()
```

def split_response(text, max_length=100):
“”“將長回覆拆分成多段”””
if len(text) <= max_length:
return [text]

```
# 按句號、問號、驚嘆號分割
sentences = []
current = ""

for char in text:
    current += char
    if char in ['。', '？', '！', '…', '~']:
        sentences.append(current.strip())
        current = ""

if current.strip():
    sentences.append(current.strip())

# 組合短句，避免太多段
result = []
current_group = ""

for sentence in sentences:
    if len(current_group + sentence) > max_length and current_group:
        result.append(current_group.strip())
        current_group = sentence
    else:
        current_group += sentence

if current_group.strip():
    result.append(current_group.strip())

return result if result else [text]
```

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
global working_status, conversation_count

```
if event.message.type != "text":
    return

user_id = event.source.user_id

if event.message.text == "說話":
    working_status = True
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ ")
    )
    return

if event.message.text == "閉嘴":
    working_status = False
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <")
    )
    return

if event.message.text == "總結":
    # 手動觸發總結
    try:
        summary = chatgpt.get_summary()
        chatgpt.apply_summary(summary)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已完成對話總結，繼續我們的對話吧～")
        )
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="總結時發生錯誤，請稍後再試")
        )
    return

if working_status:
    try:
        # 增加對話計數
        conversation_count += 1
        
        # 添加用戶訊息
        chatgpt.add_msg(event.message.text, "user")
        
        # 獲取AI回應
        reply_msg = chatgpt.get_response()
        
        # 添加AI回應到對話歷史
        chatgpt.add_msg(reply_msg, "assistant")
        
        # 分段發送回應
        messages = split_response(reply_msg)
        
        if len(messages) == 1:
            # 單條訊息用reply
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=messages[0])
            )
        else:
            # 多條訊息用push，先回覆一個確認
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=messages[0])
            )
            
            # 其餘訊息延遲發送
            if len(messages) > 1:
                send_messages_with_delay(user_id, messages[1:], delay=1.5)
        
        # 每20輪對話自動總結
        if conversation_count >= 20:
            try:
                summary = chatgpt.get_summary()
                chatgpt.apply_summary(summary)
                conversation_count = 0  # 重置計數
                
                # 發送總結完成通知（延遲發送避免打斷對話）
                time.sleep(3)
                line_bot_api.push_message(
                    user_id,
                    TextSendMessage(text="（已自動整理對話記憶）")
                )
            except Exception as e:
                print(f"自動總結失敗: {e}")
                
    except Exception as e:
        print(f"處理訊息時發生錯誤: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，我現在有點狀況，稍等一下再跟我說話好嗎？")
        )
```

if **name** == “**main**”:
app.run()
