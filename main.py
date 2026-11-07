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
    .neon-card { border: 2px solid #ccff00; border-radius: 28px; padding: 40px 30px; background-color: #0b0f0b; box-shadow: 0 0 30px rgba(204, 255, 0, 0.25); max-width: 650px; margin: 30px auto; text-align: center; }
    .neon-title { color: #ffffff; font-size: 32px; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .neon-subtitle { color: #9e9e9e; font-size: 14px; text-align: center; margin-bottom: 30px; line-height: 1.5; }
    .stTextInput input, .stTextArea textarea { background-color: #141a14 !important; color: #ffffff !important; border-radius: 20px !important; border: 1px solid #283328 !important; padding: 12px 18px !important; }
    .stButton > button { background-color: #ccff00 !important; color: #050805 !important; font-weight: 800 !important; border-radius: 30px !important; border: none !important; width: 100% !important; max-width: 320px !important; padding: 12px 20px !important; font-size: 15px !important; box-shadow: 0 0 20px rgba(204, 255, 0, 0.4); display: block; margin: 12px auto; }
    .stButton > button:hover { background-color: #b3e600 !important; box-shadow: 0 0 25px rgba(204, 255, 0, 0.7); }
    </style>
""", unsafe_allow_html=True)

SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyNDA4MTcsImV4cCI6MjEwNzgxNjgxN30."
    "HLseuSvJAAWVxPRropNAMlTdmJyWownLt9YDqiVKXJM"
)

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
    st.session_state.bot_custom_rule = "Elite AI sales closer."

def call_groq_api(p, inv, tr, rules, key):
    k = key or default_api_key
    if not k:
        return "Please enter Groq API Key in Settings!"
    try:
        sys_i = f"{rules}\nFAQ:\n{tr}\nINV:\n{inv}"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {k}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": sys_i}, {"role": "user", "content": p}],
            "temperature": 0.7
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        data = res.json()
        if res.status_code == 200:
            choices = data.get("choices", [])
            if choices:
                return choices[0]["message"]["content"]
            return "No response."
        return f"Error ({res.status_code})"
    except Exception as e:
        return f"Error: {e}"

# LANDING
if st.session_state.page == "landing" and not st.session_state.logged_in:
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Welcome to<br><span style='color:#ccff00;'>WhatsApp</span> SaaS</div>
            <div class='neon-subtitle'>Manage AI WhatsApp store and live inventory.</div>
    """, unsafe_allow_html=True)
    if st.button("Join Now"):
        st.session_state.page = "signup"
        st.session_state.signup_step = "form"
        st.rerun()
    if st.button("Login"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# SIGNUP
elif st.session_state.page == "signup" and not st.session_state.logged_in:
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Create Account</div>
            <div class='neon-subtitle'>Secure WhatsApp registration.</div>
        </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        if st.session_state.signup_step == "form":
            with st.form("signup_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                whatsapp = st.text_input("WhatsApp Number")
                agree = st.checkbox("Agree to Policy")
                if st.form_submit_button("Send OTP"):
                    if email and password and whatsapp and agree:
                        st.session_state.temp_email = email
                        st.session_state.temp_password = password
                        st.session_state.temp_whatsapp = whatsapp
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        st.session_state.signup_step = "otp"
                        st.success(f"OTP Code: {st.session_state.generated_otp}")
                    else:
                        st.warning("Fill all fields.")
        else:
            with st.form("otp_form"):
                entered = st.text_input("Enter OTP")
                if st.form_submit_button("Verify"):
                    if entered == st.session_state.generated_otp:
                        try:
                            supabase.table("users").insert({
                                "email": st.session_state.temp_email,
                                "password": st.session_state.temp_password,
                                "whatsapp_number": st.session_state.temp_whatsapp
                            }).execute()
                            st.success("Success!")
                            st.session_state.signup_step = "form"
                            st.session_state.page = "login"
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Invalid OTP.")
        if st.button("Back to Login"):
            st.session_state.signup_step = "form"
            st.session_state.page = "login"
            st.rerun()

# LOGIN
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Welcome Back</div>
            <div class='neon-subtitle'>Sign in to dashboard.</div>
        </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        with st.form("login_form"):
            email = st.text_input("Email", value="focusevingcoaching@gmail.com")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if email:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    try:
                        res = supabase.table("users").select("whatsapp_number").eq("email", email).execute()
                        if res.data and res.data[0].get("whatsapp_number"):
                            st.session_state.whatsapp_number = res.data[0].get("whatsapp_number")
                    except Exception:
                        pass
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Enter email.")
        if st.button("Create Account"):
            st.session_state.page = "signup"
            st.rerun()

# DASHBOARD
elif st.session_state.logged_in:
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.markdown(f"User: **{st.session_state.user_email}**")
    with c2:
        st.markdown(f"WhatsApp: `{st.session_state.whatsapp_number}`")
    with c3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("<h2 style='text-align: center; color: #ccff00;'>AI Sales Portal</h2>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6, t7 = st.tabs(["Overview", "Add/Edit", "Products", "Train", "AI Bot", "Campaigns", "Settings"])

    with t1:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        try:
            res = supabase.table("products").select("*").execute()
            prods = res.data if res.data else []
            st.metric("Total Products", len(prods))
            st.metric("Total Stock", sum([p.get('stock', 0) for p in prods]))
            st.success("Connected successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Add Product")
        with st.form("add_p", clear_on_submit=True):
            p_name = st.text_input("Name")
            p_price = st.number_input("Price", min_value=0.0)
            p_stock = st.number_input("Stock", min_value=0, step=1)
            p_desc = st.text_area("Description")
            if st.form_submit_button("Add"):
                if p_name:
                    supabase.table("products").insert({"name": p_name, "price": p_price, "stock": p_stock, "description": p_desc}).execute()
                    st.success("Added!")
        st.markdown("</div>", unsafe_allow_html=True)

    with t3:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        try:
            resp = supabase.table("products").select("*").execute()
            if resp.data:
                st.dataframe(pd.DataFrame(resp.data), use_container_width=True)
            else:
                st.info("No products.")
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with t4:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Train Bot")
        with st.form("train_f", clear_on_submit=True):
            q = st.text_input("Question")
            a = st.text_area("Answer")
            if st.form_submit_button("Save Rule"):
                if q and a:
                    supabase.table("training_faqs").insert({"question": q, "answer": a}).execute()
                    st.success("Saved!")
        st.markdown("</div>", unsafe_allow_html=True)

    with t5:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("AI Bot")
        if "chat" not in st.session_state:
            st.session_state.chat = [{"role": "assistant", "content": "Hello!"}]
        for m in st.session_state.chat:
            align = "right" if m["role"] == "user" else "left"
            bg = "#1e2d1e" if m["role"] == "user" else "#141a14"
            st.markdown(f"<div style='text-align:{align}; background:{bg}; padding:10px; border-radius:10px; margin:5px 0;'>{m['content']}</div>", unsafe_allow_html=True)
        user_q = st.text_input("Message", key="q_in")
        if st.button("Send"):
            if user_q:
                st.session_state.chat.append({"role": "user", "content": user_q})
                inv = json.dumps(supabase.table("products").select("*").execute().data or [])
                faq = json.dumps(supabase.table("training_faqs").select("*").execute().data or [])
                reply = call_groq_api(user_q, inv, faq, st.session_state.bot_custom_rule, st.session_state.groq_api_key)
                st.session_state.chat.append({"role": "assistant", "content": reply})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with t6:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Campaigns")
        st.text_input("Title")
        st.text_area("Message")
        if st.button("Broadcast"):
            st.success("Broadcasted!")
        st.markdown("</div>", unsafe_allow_html=True)

    with t7:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Settings")
        g_key = st.text_input("Groq API Key", value=st.session_state.groq_api_key, type="password")
        rule = st.text_area("Bot Instructions", value=st.session_state.bot_custom_rule)
        if st.button("Save Settings"):
            st.session_state.groq_api_key = g_key
            st.session_state.bot_custom_rule = rule
            st.success("Saved!")
        st.markdown("</div>", unsafe_allow_html=True)
