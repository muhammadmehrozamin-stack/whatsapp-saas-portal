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
    default_api_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    default_api_key = ""

if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = default_api_key

if "bot_custom_rule" not in st.session_state:
    st.session_state.bot_custom_rule = "You are an elite AI sales closer. Answer any query in any language, reference inventory, and close sales."

def call_groq_api(prompt, inventory_context, training_context, rules, api_key):
    key_to_use = api_key or default_api_key
    if not key_to_use:
        return "⚠️ Please enter your Groq API Key in the Settings tab! (Get a free key at console.groq.com)"
    
    try:
        system_instruction = f"{rules}\n\nMANUAL TRAINING / FAQ:\n{training_context}\n\nINVENTORY:\n{inventory_context}"
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key_to_use}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        
        if response.status_code == 200:
            choices_list = res_data.get("choices", [])
            if choices_list:
                return choices_list[0]["message"]["content"]
            return "No response generated."
        else:
            error_msg = res_data.get("error", {}).get("message", response.text)
            return f"API Error ({response.status_code}): {error_msg}"
            
    except Exception as e:
        return f"Error connecting to Groq API: {e}"

if st.session_state.page == "landing" and not st.session_state.logged_in:
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Welcome to<br><span style='color:#ccff00;'>WhatsApp</span> SaaS Portal</div>
            <div class='neon-subtitle'>Manage your AI-powered WhatsApp store and live inventory through Supabase.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🚀 Join Now"):
                st.session_state.page
