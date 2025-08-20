import io
import os
import time
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from app.llm_analysis import ask_gpt_about_data
from app.charts import generate_plot_code

# --- Page Configuration ---
st.set_page_config(page_title="DataMind", layout="wide")

st.title("DataMind 🧠")

# --- Sidebar ---
uploaded_file = st.sidebar.file_uploader("Upload a CSV", type=["csv"])

# --- Tabs Layout ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Dataset Overview",
    "🤖 Data Insights",
    "🔎 Exploratory Analysis",         
    "📊 Chart Studio",       
    "🧠 Ask AI"              
])

# --- Function to pick best two columns ---
def pick_best_two_columns(df, chart_type: str):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    
    # Scatter plot: pick two numeric columns with most variance
    if "scatter" in chart_type.lower():
        if len(numeric_cols) >= 2:
            variances = df[numeric_cols].var().sort_values(ascending=False)
            return variances.index[:2].tolist()
        elif len(numeric_cols) == 1 and categorical_cols:
            return [numeric_cols[0], categorical_cols[0]]
    
    # Bar chart: pick categorical column and numeric column
    elif "bar" in chart_type.lower():
        if categorical_cols and numeric_cols:
            cat_col = df[categorical_cols].nunique().idxmax()
            num_col = df[numeric_cols].var().idxmax()
            return [cat_col, num_col]
    
    # Histogram: pick numeric column with highest variance
    elif "hist" in chart_type.lower() or "distribution" in chart_type.lower():
        if numeric_cols:
            return [numeric_cols[df[numeric_cols].var().argmax()]]
    
    # Line chart: numeric columns
    elif "line" in chart_type.lower():
        if len(numeric_cols) >= 2:
            return numeric_cols[:2]
    
    # Fallback: pick first two columns
    return df.columns[:2].tolist()

# --- Main Logic ---
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # --- Tab 1: Dataset Overview ---
    with tab1:
        st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df.head(50))

    # --- Tab 2: Data Insights ---
    with tab2:
        if "gpt_insights" not in st.session_state:
            summary = f"""
        Columns: {df.columns.tolist()}
        Shape: {df.shape}
        Data Types: {df.dtypes.to_dict()}
        Missing Values: {df.isnull().sum().to_dict()}
        Summary Stats: {df.describe().to_dict()}
            """
            with st.spinner("Asking GPT..."):
                st.session_state.gpt_insights = ask_gpt_about_data(summary)

        st.markdown(st.session_state.gpt_insights)

    # --- Tab 3: Exploratory Analysis ---
    with tab3:
        st.write("### Data Types")
        st.dataframe(df.dtypes)

        st.write("### Missing Values")
        st.dataframe(
            df.isnull().sum()
            .reset_index()
            .rename(columns={0: 'Missing Count', 'index': 'Column'})
        )

        st.write("### Descriptive Statistics")
        desc = df.describe(include="all").T.drop(columns=["unique"], errors="ignore")
        st.dataframe(desc, use_container_width=True, height=275)

        st.write("### Unique Values per Column")
        st.dataframe(
            df.nunique()
            .reset_index()
            .rename(columns={0: 'Unique Values', 'index': 'Column'})
        )

    # --- Chart Rendering Function ---
    def render_chart(code: str, df: pd.DataFrame) -> str:
        local_env = {"df": df, "st": st, "plt": plt, "alt": alt}
        buf = io.BytesIO()

        try:
            exec(code, {}, local_env)

            if plt.get_fignums():
                plt.savefig(buf, format="png", bbox_inches="tight")
                plt.close()
            elif "chart" in local_env:
                chart = local_env["chart"]
                chart.save(buf, format="png")
        except Exception as e:
            st.error(f"Chart rendering failed: {e}")
            return None

        buf.seek(0)
        temp_chart_path = "temp_chart.png"
        with open(temp_chart_path, "wb") as f:
            f.write(buf.read())
        return temp_chart_path

    # --- Tab 4: Chart Studio ---
    with tab4:
        # --- Best Chart ---
        if "best_chart_bytes" not in st.session_state:
            with st.spinner("Generating best chart..."):
                best_code = generate_plot_code("best chart for dataset", df)
                temp_chart_path = render_chart(best_code, df.sample(min(200, len(df))))
                with open(temp_chart_path, "rb") as f:
                    st.session_state.best_chart_bytes = f.read()
                st.session_state.best_chart_code = best_code

        st.markdown("### Best Chart")

        st.code(st.session_state.best_chart_code, language="python")

        st.image(st.session_state.best_chart_bytes, width=775)
        st.download_button(
            label="📥 Download ",
            data=st.session_state.best_chart_bytes,
            file_name="best_chart.png",
            mime="image/png",
            key="download_best_chart"
        )

        st.markdown("---")

        # --- Custom Chart Generator ---
        st.markdown("### Your Generated Charts")
        if "user_charts" not in st.session_state:
            st.session_state.user_charts = []

        for i, chart in enumerate(st.session_state.user_charts):
            st.markdown(f"**{i+1}. Chart for prompt:** `{chart['prompt']}`")
            st.markdown(f"**Columns Used:** {chart.get('cols', 'N/A')}")

            st.code(chart["code"], language="python")

            st.image(chart["bytes"], width=775)
            st.download_button(
                label=f"📥 Download ",
                data=chart["bytes"],
                file_name=f"chart_{i+1}.png",
                mime="image/png",
                key=f"download_btn_{i}"
            )
            st.markdown("---")

        user_prompt = st.text_input(
            "Enter a chart request (e.g., scatter plot):",
            value="",
            key=f"chart_input_{len(st.session_state.user_charts)}"
        )
        if st.button("Generate Chart", key="generate_chart_btn") and user_prompt:
            with st.spinner("Generating chart..."):
                # --- Automatically pick best two columns based on user prompt ---
                cols = pick_best_two_columns(df, user_prompt)
                df_two = df[cols].copy()

                # Take a sample of 200 rows for new chart generation
                df_two_sample = df_two.sample(min(200, len(df_two)))

                # Generate chart code using only these columns
                code = generate_plot_code(user_prompt, df_two_sample)
                temp_chart_path = render_chart(code, df_two_sample)
                
                with open(temp_chart_path, "rb") as f:
                    chart_bytes = f.read()
                
                st.session_state.user_charts.append(
                    {"prompt": user_prompt, "code": code, "bytes": chart_bytes, "cols": cols}
                )
            st.rerun()

    # --- Tab 5: Ask AI ---
    with tab5:

        if "assistant_chat" not in st.session_state:
            st.session_state.assistant_chat = []

        for msg in st.session_state.assistant_chat:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style='text-align: right;'>
                        <div style='display: inline-block; background-color: #1E3A8A;
                                    color: white; padding: 10px 14px; border-radius: 15px;
                                    margin: 5px 0; max-width: 70%; width: auto; word-wrap: break-word;'>
                            {msg['content']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style='text-align: left;'>
                        <div style='display: inline-block; background-color: #374151;
                                    color: white; padding: 10px 14px; border-radius: 15px;
                                    margin: 5px 0; max-width: 70%; width: auto; word-wrap: break-word;'>
                            {msg['content']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        user_question = st.chat_input("Ask anything about the dataset...")

        if user_question:
            st.session_state.assistant_chat.append(
                {"role": "user", "content": user_question}
            )
            from app.assistant import ask_assistant
            with st.spinner("Thinking..."):
                response = ask_assistant(user_question, df)

            st.session_state.assistant_chat.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

else:
    st.warning("👈 Upload a CSV file from the sidebar to get started.")