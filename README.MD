# Docu-Agent

The main goal is to create a functional web application "Docu-Agent" with a simple user interface. The user will be able to upload a document in PDF format and then have a conversation with an AI assistant who will answer questions based solely on the content of this document. In addition, the application will be able to extract key information from the text in a structured form on request.

### MVP
**Core Technologies**

* **Interface**: The application will be operated via a CLI (Command-Line Interface).

* **Framework**: The core application logic will be built using the LangChain framework.

* **LLM**: The application will use Google's Gemini as its core Language Model for generating answers.
  
**Document Ingestion (When a PDF is Uploaded)**

* **Load**: Read and extract all text from the uploaded PDF.

* **Split**: Break the extracted text into smaller, defined-size chunks.

* **Embed**: Use an embeddings model to convert each text chunk into a numerical vector.

* **Store**: Save these vectors (and their corresponding text chunks) into a vector database.

**Querying (When a User Asks a Question)**

* **Embed Question**: Convert the user's question into a vector using the same embeddings model.

* **Retrieve**: Search the vector database to find the most relevant document chunks based on the question's vector.

* **Generate**: Create a new prompt containing the user's original question and the retrieved text chunks.

* **Answer**: Send this combined prompt to an LLM and display the resulting answer to the user in the chat interface.