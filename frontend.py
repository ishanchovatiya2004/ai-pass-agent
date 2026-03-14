import streamlit as st
import requests

st.set_page_config(page_title="AI-Pass Assistant", page_icon="🤖")
st.title("🤖 AI-Pass Chat Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # IMPORTANT: Use your actual Backend Render URL here
                API_URL = "https://ai-pass-agent.onrender.com/task" 
                
                response = requests.post(API_URL, json={"message": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    # Display the 'reply' field from the backend
                    answer = data.get("reply", "Task processed.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
