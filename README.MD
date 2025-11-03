# Home-Appliance-Agent

The main goal is to create a functional web application, "Home-Appliance-Agent," that acts as a central "smart" manual for all of a user's home appliances. A user can upload PDF manuals for their TV, oven, microwave, coffee machine, etc., and give each one a name. They can then have a single conversation with an AI assistant. When the user asks, "How do I set the timer on my oven?" or "How to mute my TV," the application will load the correct manual, and find the answer based only on the content of that specific document.
### MVP
**Core Technologies**

* **Interface**: A web application built with Streamlit.

* **Framework**: The core application logic will be built using the LangChain framework.

* **LLM**: The application will use Google's Gemini as its core Language Model for generating answers.
* **Vector Store**: FAISS, with a separate local index created and stored for each uploaded manual.

### The Workflow

#### **1. New Appliance Indexing (When a User Adds a Manual)**

* **Upload**: The user uploads a PDF manual via the Streamlit interface.

* **Name**: The user assigns a unique name to that appliance (e.g., "LG TV," "Kitchen Oven," "Sony Soundbar").

* **Load & Split**: The application reads and extracts all text from the PDF, then breaks it into smaller, defined-size chunks.

* **Embed**: The app uses an embeddings model (like gemini-embedding-001) to convert each text chunk into a numerical vector.

* **Store & Register**: The app saves these vectors into a new, separate FAISS index (e.g., faiss_index_lg_tv). It then saves a "pointer" in a central JSON file, mapping the user's name to that index folder (e.g., {"LG TV": "faiss_index_lg_tv"}).
  
#### **2. Querying (When a User Asks a Question)**
This is a two-stage process that happens every time the user sends a message.

* **Select Appliance**: The user first selects which appliance they want to talk to from a dropdown list (e.g., "LG TV," "Kitchen Oven").
  
* **Load**: The app loads the specific FAISS index for that selected appliance (e.g., it loads the faiss_index_kitchen_oven store).
  
* **Chat**: The user asks their question (e.g., "How do I set the temperature?").

* **Retrieve (RAG)**: The app now performs the standard RAG workflow only on that single, relevant index:

  *  **Embed Question**: Convert the user's question into a vector using the same embeddings model.

  *  **Retrieve**: Search the vector database to find the most relevant document chunks based on the question's vector.

  *  **Generate**: Create a new prompt containing the user's original question and the retrieved text chunks.

  *  **Answer**: Send this combined prompt to an LLM and display the resulting answer to the user in the chat interface.
