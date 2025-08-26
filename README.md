# Simple Chatbot — Hugging Face + Streamlit

This is a minimal chatbot you can deploy on Streamlit Community Cloud.

## Files
- `streamlit_app.py`
- `requirements.txt`

## Steps
1. Make a new **public GitHub repo** and upload these two files.
2. In Streamlit Community Cloud, click **New app**, pick your repo and `streamlit_app.py`.
3. In app settings, go to **Secrets** and add your Hugging Face token:
   ```
   HUGGINGFACE_API_TOKEN = your_token_here
   ```
4. Open your app URL, type in the chat box, and see replies.

If a model errors, switch to another in the sidebar dropdown.
