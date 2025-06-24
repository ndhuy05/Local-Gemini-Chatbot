import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

st.set_page_config(page_title="LangChain Chatbot", page_icon="💬")

st.title("LangChain AI Chatbot")
st.markdown("Ask any question and get answers from the AI using LangChain.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    memory = ConversationBufferMemory()
    st.session_state.conversation = ConversationChain(
        llm=model,
        memory=memory,
        verbose=False
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.conversation.predict(input=user_input)
                st.write(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")

with st.sidebar:
    st.title("About")
    st.info("This is a chatbot powered by LangChain and Google's Gemini model.")
    
    st.subheader("Model Options")
    model_option = st.selectbox(
        "Choose a model:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
        index=0
    )
    
    temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    if st.button("Update Model"):
        model = ChatGoogleGenerativeAI(model=model_option, temperature=temperature)
        memory = ConversationBufferMemory()  # Reset memory when changing models
        st.session_state.conversation = ConversationChain(
            llm=model,
            memory=memory,
            verbose=False
        )
        st.success(f"Model updated to {model_option} with temperature {temperature}")
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        model = ChatGoogleGenerativeAI(model=model_option, temperature=temperature)
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain(
            llm=model,
            memory=memory,
            verbose=False
        )
        st.rerun()
