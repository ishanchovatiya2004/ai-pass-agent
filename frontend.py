import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="AI-Pass Assistant", page_icon="🤖")
st.title("🤖 AI-Pass Chat Agent")
st.markdown("Automate your tasks by chatting with the agent below.")

# 2. Initialize Chat History (keeps the conversation visible)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input Area
if prompt := st.chat_input("How can I help you?"):
    # Add user message to UI and history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Call the FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Processing task..."):
            try:
                # Replace with your actual Render URL for live testing
                API_URL = "https://ai-pass-agent.onrender.com/task" 
                
                response = requests.post(API_URL, json={"message": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    # Formatted response for the user
                    answer = (
                        f"✅ **Task Recognized:** {data['task']}\n\n"
                        f"👤 **Participants:** {', '.join(data['participants'])}\n\n"
                        f"📊 **Logged to Sheet:** {'Yes' if data['logged_to_sheet'] else 'No'}"
                    )
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {e}")