import os
from openai import OpenAI
from api.prompt import Prompt

class ChatGPT:
def **init**(self):
self.prompt = Prompt()
self.model = os.getenv(“OPENAI_MODEL”, default=“gpt-4o”)
self.temperature = float(os.getenv(“OPENAI_TEMPERATURE”, default=0))
self.max_tokens = int(os.getenv(“OPENAI_MAX_TOKENS”, default=1800))
self.openai = OpenAI(api_key=os.getenv(“OPENAI_API_KEY”))

```
def get_response(self):
    """獲取AI回應"""
    try:
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API 錯誤: {e}")
        return "抱歉，我現在無法回應，請稍後再試。"

def add_msg(self, text, role="user"):
    """添加訊息到對話歷史"""
    self.prompt.add_msg(text, role)

def get_summary(self):
    """生成對話總結"""
    try:
        # 獲取當前對話歷史
        current_messages = self.prompt.get_conversation_history()
        
        # 創建總結提示
        summary_prompt = [
            {
                "role": "system",
                "content": "請將以下對話總結成簡潔的要點，保留重要的情感狀態、話題和關鍵互動，以便後續對話能夠延續。請用第一人稱視角（Michael的視角）來總結，保持角色一致性。"
            },
            {
                "role": "user", 
                "content": f"請總結以下對話內容：\n\n{self._format_messages_for_summary(current_messages)}"
            }
        ]
        
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=summary_prompt,
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"生成總結時發生錯誤: {e}")
        return "與Anni的近期對話記錄。"

def apply_summary(self, summary):
    """應用總結，清理對話歷史"""
    self.prompt.apply_summary(summary)

def _format_messages_for_summary(self, messages):
    """格式化訊息用於總結"""
    formatted = []
    for msg in messages:
        if msg["role"] == "user":
            formatted.append(f"Anni: {msg['content']}")
        elif msg["role"] == "assistant":
            formatted.append(f"Michael: {msg['content']}")
    return "\n".join(formatted)
```
