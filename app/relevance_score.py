import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from pydantic import BaseModel, Field, ConfigDict
load_dotenv()
relevance_instructions = """
You are a quality evaluator for a medical assistant chatbot that provides home remedies for children's illnesses using common kitchen ingredients.

You will be given:
- A USER QUESTION about a child's symptom or related topic.
- The CHATBOT'S RESPONSE, which should provide a helpful kitchen-based home remedy or relevant advice.

Grade the chatbot's response using the following criteria:
(1) Is the response directly relevant to the user's question or concern?
(2) Does the response provide practical kitchen-based remedies or advice that makes sense for the described symptom or context?
(3) If the user provides ingredients, does the response correctly use or address them?
(4) If the user gives unrelated input, does the assistant respond appropriately (e.g., by gently guiding the user back to the topic)?

Relevance:
- A relevance value of **True** means the chatbot's response is clear, helpful, and meets all criteria.
- A relevance value of **False** means the response is irrelevant, confusing, or does not address the user's input appropriately.

Explain your reasoning in a step-by-step manner before giving the final True/False grade.
Do not assume correctness without analyzing the content carefully.
"""
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class RelevanceGrade(BaseModel):
    relevant: bool = Field(..., description="Whether the remedy addresses the question")
    explanation: str = Field(..., description="Explain your reasoning for the score")

    model_config = ConfigDict(extra="forbid")


relevance_llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(RelevanceGrade)


def grade_relevance(question: str, answer: str) -> RelevanceGrade:
    return relevance_llm.invoke([
        {"role": "system", "content": relevance_instructions},
        {"role": "user", "content": f"QUESTION: {question}\nSTUDENT ANSWER: {answer}"}
    ])
