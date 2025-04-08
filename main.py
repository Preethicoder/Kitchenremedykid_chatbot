# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 🔹 Load environment variables
load_dotenv()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔹 Load and process documents (you can cache this in real use)
urls = [
    "https://www.chkd.org/patient-family-resources/our-blog/home-remedies-for-sick-kids/",
    "https://www.webmd.com/parenting/baby/ss/slideshow-home-remedies",
    "https://www.babycenter.com/health/illness-and-infection/safe-home-remedies-for-your-childs-cough-cold-or-flu_10014077"
]
all_docs = []
for url in urls:
    loader = WebBaseLoader(url)
    docs = loader.load()
    all_docs.extend(docs)

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(all_docs)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

retriever_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up remedies relevant to the conversation.")
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, retriever_prompt)

response_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly medical assistant trained to give kitchen-based home remedies for children's illnesses.
Use ONLY the context provided to answer questions. If the question is not related to kids’ symptoms or kitchen remedies, say:
'I can only help with home remedies for kids' symptoms using kitchen ingredients right now.'

Please provide remedies in bullet points.
<context>
{context}
</context>"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, response_prompt)
retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

# 🔹 FastAPI Setup
app = FastAPI()

# 🔹 CORS setup to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Set to your React origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Chat Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/chat")
async def chat(req: ChatRequest):
    chat_history = []
    for msg in req.messages[:-1]:
        if msg.role == "user":
            chat_history.append(HumanMessage(content=msg.content))
        else:
            chat_history.append(AIMessage(content=msg.content))

    current_input = req.messages[-1].content

    response = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": current_input
    })

    return {"answer": response["answer"]}
