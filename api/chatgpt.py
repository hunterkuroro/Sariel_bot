import os
import openai
from api.prompt import Prompt

# 設定 API 金鑰：新版用法
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        # 模型預設為 gpt-4o；若有需要，可在環境變數中調整
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4o")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1800))
        
    def get_response(self):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0]["message"]["content"]

    def add_msg(self, text):
        self.prompt.add_msg(text)
