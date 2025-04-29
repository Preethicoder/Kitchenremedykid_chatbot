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
3. **Install dependencies:**:
   ```bash
   pip install -r requirements.txt
4. **Set your OpenAI API key: Create a .env file and add**:
   OPENAI_API_KEY=your-api-key-here
5. **Start the server**:
   uvicorn main:app --reload
Your backend will run at: http://localhost:8000

### 💻 Frontend Setup (React)
1. **Navigate to frontend folder**:
   ```bash
   cd ../frontend
2. **Install Node.js dependenciest**:
   ```bash
   npm install
3. **Start the React app:**:
   ```bash
   npm start
The app will run at: http://localhost:3000

### CORS Configuration
  Make sure your FastAPI main.py includes:
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
     expose_headers=["Content-Disposition"], 
   )

### 🧪 Testing the Chatbot
1.Open http://localhost:3000 in your browser.
2.Type a symptom like "My kid has a sore throat".
3.The chatbot will respond with friendly, bullet-pointed home remedies.

### 🙌 Contributing
Contributions are welcome!

1)Open issues

2)Submit pull requests

3)Improve documentation

4)Suggest better remedies 💡
### ⚠️ Disclaimer
This chatbot provides kitchen-based home remedy suggestions based on scraped public content and AI-generated summaries. It is not a replacement for medical advice. Please consult a licensed healthcare provider for serious symptoms or emergencies.


 
