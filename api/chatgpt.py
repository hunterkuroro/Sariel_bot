
import os
from openai import OpenAI
from api.prompt import Prompt

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4o")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1800))
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self):
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

    def add_msg(self, text):
        self.prompt.add_msg(text)
