# streamlit_app.py (patched, final)
import requests
import streamlit as st

st.set_page_config(page_title="Simple Chatbot (HF + Streamlit)", layout="centered")
st.title("Simple Chatbot — Hugging Face + Streamlit")
st.caption("Type a message and press Send. If a model errors, pick another from the sidebar.")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model (choose another if one errors)",
        [
            "Qwen/Qwen2.5-1.5B-Instruct",
            "HuggingFaceH4/zephyr-7b-beta",
            "mistralai/Mistral-7B-Instruct-v0.2",
        ],
        index=0
    )
    if "HUGGINGFACE_API_TOKEN" in st.secrets:
        st.success("API token found in secrets.")
    else:
        st.warning('Add HUGGINGFACE_API_TOKEN = "hf_..." in Settings → Secrets.')

if "messages" not in st.session_state:
    st.session_state.messages = []

def call_hf(model_id: str, user_text: str, token: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    payload = {
        "inputs": user_text,
        "parameters": {"max_new_tokens": 256, "temperature": 0.7, "return_full_text": False},
        "options": {"wait_for_model": True, "use_cache": True}
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=90)
        try:
            data = r.json()
        except Exception:
            txt = r.text.strip()
            if r.status_code == 401:
                return "[401 Unauthorized] Check your HUGGINGFACE_API_TOKEN in Secrets (wrap in quotes)."
            if r.status_code == 403:
                return "[403 Forbidden] Model is gated or requires license acceptance on Hugging Face."
            if txt:
                return f"[HTTP {r.status_code}] {txt[:400]}"
            return f"[HTTP {r.status_code}] Empty response"
        if isinstance(data, dict) and "error" in data:
            return f"[HF error] {data['error']}"
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        return str(data)
    except requests.exceptions.RequestException as e:
        return f"[Network error] {e}"

# render previous messages
for m in st.session_state.messages:
    with st.chat_message(m.get("role","assistant")):
        st.markdown(m["content"])

prompt = st.chat_input("Type your message")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    token = st.secrets.get("HUGGINGFACE_API_TOKEN")
    if not token:
        reply = 'Please add HUGGINGFACE_API_TOKEN = "hf_..." in Settings → Secrets.'
    else:
        reply = call_hf(model, prompt, token)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"): st.markdown(reply)
