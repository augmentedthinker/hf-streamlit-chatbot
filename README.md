# Simple Chatbot — Hugging Face + Streamlit (Patched)

## Files
- `streamlit_app.py`
- `requirements.txt`

## Deploy (no terminal)
1. Create a **public** GitHub repo and upload both files.
2. In Streamlit Community Cloud → New app → select repo and main file `streamlit_app.py` → Deploy.
3. App → Manage app → Settings → **Secrets**:
```
HUGGINGFACE_API_TOKEN = "hf_your_token_here"
```
4. Reload the app. Choose a model in the sidebar. Type and send.

If you see `[401 Unauthorized]`, your token is missing or not quoted properly.  
If you see `[403 Forbidden]`, the model is gated; pick a different one or accept its license on Hugging Face.
