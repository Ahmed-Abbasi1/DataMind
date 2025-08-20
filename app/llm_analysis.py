import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Set up Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama3-70b-8192"
)

# Template for insights
prompt_template = ChatPromptTemplate.from_template("""
You are a professional data analyst. The user has uploaded a dataset and here is the summary:

{description}

Based on this, write 5–7 bullet-point insights about the dataset. Focus on:
- distributions
- missing values
- anomalies
- potential relationships

Make it easy to understand and actionable.
""")

chain = prompt_template | llm | StrOutputParser()

def ask_gpt_about_data(description: str) -> str:
    return chain.invoke({"description": description})