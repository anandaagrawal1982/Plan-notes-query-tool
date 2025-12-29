import streamlit as st
import asyncio
from fastmcp import Client
from google import genai
from google.genai import types

st.set_page_config(page_title="Care Manager Assistant", page_icon="🏥")
st.title("🏥 Benefit Query Assistant")

# Sidebar for configuration
with st.sidebar:
    st.header("Patient Context")
    plan_option = st.selectbox("Select Plan Sponsor", ["Sponsor_A", "Sponsor_B"])
    st.info("The AI will strictly use documents for the selected sponsor.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

async def get_ai_response(user_input, plan_id):
    print("Gemini client executing: ", user_input)
    mcp_client = Client("server.py")
    gemini_client = genai.Client(api_key="xxxx")
    
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Patient Plan: {plan_id}. Question: {user_input}",
            config=types.GenerateContentConfig(
                tools=[mcp_client.session],
                system_instruction="You are a care manager assistant. Use query_benefits to answer based ONLY on the provided plan."
            )
        )
        return response.text

# Chat input
if prompt := st.chat_input("Ask about plan benefits..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = asyncio.run(get_ai_response(prompt, plan_option))
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})