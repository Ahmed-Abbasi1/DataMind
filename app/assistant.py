import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-70b-8192")

# Define prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are a helpful data analyst assistant. Answer the user's question using the dataset provided.

Dataset Info:
-------------
{data_context}

User Question:
--------------
{user_query}

Instructions:
- Respond like a data analyst.
- Be concise, helpful, and clear.
- If a Python code snippet can help, include it inside a markdown code block.
""")

chain = prompt_template | llm | StrOutputParser()

def ask_assistant(user_query: str, df) -> str:
    context = f"""
Columns: {df.columns.tolist()}
Shape: {df.shape}
DTypes: {df.dtypes.to_dict()}
Missing Values: {df.isnull().sum().to_dict()}
"""
    return chain.invoke({
        "user_query": user_query,
        "data_context": context
    })