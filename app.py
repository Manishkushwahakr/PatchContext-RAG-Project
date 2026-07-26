import os
import streamlit as st
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------------------------------------------
# Streamlit Page
# ---------------------------------------------------
st.set_page_config(
    page_title="PatchContext",
    page_icon="🩹",
    layout="wide"
)

st.title("🩹 PatchContext")
st.write("Ask questions about the FastAPI GitHub repository.")

# ---------------------------------------------------
# Load FAISS
# ---------------------------------------------------
@st.cache_resource
def load_vector_db():

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


vector_db = load_vector_db()

st.sidebar.success(f"FAISS Loaded: {vector_db.index.ntotal} vectors")

# ---------------------------------------------------
# Retriever
# ---------------------------------------------------
retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 8,
        "fetch_k": 40,
        "lambda_mult": 0.4
    }
)

# ---------------------------------------------------
# Gemini
# ---------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# ---------------------------------------------------
# Prompt
# ---------------------------------------------------
prompt = ChatPromptTemplate.from_template("""
You are PatchContext.

You answer ONLY using the repository context below.

If the answer is partially available,
combine information from multiple documents.

Never invent facts.

Repository Context:
{context}

Question:
{question}

Return:

- Detailed answer
- Sources used
""")

parser = StrOutputParser()

chain = prompt | llm | parser

# ---------------------------------------------------
# Format Documents
# ---------------------------------------------------
def format_docs(docs):

    formatted = []

    for doc in docs:

        meta = doc.metadata

        if meta.get("type") == "issue":
            source = f"Issue #{meta.get('number')}"

        elif meta.get("type") == "pull_request":
            source = f"PR #{meta.get('number')}"

        elif meta.get("type") == "commit":
            source = f"Commit {meta.get('sha','')[:7]}"

        else:
            source = "Unknown"

        formatted.append(f"""
==============================
SOURCE: {source}
TYPE: {meta.get("type")}

CONTENT:
{doc.page_content}
==============================
""")

    return "\n".join(formatted)

# ---------------------------------------------------
# UI
# ---------------------------------------------------
question = st.text_input(
    "Ask a question",
    placeholder="How are dependencies managed in FastAPI?"
)

if st.button("Ask"):

    with st.spinner("Searching..."):

        docs = retriever.invoke(question)

        st.sidebar.info(f"Retrieved Documents: {len(docs)}")

        context = format_docs(docs)

        answer = chain.invoke({
            "context": context,
            "question": question
        })

    # -----------------------------
    # Answer
    # -----------------------------
    st.subheader("Answer")
    st.markdown(answer)

    # -----------------------------
    # Debug Context
    # -----------------------------
    with st.expander("Context Sent To Gemini"):

        st.text(context)

    # -----------------------------
    # Retrieved Documents
    # -----------------------------
    st.subheader("Retrieved Documents")

    for i, doc in enumerate(docs, 1):

        with st.expander(f"Document {i}"):

            st.json(doc.metadata)

            st.write(doc.page_content)