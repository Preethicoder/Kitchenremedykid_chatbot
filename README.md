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

### ➕ Additional Features

- 🖼️ **Visual Remedy Guide** – Generates step-by-step illustrations using DALL·E for each remedy.
- 📝 **PDF Export** – Remedies can be downloaded as nicely formatted PDFs.
- 📧 **Email Support** – Remedy PDFs can be sent directly to your inbox.
- ✅ **Relevance Evaluation** – Each remedy is automatically evaluated for accuracy and relevance.

### 🧪 Testing the Chatbot (Extended)

1. Open http://localhost:3000 in your browser.
2. Ask a question like "My kid has a sore throat".
3. The chatbot will:
   - Respond with a friendly, step-by-step remedy.
   - Show a visual guide (image).
   - Optionally allow you to export the remedy as a PDF.
   - Internally evaluate how relevant the answer is and log it.


### 🙌 Contributing
Contributions are welcome!

1)Open issues

2)Submit pull requests

3)Improve documentation

4)Suggest better remedies 💡
### ⚠️ Disclaimer
This chatbot provides kitchen-based home remedy suggestions based on scraped public content and AI-generated summaries. It is not a replacement for medical advice. Please consult a licensed healthcare provider for serious symptoms or emergencies.


 
