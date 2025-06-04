# 🧑‍🍳 Kitchenremedykid_chatbot

HomeCure-Kids is a web-based chatbot that provides kitchen-based home remedies for children’s illnesses. It uses FastAPI, LangChain, and OpenAI to deliver symptom-based suggestions in an interactive and friendly way.

---

## 🌟 Features

- 🗨️ **Conversational Interface** – Type symptoms and receive remedy suggestions.
- 🧠 **Context-Aware** – Understands chat history for relevant results.
- 🍋 **Kitchen Ingredients Only** – All remedies are based on household items.
- 🧪 **Hybrid Retrieval** – Combines dense + sparse + reranking for better accuracy.
- ⚡ **Fast & Responsive** – Built with FastAPI backend and a React frontend.
- 📚 **Web Data Powered** – Uses trusted online sources to provide suggestions.

---

## 🧰 Tech Stack

| Layer        | Technology                 |
|--------------|----------------------------|
| Frontend     | React                      |
| Backend      | FastAPI                    |
| AI           | OpenAI (GPT model)         |
| Retrieval    | LangChain + FAISS + BM25   |
| Reranking    | Cross-Encoder (Optional)   |
| Scraping     | WebBaseLoader              |
| Language     | Python + JavaScript        |

---

## 🔍 Retrieval Strategy (Hybrid Search)

To deliver the most relevant remedy suggestions, HomeCure-Kids uses a **hybrid retrieval** system:

- **Dense Retrieval**: Uses FAISS with sentence-transformer embeddings to retrieve semantically similar documents based on symptoms and context.
- **Sparse Retrieval**: Uses BM25 (via `rank_bm25`) to perform keyword-based search, especially effective for exact matches like ingredient names or common phrases.
- **Context-Awareness**: Dense retriever uses recent chat history to better understand ongoing conversations.
- **Reranking**: All retrieved documents are scored using a Cross-Encoder model, and the top results are selected for the LLM.
- ✅ **Benefit**: Significantly improves relevance and robustness across different user query styles.

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

## 📨 Email Delivery (via Celery)

Email sending is handled as a **background task** using [Celery](https://docs.celeryq.dev/). This ensures that the FastAPI server remains responsive and does not block while sending emails.

### How It Works

- When a PDF is generated, an email-sending task is pushed to a Celery queue.
- A Celery worker (connected to Redis) processes the task and sends the email.

### Requirements

Make sure you have:
- Redis installed and running on `localhost:6379`
- A Celery worker running with:
  ```bash
  celery -A tasks.email_tasks worker --loglevel=info

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


 
