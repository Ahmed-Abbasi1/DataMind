# LLM Data Analyst

**LLM Data Analyst** is an interactive Streamlit application that allows users to upload any CSV dataset and automatically generate insights, visualizations, and Python chart code using Large Language Models (LLMs) and smart EDA techniques. The app makes data analysis simple, fast, and accessible to both beginners and advanced users.

---

## Features

### 1. Dataset Overview
- View the dataset's **shape**, **columns**, and **top rows**.
- Quickly inspect data types and missing values.

### 2. AI-Powered Data Insights
- Automatically generates a **GPT-based summary** of your dataset.
- Includes insights on data types, missing values, and summary statistics.

### 3. Exploratory Data Analysis (EDA)
- Examine **data types**, **missing values**, **descriptive statistics**, and **unique values per column**.
- Helps identify patterns and potential data issues.

### 4. Chart Studio
- Generates **best-suited visualizations** for your dataset automatically.
- Users can input a natural language prompt (e.g., “scatter plot of age vs cost”) to generate charts.
- Code for each chart is displayed above the visualization for easy editing and reproducibility.
- Charts can be **downloaded as PNG**.
- Automatically samples up to **100 rows** for new chart generation to improve speed.

### 5. Ask AI
- Interactive **AI assistant** to answer questions about the dataset.
- Suggests visualizations and analysis steps.
- Generates Python code snippets if required.

---

## Tech Stack

- **Frontend & App**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **Visualization**: Matplotlib, Altair
- **AI & LLM**: GPT integration via LangChain or custom APIs
- **Environment Management**: Python 3.9+
- **Chart Rendering**: Automated chart code generation and execution

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/LLM-Data-Analyst.git
cd LLM-Data-Analyst

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

streamlit run streamlit_app.py

Usage

Upload your CSV dataset via the sidebar.

Navigate between tabs to:

Explore dataset overview

View AI-generated insights

Perform EDA

Generate and download charts

Ask AI questions about the dataset

For chart generation, enter a natural language prompt (e.g., "bar chart of sales vs region") and click Generate Chart.

Download charts directly using the Download buttons.


LLM-Data-Analyst/
├─ app.py                  # Main Streamlit app
├─ app/
│  ├─ llm_analysis.py      # Functions for GPT-based dKey Benefits

No coding required for generating insights or visualizations.

Automatically generates reproducible Python code for charts.

AI-powered recommendations make EDA faster and more insightful.

Ideal for beginners, analysts, or anyone exploring new datasets.ata insights
│  ├─ charts.py            # Functions to generate and render charts
│  ├─ assistant.py         # AI assistant integration
├─ requirements.txt        # Python dependencies
└─ README.md





