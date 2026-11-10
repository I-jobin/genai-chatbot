import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------- Setup ----------
load_dotenv(override=True)

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Chatbot")
st.caption("Built with LangChain + Streamlit")

API_KEY = (
    os.getenv("GEM")
    or os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)
if not API_KEY:
    st.error(
        "API key not found. Add `GEM=your_key` to a `.env` file in the project "
        "root, then restart the app."
    )
    st.stop()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox(
        "Model",
        ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-2.5-pro"],
        index=0,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful, concise assistant.",
        height=120,
    )
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------- LangChain chain ----------
@st.cache_resource(show_spinner=False)
def build_chain(model: str, temp: float, system: str):
    llm = ChatGoogleGenerativeAI(
        model=model,
        temperature=temp,
        google_api_key=API_KEY,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system}"),
            MessagesPlaceholder("history"),
            ("human", "{input}"),
        ]
    )
    return prompt | llm | StrOutputParser()


chain = build_chain(model_name, temperature, system_prompt)

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of HumanMessage / AIMessage

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ---------- Chat input ----------
if user_input := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(
                chain.stream(
                    {
                        "system": system_prompt,
                        "history": st.session_state.messages,
                        "input": user_input,
                    }
                )
            )
        except Exception as e:
            reply = None
            st.error(f"Error: {e}")

    if reply:
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.session_state.messages.append(AIMessage(content=reply))