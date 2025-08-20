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

- **Frontend & App**: [Streamlit](https://datamind-8m6u8hlbkf4tezv3qdbor7.streamlit.app/).
- **Data Processing**: Pandas.
- **Visualization**: Matplotlib, Altair.
- **AI & LLM**: GPT integration via LangChain or custom APIs.
- **Environment Management**: Python 3.9+.
- **Chart Rendering**: Automated chart code generation and execution.

---

 ## Key Benefits

- No coding required for generating insights or visualizations.
- Automatically generates reproducible Python code for charts.
- AI-powered recommendations make EDA faster and more insightful.
- Ideal for beginners, analysts, or anyone exploring new datasets.
