# main.py
"""
main.py

Backend API for HomeCure Kids – a FastAPI app that provides kitchen-based home remedies
for children's illnesses using LangChain, OpenAI, FAISS, and PDF/email integration.

Author: Preethi
"""
import json
import os

import asyncio

from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict
from starlette.responses import FileResponse
from fastapi import BackgroundTasks
import email_utils
from tasks.email_tasks import send_remedy_email_task
import pdf_utils
import retrieverFAISS
from relevance_score import grade_relevance

# 🔹 Load environment variables
load_dotenv()

# Set up OpenAI clients and vector store components
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔹 Initialize reranker (lightweight cross-encoder model)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
# 🔹 FastAPI Setup
app = FastAPI()

# 🔹 CORS setup to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Set to your React origin in production
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # <-- Important!
)

urls = [
    "https://www.chkd.org/patient-family-resources/our-blog/home-remedies-for-sick-kids/",
    "https://www.webmd.com/parenting/baby/ss/slideshow-home-remedies",
    "https://www.babycenter.com/health/illness-and-infection/safe-home-remedies-for-your-childs-cough-cold-or-flu_10014077",
    "https://www.carehospitals.com/news-media-detail/home-remedies-for-minor-childhood-ailments",
    "https://www.healthychildren.org/English/health-issues/conditions/chest-lungs/Pages/caring-for-kids-with-colds-and-flu-simple-remedies-that-help.aspx",
    "https://www.afcurgentcare.com/nanuet/blog/home-remedies-for-common-childhood-illnesses-safe-and-effective-tips/",
    "https://www.childrensnebraska.org/natural-alternatives-5-home-remedies-that-are-safe-for-infants",
    "https://juniperfamilyhealth.com/blog/2018/3/23/natural-remedies-for-children",
    "https://www.childrens.com/health-wellness/6-non-medical-remedies-for-the-flu",
    "https://healthcare.com.sa/7-natural-remedies-for-treating-your-childs-cold-and-flu/",
    "https://pillarsofwellness.ca/naturopathy/what-are-the-best-natural-remdiese-for-kids-health/ ",
    "https://www.hachette.co.uk/titles/rosemary-gladstar/herbs-for-childrens-health/9781635868289/ ",
    "https://www.nationwidechildrens.org/family-resources-education/family-resources-library/a-guide-to-common-medicinal-herbs "
    # You can add new URLs here anytime
]
# Load and split documents from URLs (reusing your function)
docs = retrieverFAISS.load_documents_from_urls(urls)
# Create the BM25 sparse retriever
sparse_retriever = BM25Retriever.from_documents(docs)
retriever = retrieverFAISS.get_or_create_vectorstore(urls)


retriever_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user",
     "You are an assistant that helps search for natural remedies based on a conversation. Generate a focused search query from the chat history.")
])
print("iput::",input)
history_aware_retriever = create_history_aware_retriever(llm, retriever, retriever_prompt)


response_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly medical assistant trained to give kitchen-based home remedies for **children's illnesses only**.
**Do not give remedies for adults or any non-child-related issue.** If the user clearly says they are asking for themselves (e.g., "I am an adult", "Can I use this too?", or "What about for me?"), politely respond:
"I'm here to help with remedies for children's health using kitchen ingredients. If you’re asking for yourself, I recommend speaking with a healthcare provider. Let me know if you're asking about a child’s health instead!"

- If the user provides ingredients commonly used for kids' symptoms, provide remedies in steps with instructions for each step.
- If the user provides ingredients NOT commonly used for kids' symptoms, suggest common kitchen ingredients that ARE suitable for remedies, and explain why the user's ingredients are not ideal.
- If the user does NOT provide any ingredients, suggest common home remedies using typical kitchen ingredients for common kids' symptoms, and explain the benefits of each remedy.
- If there's no mention of a symptom or ingredients, kindly ask for more information.
- If the user's input is not related to kids' symptoms or kitchen ingredients, say: 'I'm sorry to hear that. I specialize in offering home remedies using kitchen ingredients for common children's symptoms. If you're looking for help with a child’s health issue, feel free to share the symptoms, and I'll do my best to assist!'

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
            size="1024x1024"  # Adjust size as needed
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


memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=256)# Adjust token limit as needed
def get_sparse_with_history(sparse_retriever, memory, current_input):
    history_text = "\n".join(
        [msg.content for msg in memory.chat_memory.messages if isinstance(msg, HumanMessage)]
    )
    full_query = history_text + "\n" + current_input
    return sparse_retriever.get_relevant_documents(full_query)

def hybrid_retrieve_and_rerank(query: str, retrieved_docs, sparse_docs, reranker, top_k=4):
    all_docs = retrieved_docs + sparse_docs
    unique_docs = {doc.page_content: doc for doc in all_docs}.values()
    # Step 2: Rerank the retrieved documents

    doc_pairs = [(query, docs.page_content) for docs in unique_docs]
    scores = reranker.predict(doc_pairs)

    # Combine scores with docs and sort
    scored_docs = list(zip(unique_docs, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # Take top-k docs after reranking

    reranked_docs = [doc for doc, score in scored_docs[:top_k]]

    for doc in reranked_docs:
        print("reranked:::", doc.page_content)
    return reranked_docs
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
    # 🔹 Step 1: Retrieve documents manually using history_aware_retriever
    retrieved_docs = history_aware_retriever.invoke({
        "chat_history": memory.chat_memory.messages,
        "input": current_input
    })
    # Step 2: Sparse retrieval
    sparse_docs = get_sparse_with_history(sparse_retriever, memory, current_input)

    reranked_docs = hybrid_retrieve_and_rerank(current_input,retrieved_docs,sparse_docs,reranker)
    # Then it combines the fetched info + chat history + input and sends it to the language model to get a final response.
    response = document_chain.invoke({
        "context": reranked_docs,
        "chat_history": memory.chat_memory.messages,
        "input": current_input
    })
    print("response:::::::",response)


    # Generate an image based on the remedy steps
    image_url = ""
    image_prompt = f"Create a simple step-by-step visual guide for the following home remedy for kids: {response}"
    #image_url = generate_image(image_prompt)
    #print("image_url", image_url)


    # Return both the text answer and the image URL
    return {"answer": response, "image_url": image_url}


async def generate_title(last_ai_message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant that generates concise, informative titles for remedy instructions."
        },
            {
                "role": "user",
                "content": f"Suggest a short, clear title suitable as a file name for this remedy:\n{last_ai_message}"
            }
        ]
    )
    title = response.choices[0].message.content.strip()
    file_name = title.lower().replace(' ', '_').replace('&', 'and') + ".pdf"
    print("response:::", file_name)

    return file_name


def readandwritetofile(entry):
    file_path = "relevance_scores.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(entry)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


@app.post("/generate_pdf")
async def generate_pdf(remedy_request: RemedyRequest):
    print("generate PDF:::", remedy_request)

    # Get the last AI message (remedy suggestion)
    last_ai_message = next((m.content for m in reversed(remedy_request.messages) if m.role != "user"),
                           "no Remedy found")
    # Get last user message (question) and AI message (answer)
    last_user_message = next((m.content for m in reversed(remedy_request.messages) if m.role == "user"), "")

    # Evaluate relevance
    relevance_score = grade_relevance(last_user_message, last_ai_message)
    print("Relevance score:", relevance_score.relevant)
    print("Explanation:", relevance_score.explanation)
    entry = {"last_user_message:::": last_user_message,
             "last_ai_message:::": last_ai_message,
             "Relevance score:::": relevance_score.relevant,
             "Explanation:::": relevance_score.explanation}
    readandwritetofile(entry)
    # Generate the title for the PDF
    title = await generate_title(last_ai_message)
    print("Generated title:::", title)

    # Prepare the remedy text for the PDF
    remedy_text = f"Recommended Remedy:\n{last_ai_message}"

    # Create the remedy PDF
    pdf_path = pdf_utils.create_remedy_pdf(remedy_text,title)
    print("Generated PDF Path:::", pdf_path)

    # Send the generated remedy PDF via email
    #await email_utils.send_remedy_email("preethisivakumar94@gmail.com", pdf_path)

    # ✅ Run email task asynchronously via Celery
    send_remedy_email_task.delay("preethisivakumar94@gmail.com", pdf_path)

    # Return the generated PDF as a file response, using the generated title for filename
    return FileResponse(pdf_path, filename=title, media_type='application/pdf')
