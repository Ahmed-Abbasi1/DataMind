import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# --- Load API key ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# --- LLM Setup ---
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-70b-8192")

# --- Prompt Template ---
prompt_template = ChatPromptTemplate.from_template("""
You are a Python data visualization expert. The user has uploaded a dataset and is asking you to create a chart using matplotlib in Streamlit.

Here is the user's request:
----------------------------
{user_prompt}

Dataset sample (df.head()):
----------------------------
{df_sample}

Instructions:
- If the user prompt is generic (e.g., "scatter plot", "histogram"), you must intelligently choose the best columns for that chart type.
- Assume the DataFrame is named `df`
- Do NOT include import statements.
- Only return valid Python code inside a Python code block.
- The last line must be: st.pyplot(fig)
""")

# --- Chain ---
chain = prompt_template | llm | StrOutputParser()

# --- Generate Python Code ---
def generate_plot_code(user_prompt: str, df: pd.DataFrame) -> str:
    df_sample = df.sample(min(len(df), 300)).reset_index(drop=True).head(5).to_string(index=False)

    raw_code = chain.invoke({
        "user_prompt": user_prompt,
        "df_sample": df_sample
    })

    # Extract clean code from markdown
    if "```" in raw_code:
        code = raw_code.split("```")[1]
        code = code.replace("python", "")
        return code.strip()

    return raw_code.strip()

# --- Execute Chart Code & Save Plot ---
def render_chart(code: str, df: pd.DataFrame) -> str:
    df = df.sample(min(len(df), 100)).copy()
    global_vars = {"df": df, "plt": plt, "st": st}
    fig_path = "generated_chart.png"

    try:
        exec(code, global_vars)
        # Save fig if defined
        if "fig" in global_vars:
            global_vars["fig"].savefig(fig_path)
            return fig_path
    except Exception as e:
        st.error(f"⚠️ Error in generated chart code:\n{e}")
    return None