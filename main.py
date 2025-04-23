# main.py
"""
main.py

Backend API for HomeCure Kids – a FastAPI app that provides kitchen-based home remedies
for children's illnesses using LangChain, OpenAI, FAISS, and PDF/email integration.

Author: Preethi
"""
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from pydantic import BaseModel
from weasyprint import HTML

import email_utils
import pdf_utils
import retrieverFAISS

# 🔹 Load environment variables
load_dotenv()

# Set up OpenAI clients and vector store components
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔹 FastAPI Setup
app = FastAPI()

# 🔹 CORS setup to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Set to your React origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

urls = [
    "https://www.chkd.org/patient-family-resources/our-blog/home-remedies-for-sick-kids/",
    "https://www.webmd.com/parenting/baby/ss/slideshow-home-remedies",
    "https://www.babycenter.com/health/illness-and-infection/safe-home-remedies-for-your-childs-cough-cold-or-flu_10014077",
    "https://www.carehospitals.com/news-media-detail/home-remedies-for-minor-childhood-ailments"
    # You can add new URLs here anytime
]




retriever = retrieverFAISS.get_or_create_vectorstore(urls)

retriever_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user",
     "You are an assistant that helps search for natural remedies based on a conversation. Generate a focused search query from the chat history.")
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, retriever_prompt)

response_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly medical assistant trained to give kitchen-based home remedies for children's illnesses.

- If the user provides ingredients commonly used for kids' symptoms, provide remedies in steps with instructions for each step.
- If the user provides ingredients NOT commonly used for kids' symptoms, suggest common kitchen ingredients that ARE suitable for remedies, and explain why the user's ingredients are not ideal.
- If the user does NOT provide any ingredients, suggest common home remedies using typical kitchen ingredients for common kids' symptoms, and explain the benefits of each remedy.
- If there's no mention of a symptom or ingredients, kindly ask for more information.
- If the user's input is not related to kids' symptoms or kitchen ingredients, say: 'I can only help with home remedies for kids' symptoms using kitchen ingredients right now.'

Format all remedies in clear, numbered steps. Be concise and friendly.
Example:
User: My kid has a sore throat. I have salt and lemon at home.
Assistant:
1. Gargle with warm salt water: Mix 1/4 to 1/2 teaspoon of salt in a cup of warm water and have your child gargle for 30 seconds, several times a day.
2. Lemon and honey drink: Mix 1 tablespoon of lemon juice and 1 tablespoon of honey in a cup of warm water. Have your child drink this slowly.

<context>
{context}
</context>"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, response_prompt)
retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)


def generate_image(prompt: str):
    try:
        response = client.images.generate(
            model="dall-e-3",  # Or "dall-e-2"
            prompt=prompt,
            n=1,
            size="256x256"  # Adjust size as needed
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None




# 🔹 Chat Models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


class RemedyRequest(BaseModel):
    messages: list[Message]



memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=256)  # Adjust token limit as needed


@app.post("/chat")
async def chat(req: ChatRequest):
    chat_history = []
    for msg in req.messages[:-1]:
        if msg.role == "user":
            chat_history.append(HumanMessage(content=msg.content))
        else:
            chat_history.append(AIMessage(content=msg.content))

    memory.chat_memory.messages = chat_history
    current_input = req.messages[-1].content
    # It likely uses a retriever (like FAISS, Pinecone, etc.) to fetch relevant documents based on the current input.

    # Then it combines the fetched info + chat history + input and sends it to the language model to get a final response.
    response = retrieval_chain.invoke({
        "chat_history": memory.chat_memory.messages,
        "input": current_input
    })

    # Generate an image based on the remedy steps
    image_prompt = f"Create a simple step-by-step visual guide for the following home remedy for kids: {response['answer']}"
    image_url = generate_image(image_prompt)
    print("image_url", image_url)
    print(response["answer"])

    # Return both the text answer and the image URL
    return {"answer": response["answer"], "image_url": image_url}




@app.post("/generate_pdf")
async def generate_pdf(remedy_request: RemedyRequest):
    last_ai_message = next((m.content for m in reversed(remedy_request.messages) if m.role != "user"),
                           "no Remedy found")
    remedy_text = f"Recommended Remedy:\n{last_ai_message}"
    # remedy_text = "\n".join([f"{m.role}: {m.content}" for m in remedy_request.messages])
    pdf_path = pdf_utils.create_remedy_pdf(remedy_text)
    print(pdf_path)
    await email_utils.send_remedy_email("preethisivakumar94@gmail.com", pdf_path)
    # Return the generated PDF as a file response
    return FileResponse(pdf_path, filename="remedy.pdf", media_type='application/pdf')