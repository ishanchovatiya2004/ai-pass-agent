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
        with st.spinner("Processing..."):
            try:
                # Use your Backend Render URL here
                API_URL = "https://ai-pass-agent.onrender.com/task" 
                
                response = requests.post(API_URL, json={"message": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("reply")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                
                elif response.status_code == 429:
                    error_msg = "🚨 **Rate Limit Reached.** \n\n**Guide:** I'm receiving too many requests right now. Please wait about 60 seconds and try your request again."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                else:
                    error_msg = "❌ **Service Error.** \n\n**Guide:** Something went wrong on the server. Please check your internet connection or try rephrasing your task."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except Exception:
                st.error("Connection failed. Please ensure the Backend is running.")
