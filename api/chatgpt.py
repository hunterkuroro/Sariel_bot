from api.prompt import Prompt
import os
import openai

client = openai
client.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4o")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=500))
        # 設定上下文數量上限，超過此數量時進行摘要
        self.context_limit = 15

    def summarize_context(self, messages):
        """
        將傳入的 messages 列表內容（通常是不再需要保留原文的對話歷史）摘要成一段精簡文字，
        保留關鍵信息與情感脈絡。
        """
        # 將每則消息轉換成 "role: content" 格式字串後合併
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        prompt_text = f"請總結下列對話內容，保留關鍵信息與情感脈絡，並精簡重點：\n{conversation_text}"
        try:
            summary_response = client.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.5,
            )
            summary = summary_response["choices"][0]["message"]["content"].strip()
            return summary
        except Exception as e:
            # 若摘要失敗，直接回傳空字串
            return ""

    def get_response(self):
        # 取得完整的對話消息列表
        messages = self.prompt.generate_prompt()
        # 若消息數超過設定上限，則摘要舊的消息
        if len(messages) > self.context_limit:
            # 取出除系統 prompt 以外的部分進行摘要（這邊以 [1:-2] 範圍為例，可根據需要調整）
            old_messages = messages[1:-2]
            summary = self.summarize_context(old_messages)
            if summary:
                # 以摘要訊息取代舊的訊息，僅保留系統 prompt 與最近兩條消息
                new_messages = [messages[0], {"role": "assistant", "content": f"摘要：{summary}"}] + messages[-2:]
                # 更新上下文消息
                self.prompt.msg_list = new_messages
                messages = new_messages

        try:
            response = client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            reply = response["choices"][0]["message"]["content"]
            return reply
        except Exception as e:
            return f"出錯了：{str(e)}"

    def add_msg(self, text):
        self.prompt.add_msg(text)
