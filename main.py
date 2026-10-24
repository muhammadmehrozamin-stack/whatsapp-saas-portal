import streamlit as st
from supabase import create_client
import pandas as pd
import json

# ---------------------------------------------------------
# Page Setup & Theme Styling
# ---------------------------------------------------------
st.set_page_config(page_title='WhatsApp SaaS Portal', layout='centered', page_icon='🟢')

st.markdown('''
    <style>
    .stApp {
        background-color: #050805;
        color: #ffffff;
    }
    
    .neon-card {
        border: 2px solid #ccff00;
        border-radius: 28px;
        padding: 45px 35px;
        background-color: #0b0f0b;
        box-shadow: 0 0 30px rgba(204, 255, 0, 0.25);
        max-width: 750px;
        margin: 20px auto;
        text-align: center;
    }
    
    .neon-title {
        color: #ffffff;
        font-size: 34px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .neon-subtitle {
        color: #9e9e9e;
        font-size: 15px;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.5;
    }

    .stTextInput > div > div > input, .stPasswordInput > div > div > input, .stTextArea textarea {
        background-color: #141a14 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid #283328 !important;
        padding: 12px 18px !important;
    }

    .stButton > button {
        background-color: #ccff00 !important;
        color: #050805 !important;
        font-weight: 800 !important;
        border-radius: 30px !important;
        border: none !important;
        width: 100% !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
        box-shadow: 0 0 20px rgba(204, 255, 0, 0.4);
    }
    .stButton > button:hover {
        background-color: #b3e600 !important;
        box-shadow: 0 0 25px rgba(204, 255, 0, 0.7);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0e140e;
        padding: 8px;
        border-radius: 18px;
        border: 1px solid #222e22;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #162016;
        border-radius: 12px;
        color: white;
        padding: 8px 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ccff00 !important;
        color: #000000 !important;
    }
    </style>
''', unsafe_allow_html=True)

# ---------------------------------------------------------
# Initialize Supabase Client
# ---------------------------------------------------------
SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"
SUPABASE_KEY = "EyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyNDA4MTcsImV4cCI6MjEwNzgxNjgxN30.HLseuSvJAAWVxPRropNAMlTdmJyWownLt9YDqiVKXJM"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ''
if 'whatsapp_number' not in st.session_state:
    st.session_state.whatsapp_number = '+92 300 0000000'

if 'bot_custom_rule' not in st.session_state:
    st.session_state.bot_custom_rule = (
        "You are an elite AI sales closer. Answer any customer question in any language (English, Urdu, Arabic, etc.), "
        "be extremely helpful and friendly, and seamlessly bridge the conversation back to our live store products and colors to close the sale."
    )

# ---------------------------------------------------------
# Intelligent Multilingual Sales Engine (Cleaned: No trainer text in replies)
# ---------------------------------------------------------
def generate_smart_sales_response(prompt, items):
    prompt_lower = prompt.lower()
    
    is_urdu_hindi = any(word in prompt_lower for word in ['aoa', 'kya', 'hai', 'kaise', 'bhai', 'price', 'kitna', 'mujhe', 'chahiye', 'colour', 'rang', 'features'])
    
    matched_item = None
    for item in items:
        if item['name'].lower() in prompt_lower or any(w in prompt_lower for w in item['name'].lower().split()):
            matched_item = item
            break

    if is_urdu_hindi:
        if matched_item:
            return f"Waalikum Assalam! Ji bilkul, *{matched_item['name']}* available hai! 🔥 Price sirf **${matched_item['price']}** hai aur stock mein **{matched_item['stock']} units** baqi hain. \n\n📝 Details & Features: _{matched_item['description']}_\n\nKia mein apka order confirm kar dun taake express delivery karwa dein?"
        elif any(w in prompt_lower for w in ['colour', 'rang', 'features', 'details', 'batao']):
            return f"Ji bilkul! Humare paas jo items available hain unki premium build quality, multiple color options, aur advanced features hain. Aapko kis specific product ka color ya feature pochna hai?"
        elif any(w in prompt_lower for w in ['kaise', 'haal']):
            return f"Alhamdulillah bilkul theek! Aap sunayein, aaj aapko konsi item chahiye? Humare paas best products mojood hain."
        else:
            best_item = items[0] if items else {"name": "Gaming Product", "price": "200,000", "stock": 10}
            return f"Aapka sawal bohat acha hai! Humare store par is waqt top-rated **{best_item['name']}** mojood hai sirf **${best_item['price']}** mein. Bataiye, kya isko lock kar dein?"
    else:
        if matched_item:
            return f"Hello! Yes, the *{matched_item['name']}* is currently in stock! 🔥 Price is **${matched_item['price']}** with {matched_item['stock']} units ready. \n\n📝 Features & Details: _{matched_item['description']}_\n\nShall I lock this order in for you right now?"
        elif any(w in prompt_lower for w in ['colour', 'color', 'features', 'specs']):
            return f"Our products feature top-tier premium finishes, multi-color availability, and high-performance specs! Let me know which product you're looking at and I'll give you all the details."
        elif "hello" in prompt_lower or "hi" in prompt_lower:
            return f"Hello! 👋 Welcome to our store. How can I help you close a great deal today?"
        else:
            best_item = items[0] if items else {"name": "Gaming Gear", "price": "200,000"}
            return f"That's a great question! Regarding your query, while we assist with that, I wanted to highlight our best-selling **{best_item['name']}** for **${best_item['price']}**. Would you like me to reserve one for you today?"

# ---------------------------------------------------------
# View 1: Landing Page
# ---------------------------------------------------------
if st.session_state.page == 'landing' and not st.session_state.logged_in:
    st.markdown('''
        <div style="text-align: center; margin-bottom: 15px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="65" height="65" viewBox="0 0 24 24" fill="none" stroke="#25D366" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
        </div>
        <div class="neon-card">
            <div class="neon-title">Welcome to<br><span style="color:#ccff00;">WhatsApp</span> SaaS Portal</div>
            <div class="neon-subtitle">
                Manage your AI-powered WhatsApp automated store, update live inventory in real-time, and streamline customer ordering directly through Supabase.
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        b1, b2 = st.columns(2)
        with b1:
            if st.button('🚀 Join Now'):
                st.session_state.page = 'signup'
                st.rerun()
        with b2:
            if st.button('🔑 Login'):
                st.session_state.page = 'login'
                st.rerun()

# ---------------------------------------------------------
# View 2: Sign Up Modal Card
# ---------------------------------------------------------
elif st.session_state.page == 'signup' and not st.session_state.logged_in:
    st.markdown('''
        <div style="text-align: center; margin-bottom: 15px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="65" height="65" viewBox="0 0 24 24" fill="none" stroke="#25D366" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
        </div>
        <div class="neon-card">
            <div class="neon-title">Welcome to Portal</div>
            <div class="neon-subtitle">Create an account to start.</div>
        </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        with st.form('signup_form'):
            email = st.text_input('Email', placeholder='Enter your email')
            password = st.text_input('Password', type='password', placeholder='Choose password')
            agree = st.checkbox('I agree to Privacy Policy')
            submit_signup = st.form_submit_button('Create Account')

            if submit_signup:
                if not email or not password:
                    st.error('Please fill in all fields.')
                elif not agree:
                    st.warning('You must agree to the Privacy Policy.')
                else:
                    try:
                        supabase.table('users').insert({'email': email, 'password': password}).execute()
                        st.success('🎉 Account created successfully! Please Login Now.')
                        st.session_state.page = 'login'
                        st.rerun()
                    except Exception as e:
                        st.error(f'Error creating account: {e}')

        st.markdown("<p style='text-align:center; font-size:14px; margin-top:15px;'>Already have an account?</p>", unsafe_allow_html=True)
        if st.button('Login now'):
            st.session_state.page = 'login'
            st.rerun()

# ---------------------------------------------------------
# View 3: Login Modal Card
# ---------------------------------------------------------
elif st.session_state.page == 'login' and not st.session_state.logged_in:
    st.markdown('''
        <div style="text-align: center; margin-bottom: 15px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="65" height="65" viewBox="0 0 24 24" fill="none" stroke="#25D366" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
        </div>
        <div class="neon-card">
            <div class="neon-title">Welcome to Website</div>
            <div class="neon-subtitle">Sign in to Website</div>
        </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        with st.form('login_form'):
            email = st.text_input('Email', placeholder='Enter your email')
            password = st.text_input('Password', type='password', placeholder='Enter your password')
            st.markdown("<p style='font-size:13px; color:#a0a0a0;'>I agree to <span style='color:#ccff00;'>Privacy Policy</span></p>", unsafe_allow_html=True)
            submit_login = st.form_submit_button('Login')

            if submit_login:
                if not email or not password:
                    st.error('Please fill in all fields.')
                else:
                    try:
                        res = supabase.table('users').select('*').eq('email', email).eq('password', password).execute()
                        if res.data and len(res.data) > 0:
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.page = 'dashboard'
                            st.rerun()
                        else:
                            st.error('Invalid Email or Password.')
                    except Exception as e:
                        st.error(f'Login error: {e}')

        st.markdown("<p style='text-align:center; font-size:14px; margin-top:10px; color:#ccff00;'>Forgot password?</p>", unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button('⬅ Back'):
                st.session_state.page = 'landing'
                st.rerun()
        with b2:
            if st.button('Create Account'):
                st.session_state.page = 'signup'
                st.rerun()

# ---------------------------------------------------------
# View 4: Dashboard with 6 Specialized Tabs
# ---------------------------------------------------------
elif st.session_state.logged_in:
    st.sidebar.markdown(f"### 👤 {st.
