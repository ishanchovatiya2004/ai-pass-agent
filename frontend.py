import streamlit as st
import requests

st.set_page_config(page_title="AI-Pass Assistant", page_icon="🤖")
st.title("🤖 AI-Pass Chat Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Change to your actual backend URL
            API_URL = "https://ai-pass-agent.onrender.com/task" 
            response = requests.post(API_URL, json={"message": prompt})
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("reply")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Backend Error. Please try again.")
        except Exception:
            st.error("Connection failed.")
