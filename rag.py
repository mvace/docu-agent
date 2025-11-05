import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
You are a helpful assistant for answering questions about user manuals.
Answer the user's question based *only* on the following context.
If the answer is not found in the context, simply say "I don't have that information in the manual."
Do not make up answers.

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
    prompt_input = {"context": context, "question": user_query}
    formatted_prompt = prompt.invoke(prompt_input)
    response_message = llm.invoke(formatted_prompt)
    answer = response_message.content

    return answer
