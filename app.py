import streamlit as st
import random
import time
from pathlib import Path
import json

from vector_builder import create_vector_store
from db_handler import add_appliance, get_appliance_list

UPLOAD_DIRECTORY = Path("uploaded_pdfs")

# Ensure the upload directory exists
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

# --- Page Configuration ---
st.set_page_config(page_title="Home Appliance Agent", page_icon="🤖", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.header("Add a new user guide")
    with st.form(
        "upload_pdf_form", clear_on_submit=True, enter_to_submit=True, border=False
    ):
        # Input for Name
        appliance_name = st.text_input(
            "Name your appliance", placeholder="e.g., Whirlpool Microwave"
        )

        # PDF Uploader
        uploaded_file = st.file_uploader(
            "Upload a PDF", type=["pdf"], help="Upload your PDF file here."
        )

        # if uploaded_file:
        #     st.success(f"File '{uploaded_file.name}' added successfully!")
        #     file_name = uploaded_file.name

        submitted = st.form_submit_button("Add guide")
        if submitted:
            if uploaded_file and appliance_name is not None:
                file_path = UPLOAD_DIRECTORY / uploaded_file.name
                try:

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    create_vector_store(pdf=file_path, name=appliance_name)
                    add_appliance(appliance_name, appliance_name)
                    st.success(f"Successfully added guide for {appliance_name}!")

                except Exception as e:
                    st.error(f"Error saving file: {e}")
            else:
                st.error("Please provide both an appliance name and a PDF file.")


# --- Main Area ---
st.title("Home Appliance Agent")

# Dropdown Box
options = get_appliance_list()
dropdown_option = st.selectbox(
    "Choose an option:",
    options,
    index=0,
)


# st.write("You selected:", dropdown_option)


st.divider()

# --- Simple Chat Interface ---
st.header("Simple Chat Bot")
st.markdown("Ask a question, and the bot will give a random reply.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# List of random bot responses
bot_responses = [
    "That's an interesting question!",
    "I'm not sure I understand, can you rephrase?",
    "Let me think about that...",
    "Why do you ask that?",
    "Fascinating!",
    "Could you tell me more?",
]

# Get user input
prompt = st.chat_input("What is your question?")
if prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)

    # Generate and display bot response
    with st.chat_message("ai"):
        # Simulate thinking
        with st.spinner("Thinking..."):
            time.sleep(0.5)

        response = random.choice(bot_responses)
        st.markdown(response)

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
