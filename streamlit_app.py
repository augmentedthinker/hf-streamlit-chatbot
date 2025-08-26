# streamlit_app.py
# Minimal browser chatbot using Hugging Face Inference API + Streamlit

import os
import requests
import streamlit as st

st.set_page_config(page_title="Simple Chatbot (HF + Streamlit)", layout="centered")

st.title("Simple Chatbot — Hugging Face + Streamlit")
st.caption("Type a message and press Send.")

# Sidebar: model selector and token status
with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model (pick another if one errors)",
        [
            "HuggingFaceH4/zephyr-7b-beta",
            "Qwen/Qwen2.5-1.5B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.2",
        ],
    )
    if "HUGGINGFACE_API_TOKEN" in st.secrets:
        st.success("API token found in secrets.")
    else:
        st.warning("No Hugging Face token set yet.")

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

def call_hf(model_id: str, prompt: str, token: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7, "return_full_text": False},
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        data = resp.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        if isinstance(data, dict) and "error" in data:
            return f"[API error] {data['error']}"
        return str(data)
    except Exception as e:
        return f"[Request error] {e}"

# Display past messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat input
prompt = st.chat_input("Type your message")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    token = st.secrets.get("HUGGINGFACE_API_TOKEN", None)
    if not token:
        reply = "Please set your Hugging Face API token in Streamlit Secrets."
    else:
        reply = call_hf(model, prompt, token)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
