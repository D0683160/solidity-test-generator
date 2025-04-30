# 🛠️ Solidity Test Case Auto Generator / 智能合約測資自動生成器

This is an AI-powered tool that **automatically generates Hardhat-compatible JavaScript unit tests for Solidity smart contracts**, powered by local LLMs via Ollama, with optional RAG enhancement and test coverage analysis.

本專案是一個結合 **LLM + RAG + Hardhat Coverage** 的 AI 工具，可自動為 Solidity 合約產生單元測試並提供測試覆蓋率報告，支援本地模型推論、前後端分離與簡易 UI 操作。

---

## 🌟 Features | 功能特色

- ✅ Upload or paste Solidity contracts / 上傳或貼上 Solidity 合約
- 🧠 Generate tests using LLMs (LLaMA3, Gemma2, Qwen2, etc.)
- 🔍 Optional RAG enhancement using known test corpus
- 📦 Auto-generate JavaScript test files
- 📊 Run tests & get coverage with one click
- 🖥️ Web UI via Streamlit

---

## 🧱 Tech Stack | 使用技術

| Layer        | 技術 / Tools            |
|--------------|--------------------------|
| Frontend UI  | Streamlit                |
| Backend API  | FastAPI                  |
| LLM Pipeline | LangChain + Ollama       |
| Local Models | LLaMA3, Gemma3, Qwen3    |
| Vector DB    | Chroma                   |
| Testing Tool | Hardhat                  |
| Coverage     | solidity-coverage        |
| Prompt I/O   | PromptTemplate (Zero/One-Shot) |

---

## ⚙️Usage | 快速使用
### 1️⃣ Install Dependencies
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

```bash
# Python venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Node.js packages
npm install
```
### 2️⃣ Run the System | 啟動系統

```bash
# Start Ollama local LLM service
ollama serve

# Start backend
uvicorn backend.main:app --reload

# Start frontend
streamlit run frontend/app.py
```
Open browser at: [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure
```text
├── backend/         # FastAPI server & test generation logic
├── frontend/        # Streamlit UI
├── scripts/         # Chroma DB setup script
├── prompts/         # Prompt templates (zero-shot / one-shot)
├── contracts/       # Uploaded Solidity contracts
├── test/            # Generated Hardhat test files
├── chroma_db/       # Vector database
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

---

## 🙋‍♂️ Author
Yi-Huan,Lee  
GitHub: [https://github.com/D0683160](https://github.com/D0683160)

---

## 📜 License
MIT License
