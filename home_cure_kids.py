import os
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
"""User asks → Retriever (LLM-enhanced) generates query → FAISS returns remedy chunks →
Stuffed into prompt with system rules → LLM answers → User gets a smart, focused reply.
l"""
# 🔹 Load environment
load_dotenv()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
urls = [
    "https://www.chkd.org/patient-family-resources/our-blog/home-remedies-for-sick-kids/",
    "https://www.webmd.com/parenting/baby/ss/slideshow-home-remedies",
    "https://www.babycenter.com/health/illness-and-infection/safe-home-remedies-for-your-childs-cough-cold-or-flu_10014077"# Another source
]
# 🔹 Load Kitchen Remedy page from CHKD
all_docs = []
for url in urls:
    loader =WebBaseLoader(url)
    docs = loader.load()
    all_docs.extend(docs)

# 🔹 Split and embed documents
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(all_docs)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# 🔹 Create history-aware retriever
retriever_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up remedies relevant to the conversation.")
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, retriever_prompt)

# 🔹 Create the document QA chain
response_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly medical assistant trained to give kitchen-based home remedies for children's illnesses.
Use ONLY the context provided to answer questions. If the question is not related to kids’ symptoms or kitchen remedies, say:
'I can only help with home remedies for kids' symptoms using kitchen ingredients right now.'

<context>
{context}
</context>"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, response_prompt)
retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

# 🔹 Initialize chat history
chat_history = []

# 🔁 Chat loop
print("🧑‍🍳 HomeCure-Kids Chatbot is ready! (type 'exit' to quit)\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Take care! Hope your little one feels better soon!")
        break

    # 🔸 Call the chain with history and current input
    response = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": user_input
    })

    answer = response["answer"]
    print(f"AI: {answer}\n")

    # 🔸 Add to chat history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=answer))
