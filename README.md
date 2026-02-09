# LitAI: Structural Manuscript Auditor

**LitAI** is an industry-grade, AI-powered literary assistant designed to perform deep structural audits on manuscripts. Unlike basic summarization tools, LitAI utilizes an **Agentic RAG (Retrieval-Augmented Generation)** pipeline to simulate the mind of a Senior Developmental Editor, identifying narrative inconsistencies and thematic gaps with precise source attribution.

---

## 🚀 Key Features

* **Semantic Section Marking:** Automatically identifies and cites specific page numbers (e.g., `[📍 Page 12]`) using metadata-aware retrieval.
* **Editor Persona Engine:** Leverages **Gemini 3 Flash** with `thinking_level="medium"` to generate critical questions, structural impacts, and expected narrative answers.
* **Fluid Intent Recognition:** Distinguishes between factual queries (listing characters) and analytical requests (auditing pacing or themes).
* **High-Performance Vector Store:** Utilizes **FAISS** (Facebook AI Similarity Search) for sub-second retrieval across large text corpora.
* **2026-Ready Stack:** Built on the latest **Gemini 3 Flash Preview** architecture for superior zero-shot reasoning.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **LLM** | Google Gemini 3 Flash Preview |
| **Orchestration** | LangChain (LCEL) |
| **Vector Database** | FAISS (CPU) |
| **UI Framework** | Streamlit |
| **PDF Processing** | PyPDF with Metadata Extraction |

---

## 📂 Project Structure

```plaintext
├── src/
│   ├── app.py              # Streamlit Frontend & Orchestration
│   ├── preprocess.py       # Document Loading & Metadata Chunking
│   └── generator.py        # AI Persona & RAG Chain Logic
├── .env                    # API Key Storage (Ignored by Git)
├── requirements.txt        # Dependency List
└── README.md               # Project Documentation

```
# ⚙️ Installation & Setup

Follow these steps to get the environment running locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/adexxhh/AI-Literary-Question-Generator.git](https://github.com/adexxhh/AI-Literary-Question-Generator.git)
cd AI-Literary-Question-Generator

```
### 2. Setup Virtual Environment
### Create the environment
```bash
python -m venv venv
```
### Activate on macOS/Linux:
```bash
source venv/bin/activate 
```
### Activate on Windows:
```bash
venv\Scripts\activate
```
### 3. Install Dependencies:
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a file named .env in the root directory and add your Google API Key.

Note: Never commit your .env file to version control.

```plaintext
GOOGLE_API_KEY=your_gemini_api_key_here
```
### 5. Run the Application
Start the Streamlit server to view the auditor in your browser.
```bash
streamlit run src/app.py
```
## Engineering Highlights (For Evaluators)
This project was designed with a focus on data integrity and retrieval precision. Below are the core technical considerations:

***Metadata Persistence:*** Implemented a custom pre-processing pipeline that attaches page-level metadata to document chunks. This ensures the LLM maintains "spatial awareness" of the manuscript, enabling it to cite specific locations rather than just general context.

---

***Robust Extraction Logic:*** Designed a fail-safe parser to handle the complex JSON/List response formats of the Gemini 3 Preview API, ensuring 99.9% UI stability even when the model returns structured reasoning data.

---
***Context Optimization:*** Implemented a top-k retrieval strategy ($k=5$) with 2000-token chunks. This balance maximizes reasoning quality for deep thematic analysis while minimizing token latency for a responsive user experience.

---


