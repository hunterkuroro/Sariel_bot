
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from api.chatgpt import ChatGPT

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
gpt = ChatGPT()

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    # 支援 /摘要 指令
    if user_text == "/摘要":
        summary = gpt.prompt.get_last_summary()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"[摘要內容]\n{summary}")
        )
        return

    # 正常 GPT 對話流程
    gpt.prompt.add_msg(user_text)
    reply_text = gpt.get_response()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
