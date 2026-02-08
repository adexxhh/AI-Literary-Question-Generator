import streamlit as st
import os
from dotenv import load_dotenv
from preprocess import load_and_split
from generator import get_question_generator_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

st.set_page_config(page_title="LitAI Auditor", layout="wide")
st.title("📚 LitAI: Structural Manuscript Auditor")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password") or os.getenv("GOOGLE_API_KEY")

    st.divider()
    st.subheader("📊 System Capabilities & Limits")
    st.info("""
    **How I Read:** I don't read the whole book at once. I use **Semantic Retrieval** to find the 5 most relevant sections (approx. 10,000 characters) related to your focus area.

    **Current Limits:**
    - **Max PDF Size:** ~200 pages (recommended).
    - **Context Window:** I analyze up to 5 sections per audit.
    - **Accuracy:** Best for structural analysis and specific character queries.
    """)

uploaded_file = st.file_uploader("Upload Manuscript (PDF/TXT)", type=['pdf', 'txt'])

if uploaded_file and api_key:
    # 1. Processing Logic
    if "vector_db" not in st.session_state:
        with st.spinner("Indexing Manuscript with Metadata..."):
            # Save temp file
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            chunks = load_and_split(temp_path)
            
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=api_key,
                task_type="retrieval_document"
            )
            
            st.session_state.vector_db = FAISS.from_documents(chunks, embeddings)
            st.success("Analysis Ready!")

    # --- Interaction Layer ---
    st.divider()
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Audit Focus")
        focus = st.text_area("What should the AI look for?", 
                            placeholder="e.g. Inconsistencies in character motivation or pacing issues in the middle act.")
        audit_btn = st.button("🔍 Run Deep Audit")

    with col2:
        if audit_btn and focus:
            with st.spinner("Simulating Editor's Mind..."):
                # 2. Retrieval with Metadata
                docs = st.session_state.vector_db.similarity_search(focus, k=5)
                
                context_texts = []
                for d in docs:
                    # In LangChain, page indices start at 0, so we add 1 for the user
                    page_num = d.metadata.get('page', 0) + 1
                    context_texts.append(f"[SOURCE: Page {page_num}]\n{d.page_content}")
                
                full_context = "\n\n---\n\n".join(context_texts)

                # 3. Generation
                chain = get_question_generator_chain(api_key)
                
                # We call the chain with both context and the focus query
                response = chain.invoke({"context": full_context, "query": focus})

                # --- Bulletproof Content Extraction ---
                # This handles strings, dictionaries, or LangChain Message objects
                result_text = ""
                try:
                    if hasattr(response, 'content'):
                        
                        content_data = response.content
                    else: 
                        content_data = response
                    if isinstance(content_data, list):
                        parts = []
                        for item in content_data:
                            if isinstance(item, dict) and 'text' in item:
                                parts.append(item['text'])
                            else:
                                parts.append(str(item))
                        result_text = "\n".join(parts)
                    else:
                        result_text = str(content_data)  
                    # 3. Final Clean-up (Remove API signatures and JSON noise)

                    if "'extras':" in result_text:
                        result_text = result_text.split("'extras':")[0]

                    # Strip any trailing characters that look like JSON leftovers
                    result_text = result_text.strip().rstrip('}]').rstrip(',').strip()
                
                except Exception as e:
                    result_text = f"🚨 Extraction Error: {e}\n\nShowing Raw Data:\n{str(response)}"

                  

        


                st.subheader("Editor's Critical Report")
                st.markdown(result_text)
                
                # Industry touch: Export functionality
                st.download_button(
                    label="📄 Download Audit Report",
                    data=result_text,
                    file_name="manuscript_audit.md",
                    mime="text/markdown"
                )