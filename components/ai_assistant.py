import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def floating_ai_chat():
    st.markdown("### 🤖 AI Assistant (Gemini API)")
    st.write("Ask questions about the dashboard, datasets, or cyber security.")

    # Generate a unique key per page
    page = st.session_state.get("current_page", "default")
    text_key = f"ai_question_{page}"
    btn_key = f"ai_button_{page}"

    # Input
    user_msg = st.text_input("Your question:", key=text_key)

    # Button
    ask = st.button("Ask Gemini", key=btn_key)

    if ask:
        if not user_msg.strip():
            st.warning("Please type a question.")
            return

        try:
            # ✔ Correct working model
            model = genai.GenerativeModel("models/gemini-pro-latest")

            response = model.generate_content(user_msg)

            st.markdown("#### Gemini answer:")
            st.write(response.text)

        except Exception as e:
            st.error(f"Gemini API Error: {e}")
