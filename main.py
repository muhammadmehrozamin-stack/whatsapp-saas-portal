import streamlit as st
from supabase import create_client
import pandas as pd
import json

# ---------------------------------------------------------
# Page Setup & Theme Styling
# ---------------------------------------------------------
st.set_page_config(page_title="WhatsApp SaaS Portal", layout="centered", page_icon="🟢")

st.markdown("""
    <style>
    .stApp {
        background-color: #050805;
        color: #ffffff;
    }
    .neon-card {
        border: 2px solid #ccff00;
        border-radius: 20px;
        padding: 25px;
        background-color: #0b0f0b;
        box-shadow: 0 0 20px rgba(204, 255, 0, 0.2);
        max-width: 750px;
        margin: 15px auto;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #141a14 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #283328 !important;
    }
    .stButton > button {
        background-color: #ccff00 !important;
        color: #050805 !important;
        font-weight: 800 !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100% !important;
        padding: 10px 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Initialize Supabase Client
# ---------------------------------------------------------
SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"
SUPABASE_KEY = "EyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyNDA4MTcsImV4cCI6MjEwNzgxNjgxN30.HLseuSvJAAWVxPRropNAMlTdmJyWownLt9YDqiVKXJM"

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
if "bot_custom_rule" not in st.session_state:
    st.session_state.bot_custom_rule = "Be friendly, highlight colors and features, push to close the order immediately."

# ---------------------------------------------------------
# Sales Response Engine
# ---------------------------------------------------------
def generate_smart_sales_response(prompt, items):
    prompt_lower = prompt.lower()
    is_urdu = any(w in prompt_lower for w in ['aoa', 'kya', 'hai', 'kaise', 'price', 'kitna', 'colour', 'color', 'rang', 'features'])
    
    matched_item = None
    for item in items:
        if item['name'].lower() in prompt_lower or any(w in prompt_lower for w in item['name'].lower().split()):
            matched_item = item
            break

    if is_urdu:
        if matched_item:
            return f"Waalikum Assalam! Ji bilkul, {matched_item['name']} available hai! Price: ${matched_item['price']} | Stock: {matched_item['stock']} units.\n\nFeatures & Colors: {matched_item['description']}\n\nKia order confirm kar dein?"
        return "Ji bilkul! Humare products premium features aur multiple colors mein available hain. Aapko kis product ki details chahiye?"
    else:
        if matched_item:
            return f"Hello! Yes, {matched_item['name']} is in stock! Price: ${matched_item['price']} ({matched_item['stock']} left).\n\nFeatures & Colors: {matched_item['description']}\n\nShall I lock this order for you?"
        return "Hello! Welcome to our store. Check out our latest inventory items and let me know what you would like to reserve today!"

# ---------------------------------------------------------
# View 1: Landing Page
# ---------------------------------------------------------
if st.session_state.page == "landing" and not st.session_state.logged_in:
    st.markdown("<div class='neon-card' style='text-align:center;'><h2>Welcome to <span style='color:#ccff00;'>WhatsApp</span> SaaS Portal</h2><p>Manage your AI-powered store and live inventory easily.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 Join Now"):
            st.session_state.page = "signup"
            st.rerun()
        if st.button("🔑 Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------------------------------------------------------
# View 2: Sign Up
# ---------------------------------------------------------
elif st.session_state.page == "signup" and not st.session_state.logged_in:
    st.markdown("<div class='neon-card' style='text-align:center;'><h2>Create Account</h2></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("signup_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            agree = st.checkbox("I agree to Privacy Policy")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if email and password and agree:
                    try:
                        supabase.table("users").insert({"email": email, "password": password}).execute()
                        st.success("Account created! Please login.")
                        st.session_state.page = "login"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill all fields and accept policy.")
        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------------------------------------------------------
# View 3: Login
# ---------------------------------------------------------
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("<div class='neon-card' style='text-align:center;'><h2>Login to Portal</h2></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                try:
                    res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error(f"Error: {e}")
        if st.button("Create Account instead"):
            st.session_state.page = "signup"
            st.rerun()

# ---------------------------------------------------------
# View 4: Dashboard
# ---------------------------------------------------------
elif st.session_state.logged_in:
    st.sidebar.markdown(f"### 👤 {st.session_state.user_email}")
    st.sidebar.
