from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


def get_rag_answer(query_text, retriever, llm, prompt):
    # Combine Everything into a RAG Chain
    # 1. Retrieve: Get relevant documents from the vector store
    docs = retriever.invoke(query_text)

    # 2. Format Context: Combine the documents into a single string
    context = "\n\n".join(doc.page_content for doc in docs)

    # 3. Create Prompt Input: Prepare the dictionary for the prompt
    prompt_input = {"context": context, "question": query_text}

    # 4. Format Prompt: Fill in the template with context and question
    formatted_prompt = prompt.invoke(prompt_input)

    # 5. Call LLM: Send the formatted prompt to the language model
    response_message = llm.invoke(formatted_prompt)

    # 6. Parse Output: Get the plain text content from the response
    answer = response_message.content

    return answer


def main():
    # Load tools
    # Load the saved vector store and initialize the two models you'll need (the embedder and the generator).

    # Embedder
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Load vector_store
    vector_store = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )

    # LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Create the retriever
    # Create an object that knows how to take a string question, embed it (in the background), and search the vector store for relevant chunks.

    retriever = vector_store.as_retriever()

    # Build the prompt
    # Create a template for the prompt you will send to the LLM.

    template = """
    You are a helpful assistant for answering questions about user manuals.
    Answer the user's question based *only* on the following context.
    If the answer is not found in the context, simply say "I don't have that information in the manual."
    Do not make up answers.

    Context:
    {context}

    Question:
    {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # CLI
    # Create a simple Python script that continuously asks the user for a question and then prints a dummy answer, until they type "exit"
    while True:
        query = input("How can I help you? (Type 'exit' to quit) ")
        if query.lower() == "exit":
            break
        try:
            answer = get_rag_answer(query, retriever, llm, prompt)
            print("\nAnswer:\n", answer)
        except Exception as e:
            print(f"\nAn error occured {e}:")


if __name__ == "__main__":
    main()
