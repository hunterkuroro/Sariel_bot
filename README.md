# LineBot + ChatGPT + Python Flask 專案

## 簡介
這是一個使用 LineBot 和 ChatGPT 的 Python Flask 應用程式。用戶可以通過 LineBot 發送消息，並由 ChatGPT 回應。

## 安裝步驟

### 1. 克隆專案
首先，克隆此專案到本地端：
```sh
git clone https://github.com/your-repo/GitHubCopilot_LineBot.git
cd GitHubCopilot_LineBot
```

### 2. 建立虛擬環境
建議使用虛擬環境來管理依賴：
```sh
python -m venv venv
source venv/bin/activate  # 對於 Windows 使用者: venv\Scripts\activate
```

### 3. 安裝依賴
使用 `pip` 安裝所需的套件：
```sh
pip install -r requirements.txt
```

### 4. 設定環境變數
在 `config.py` 文件中設定你的 LineBot 和 OpenAI API 金鑰：
```python
LINE_CHANNEL_SECRET = '你的 LINE CHANNEL SECRET'
LINE_CHANNEL_ACCESS_TOKEN = '你的 LINE CHANNEL ACCESS TOKEN'
OPENAI_API_KEY = '你的 OPENAI API KEY'
```

### 5. 啟動應用
運行 Flask 應用：
```sh
python app.py
```

應用將在 `http://127.0.0.1:5000` 運行。

## 使用說明
1. 在 Line 開發者平台設定你的 webhook URL 為 `http://<your-domain>/callback`。
2. 發送消息到你的 LineBot，ChatGPT 將會回應你的消息。

## 注意事項
- 請確保你的伺服器可以被 Line 平台訪問。
- 請妥善保管你的 API 金鑰，避免洩露。
