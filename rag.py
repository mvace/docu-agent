import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
INSTRUCTIONS:
1. Answer the user's question based on the provided context.
2. If the user asks a general question, look for specific functions in the manual and describe those procedures.
3. If the explicit answer is not found, simply say "I don't have that information in the manual."
4. Answer in the same language as the user's question (Czech).


Context:
{context}

Question:
{question}
"""


@st.cache_resource
def get_embeddings_model():
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )


@st.cache_resource
def get_prompt_template():
    return ChatPromptTemplate.from_template(PROMPT_TEMPLATE)


@st.cache_resource
def get_retriever(appliance_name):
    embeddings = get_embeddings_model()

    vector_store = FAISS.load_local(
        f"faiss_index/{appliance_name}",
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vector_store.as_retriever()


def get_rag_answer(user_query, appliance_name):
    llm = get_llm()
    prompt = get_prompt_template()
    retriever = get_retriever(appliance_name)

    docs = retriever.invoke(user_query)
    context = "\n\n".join(doc.page_content for doc in docs)
    with st.expander("🔍 Debug: Zobrazit načtený kontext (Raw Context)"):
        st.text(context)
    prompt_input = {"context": context, "question": user_query}
    formatted_prompt = prompt.invoke(prompt_input)
    response_message = llm.invoke(formatted_prompt)
    answer = response_message.content

    return answer
