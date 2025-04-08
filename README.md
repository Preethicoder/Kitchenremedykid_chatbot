# 🧑‍🍳 HomeCure-Kids Chatbot

HomeCure-Kids is a web-based chatbot that provides kitchen-based home remedies for children’s illnesses. It uses FastAPI, LangChain, and OpenAI to deliver symptom-based suggestions in an interactive and friendly way.

---

## 🌟 Features

- 🗨️ **Conversational Interface** – Type symptoms and receive remedy suggestions.
- 🧠 **Context-Aware** – Understands chat history for relevant results.
- 🍋 **Kitchen Ingredients Only** – All remedies are based on household items.
- ⚡ **Fast & Responsive** – Built with FastAPI backend and a React frontend.
- 📚 **Web Data Powered** – Uses trusted online sources to provide suggestions.

---

## 🧰 Tech Stack

| Layer      | Technology         |
|------------|--------------------|
| Frontend   | React              |
| Backend    | FastAPI            |
| AI         | OpenAI (GPT model) |
| Retrieval  | LangChain + FAISS  |
| Scraping   | WebBaseLoader      |
| Language   | Python + JavaScript|

---

## 🚀 Setup Instructions

### 🔧 Backend Setup (FastAPI)

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/HomeCure-Kids-Chatbot.git
   cd HomeCure-Kids-Chatbot/backend
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
3.**Install dependencies:**:
   ```bash
   pip install -r requirements.txt
4. **Set your OpenAI API key: Create a .env file and add**:
   OPENAI_API_KEY=your-api-key-here
5. **Start the server**:
   uvicorn main:app --reload
Your backend will run at: http://localhost:8000


 
