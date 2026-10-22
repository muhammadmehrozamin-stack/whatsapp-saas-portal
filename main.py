import streamlit as st
from supabase import create_client
import pandas as pd

# ---------------------------------------------------------
# Page Setup & Theme Styling (Neon Dark Theme with WhatsApp Branding)
# ---------------------------------------------------------
st.set_page_config(page_title="WhatsApp SaaS Portal", layout="centered", page_icon="🟢")

st.markdown("""
    <style>
    /* Dark background styling */
    .stApp {
        background-color: #0b0f0b;
        color: #ffffff;
    }
    
    /* Neon green border container style */
    .neon-card {
        border: 2px solid #ccff00;
        border-radius: 20px;
        padding: 30px;
        background-color: #121612;
        box-shadow: 0 0 15px rgba(204, 255, 0, 0.2);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .neon-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .neon-subtitle {
        color: #ccff00;
        font-size: 14px;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #212521 !important;
        color: #ffffff !important;
        border-radius: 25px !important;
        border: 1px solid #333333 !important;
        padding-left: 15px !important;
    }

    /* Primary button styling */
    .stButton > button {
        background-color: #ccff00 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        width: 100% !important;
        padding: 10px 0px !important;
    }
    .stButton > button:hover {
        background-color: #b3e600 !important;
        color: #000000 !important;
        box-shadow: 0 0 10px rgba(204, 255, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# WhatsApp SVG Icon HTML helper
whatsapp_icon_html = """
<div style="text-align: center; margin-bottom: 10px;">
    <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#25D366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
    </svg>
</div>
"""

# ---------------------------------------------------------
# Initialize Supabase Client
# ---------------------------------------------------------
SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1MzAyOTEsImV4cCI6MjA1NjEwNjI5MX0.Qp-_7W5Gq6Q0Xp5xVvD4oJp6K3lY0q-4S5T9Xf7qSgE"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Session State Variables
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------------------------------------------------------
# View 1: Landing Page
# ---------------------------------------------------------
if st.session_state.page == "landing" and not st.session_state.logged_in:
    st.markdown(whatsapp_icon_html, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to WhatsApp SaaS Portal</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='text-align: center; color: #a0a0a0; font-size: 18px;'>
            Manage your AI-powered WhatsApp automated store, update live inventory in real-time, 
            and streamline customer ordering directly through Supabase.
        </p>
    """, unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Join Now"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("🔑 Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------------------------------------------------------
# View 2: Sign Up Dialog Box
# ---------------------------------------------------------
elif st.session_state.page == "signup" and not st.session_state.logged_in:
    st.markdown(whatsapp_icon_html, unsafe_allow_html=True)
    st.markdown("""
        <div class="neon-card">
            <div class="neon-title">Welcome to Portal</div>
            <div class="neon-subtitle">Create an account to start</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Choose password")
        agree = st.checkbox("I agree to Privacy Policy")
        submit_signup = st.form_submit_button("Create Account")

        if submit_signup:
            if not email or not password:
                st.error("Please fill in all fields.")
            elif not agree:
                st.warning("You must agree to the Privacy Policy.")
            else:
                try:
                    res = supabase.table("users").insert({"email": email, "password": password}).execute()
                    st.success("🎉 Account created successfully! Please Login Now.")
                    st.session_state.page = "login"
                except Exception as e:
                    st.error(f"Error creating account: {e}")

    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------------------------------------------------
# View 3: Login Dialog Box
# ---------------------------------------------------------
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown(whatsapp_icon_html, unsafe_allow_html=True)
    st.markdown("""
        <div class="neon-card">
            <div class="neon-title">Welcome to Website</div>
            <div class="neon-subtitle">Sign in to Website</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        st.markdown("<p style='font-size:12px;'>I agree to <span style='color:#ccff00;'>Privacy Policy</span></p>", unsafe_allow_html=True)
        submit_login = st.form_submit_button("Login")

        if submit_login:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                try:
                    res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
                    if res.data and len(res.data) > 0:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid Email or Password.")
                except Exception as e:
                    st.error(f"Login error: {e}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Home"):
            st.session_state.page = "landing"
            st.rerun()
    with col2:
        if st.button("Create Account"):
            st.session_state.page = "signup"
            st.rerun()

# ---------------------------------------------------------
# View 4: Dashboard (2 Tabs: Add Product & Live Products)
# ---------------------------------------------------------
elif st.session_state.logged_in:
    st.sidebar.title(f"👤 {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "landing"
        st.rerun()

    st.title("🛒 Product Management Portal")

    tab1, tab2 = st.tabs(["➕ Add Product", "📦 Live Products & Inventory"])

    # Tab 1: Add Product Form
    with tab1:
        st.subheader("Add a New Product")
        with st.form("add_product_form", clear_on_submit=True):
            p_name = st.text_input("Product Name")
            p_price = st.number_input("Price ($)", min_value=0.0, step=1.0)
            p_stock = st.number_input("Stock Quantity", min_value=0, step=1)
            p_desc = st.text_area("Product Description")
            
            submit_prod = st.form_submit_button("Add Product to Store")

            if submit_prod:
                if not p_name:
                    st.error("Product name is required.")
                else:
                    try:
                        supabase.table("products").insert({
                            "name": p_name,
                            "price": p_price,
                            "stock": p_stock,
                            "description": p_desc
                        }).execute()
                        st.success(f"Successfully added '{p_name}' to inventory!")
                    except Exception as e:
                        st.error(f"Failed to add product: {e}")

    # Tab 2: Live Products & Inline Editing
    with tab2:
        st.subheader("Current Live Products")
        try:
            response = supabase.table("products").select("*").execute()
            data = response.data

            if data:
                df = pd.DataFrame(data)
                
                # Interactive Data Editor for Live Editing
                st.write("✏️ **Edit live values below and click 'Save Changes'**")
                edited_df = st.data_editor(df, num_rows="dynamic", key="product_editor")

                if st.button("💾 Save Changes to Supabase"):
                    try:
                        for idx, row in edited_df.iterrows():
                            if "id" in row and pd.notnull(row["id"]):
                                supabase.table("products").update({
                                    "name": row.get("name"),
                                    "price": row.get("price"),
                                    "stock": row.get("stock"),
                                    "description": row.get("description")
                                }).eq("id", row["id"]).execute()
                        st.success("All product changes saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving updates: {e}")
            else:
                st.info("No products found in live store. Add one in the 'Add Product' tab!")
        except Exception as e:
            st.error(f"Error loading products: {e}")
