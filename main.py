import streamlit as st
from supabase import create_client
import pandas as pd
import json
import random
import requests

st.set_page_config(page_title="WhatsApp SaaS Portal", layout="centered", page_icon="🟢")

st.markdown("""
    <style>
    .stApp { background-color: #050805; color: #ffffff; }
    .neon-card { border: 2px solid #ccff00; border-radius: 28px; padding: 35px 25px; background-color: #0b0f0b; box-shadow: 0 0 30px rgba(204, 255, 0, 0.25); max-width: 650px; margin: 20px auto; text-align: center; }
    .neon-title { color: #ffffff; font-size: 32px; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .neon-subtitle { color: #9e9e9e; font-size: 14px; text-align: center; margin-bottom: 20px; line-height: 1.5; }
    .stTextInput input, .stTextArea textarea { background-color: #141a14 !important; color: #ffffff !important; border-radius: 20px !important; border: 1px solid #283328 !important; padding: 12px 18px !important; }
    .stButton > button { background-color: #ccff00 !important; color: #050805 !important; font-weight: 800 !important; border-radius: 30px !important; border: none !important; width: 100% !important; padding: 12px 20px !important; font-size: 15px !important; box-shadow: 0 0 20px rgba(204, 255, 0, 0.4); }
    .stButton > button:hover { background-color: #b3e600 !important; box-shadow: 0 0 25px rgba(204, 255, 0, 0.7); }
    </style>
""", unsafe_allow_html=True)

SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyNDA4MTcsImV4cCI6MjEwNzgxNjgxN30.HLseuSvJAAWVxPRropNAMlTdmJyWownLt9YDqiVKXJM"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "whatsapp_number" not in st.session_state:
    st.session_state.whatsapp_number = "+92 300 0000000"
if "signup_step" not in st.session_state:
    st.session_state.signup_step = "form"
if "settings_otp_step" not in st.session_state:
    st.session_state.settings_otp_step = False

try:
    default_api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    default_api_key = ""

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = default_api_key

if "bot_custom_rule" not in st.session_state:
    st.session_state.bot_custom_rule = "You are an elite AI sales closer. Answer any query in any language, reference inventory, and close sales."

def call_gemini_api(prompt, inventory_context, training_context, rules, api_key):
    key_to_use = api_key or default_api_key
    if not key_to_use:
        return "⚠️ Please enter your API Key / Token in the Settings tab!"
    
    try:
        system_instruction = f"{rules}\n\nMANUAL TRAINING / FAQ:\n{training_context}\n\nINVENTORY:\n{inventory_context}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_instruction}\n\nCustomer Message: {prompt}"}
                    ]
                }
            ]
        }

        if key_to_use.startswith("AQ."):
            url = "https://aiplatform.googleapis.com/v1/projects/947348274030/locations/us-central1/publishers/google/models/gemini-1.5-flash:generateContent"
            headers = {
                'Authorization': f'Bearer {key_to_use}',
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=payload)
        else:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            headers = {'Content-Type': 'application/json'}
            params = {'key': key_to_use}
            response = requests.post(url, headers=headers, params=params, json=payload)
            
        res_data = response.json()
        
        if response.status_code == 200:
            candidates = res_data.get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"]
            return "No response generated."
        else:
            error_msg = res_data.get("error", {}).get("message", response.text)
            return f"API Error ({response.status_code}): {error_msg}"
            
    except Exception as e:
        return f"Error connecting to
