# 🌐 PageGist — AI-Powered Webpage Summarizer

PageGist is an intelligent **Chrome extension** that summarizes entire webpages in seconds using **Qwen models via Hugging Face**.  
Inspired by the [DataCamp Qwen Agent Tutorial](https://www.datacamp.com/tutorial/qwen-agent), PageGist enhances your browsing experience by instantly delivering concise summaries of complex web content — right in your browser.

---

## 🚀 Features

- 🧠 **AI Summarization** — Uses Hugging Face Qwen models for accurate and context-aware summaries.
- 🌍 **Webpage Intelligence** — Extracts readable, meaningful text while ignoring ads, headers, and other noise.
- ⚡ **Instant Summaries** — Generates summaries in seconds with minimal resource use.
- 💬 **Simple, Clean UI** — A lightweight popup interface for quick access.
- 🔐 **Privacy Focused** — Your data stays local; only the content to summarize is sent to Hugging Face’s secure inference API.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend (AI Service)** | Python |
| **AI Model** | meta-llama/Llama-3.1-8B-Instruct (via Hugging Face Transformers) |
| **Inference Provider** | [Hugging Face Inference API](https://huggingface.co/inference-api) |
| **Browser Platform** | Chrome (Manifest V3) |
| **Base Reference** | [DataCamp Qwen Agent Tutorial](https://www.datacamp.com/tutorial/qwen-agent) |

---

## 📦 Installation & Setup Guide

Follow these steps to get **PageGist** running on your local machine:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/PageGist.git
cd PageGist
```


### 2️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Hugging Face Token
Setup Hugging Face Token in env file under 'backend' folder
```bash
HUGGINGFACEHUB_API_TOKEN = "your-huggingface-token"
```

### 4️⃣ Run the Backend Server
The extension communicates with port 7864
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 7864
```

### 5️⃣ Load the Chrome Extension
```bash
1.Open Chrome → Extensions → Manage Extensions
2.Turn on Developer Mode (top-right corner)
3.Click Load unpacked and select the /frontend folder
4.The PageGist icon will appear in your browser extension toolbar 🚀
```
