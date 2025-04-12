import openai
import os
from api.prompt import Prompt

# 設定 API 金鑰（新版用法）
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        # 設定模型，若環境中未設定，預設使用 gpt-4o 模型
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4o")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1600))
        # 定義上下文保存的最大訊息數，超過此數量時觸發摘要
        self.context_limit = int(os.getenv("CONTEXT_LIMIT", default=20))

    def summarize_context(self, messages):
        """
        將傳入的訊息列表進行摘要，要求控制在 900 字以內，
        並回傳生成的摘要文字。
        """
        # 將每則訊息轉換成 "role: content" 格式字串後合併
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        prompt_text = f"請總結下列對話內容，保留關鍵信息與情感脈絡，並精簡重點（請控制在900字以內）：\n{conversation_text}"
        try:
            summary_response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.5,
                max_tokens=1800,
            )
            summary = summary_response["choices"][0]["message"]["content"].strip()
            return summary
        except Exception as e:
            return ""

    def get_response(self):
        """
        取得回應前，先檢查上下文如果超過預定數量，則進行摘要，
        確保不會超出模型的 token 限制，再呼叫 OpenAI API 取得回覆。
        """
        messages = self.prompt.generate_prompt()
        # 當訊息數大於 context_limit 時，摘要除系統提示與最後兩條之外的對話
        if len(messages) > self.context_limit:
            # 取除第一則系統提示及最後兩則對話的中間部分進行摘要
            old_messages = messages[1:-2]
            summary = self.summarize_context(old_messages)
            if summary:
                # 用摘要訊息取代舊的對話內容，保留系統提示與最近兩則
                new_messages = [messages[0], {"role": "assistant", "content": f"摘要：{summary}"}] + messages[-2:]
                # 更新 prompt 中的訊息列表
                self.prompt.msg_list = new_messages
                messages = new_messages

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            reply = response["choices"][0]["message"]["content"]
            return reply
        except Exception as e:
            return f"出錯了：{str(e)}"

    def add_msg(self, text):
        self.prompt.add_msg(text)

