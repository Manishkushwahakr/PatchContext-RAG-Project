import os
import streamlit as st
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="PatchContext",
    page_icon="🩹",
    layout="wide"
)

st.title("🩹 PatchContext")
st.write("Ask questions about the FastAPI GitHub repository.")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found.")
    st.stop()


@st.cache_resource
def load_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )


vector_db = load_vector_db()

st.sidebar.success(f"Vectors: {vector_db.index.ntotal}")

retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 8,
        "fetch_k": 40,
        "lambda_mult": 0.4
    }
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are PatchContext.

Answer ONLY using the repository context.

If the context is insufficient, reply:
"I couldn't find enough evidence."

Repository Context:
{context}

Question:
{question}

Give a detailed markdown answer.

At the end include the sources.
""")

chain = prompt | llm | StrOutputParser()


def format_docs(docs):
    formatted = []

    for doc in docs:

        meta = doc.metadata

        if meta.get("type") == "issue":
            source = f"Issue #{meta.get('number')}"

        elif meta.get("type") == "pull_request":
            source = f"PR #{meta.get('number')}"

        elif meta.get("type") == "commit":
            source = f"Commit {meta.get('sha', '')[:7]}"

        else:
            source = "Unknown"

        formatted.append(
            f"""
SOURCE: {source}
TYPE: {meta.get('type')}

CONTENT:
{doc.page_content}
"""
        )

    return "\n\n".join(formatted)


question = st.text_input(
    "Ask a question",
    placeholder="How are dependencies managed in FastAPI?"
)

if st.button("Ask") and question:

    with st.spinner("Searching..."):

        docs = retriever.invoke(question)

        context = format_docs(docs)

        try:
            answer = chain.invoke({
                "context": context,
                "question": question
            })

            st.subheader("Answer")
            st.markdown(answer)

        except Exception as e:
            st.error("Gemini API Error")
            st.exception(e)

    with st.expander("Retrieved Documents"):

        for i, doc in enumerate(docs, 1):

            st.markdown(f"### Document {i}")
            st.json(doc.metadata)
            st.write(doc.page_content)
            st.divider()