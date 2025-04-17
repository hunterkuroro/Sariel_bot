import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from prompt import Prompt
from chatgpt import ChatGPT
from vercel_wsgi import make_handler

app = Flask(__name__)
gpt = ChatGPT()
working_status = True

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

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
    global working_status
    user_text = event.message.text.strip()

    if user_text == "說話":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ ")
        )
        return

    if user_text == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <")
        )
        return

    if user_text == "/摘要":
        summary = gpt.prompt.get_last_summary()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"[摘要內容]\n{summary}")
        )
        return

    if not working_status:
        return

    gpt.prompt.add_msg(user_text)
    reply_text = gpt.get_response()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# vercel 專用 handler
handler = make_handler(app)