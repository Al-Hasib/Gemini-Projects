from dotenv import load_dotenv
import os
import textwrap
from IPython.display import display
from IPython.display import Markdown
import streamlit as st
import google.generativeai as genai

load_dotenv()

#get the API KEY from Google Gemini API
API_KEY = os.getenv("API_KEY")


st.subheader("Question Answering Chatbot with Gemini PRO API (FREE)")
# Initialize Gemini-pro
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Add a Gemini Chat History object to streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

def to_markdown(text):
    text = text.replace('.', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _:True))

# Provide Question to the input and Get the response from API
if prompt := st.chat_input("What can I do for you?"):
    # send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt)
    # display last LLM response, convert it to Markdown format
    response_markdown = to_markdown(response.text).data
    with st.chat_message("assistant"):
        st.write(f"**USER** : {prompt}")
        st.markdown(f"**BOT** : {response_markdown}")


# For visualizing the whole history of the chat, click on the history button.
if st.button("History"):
    for message in st.session_state.chat.history:
        with st.chat_message("assistant"):
            st.markdown(message.parts[0].text)

