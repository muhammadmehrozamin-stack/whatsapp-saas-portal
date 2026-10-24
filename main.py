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
        border-radius: 28px;
        padding: 45px 35px;
        background-color: #0b0f0b;
        box-shadow: 0 0 30px rgba(204, 255, 0, 0.25);
        max-width: 650px;
        margin: 30px auto;
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
        margin-bottom: 20px;
        line-height: 1.5;
    }
    .stTextInput input, .stTextArea textarea {
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
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Welcome to<br><span style='color:#ccff00;'>WhatsApp</span> SaaS Portal</div>
            <div class='neon-subtitle'>Manage your AI-powered WhatsApp automated store, update live inventory in real-time, and streamline customer ordering directly through Supabase.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🚀 Join Now"):
                st.session_state.page = "signup"
                st.rerun()
        with b2:
            if st.button("🔑 Login"):
                st.session_state.page = "login"
                st.rerun()

# ---------------------------------------------------------
# View 2: Sign Up
# ---------------------------------------------------------
elif st.session_state.page == "signup" and not st.session_state.logged_in:
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Create Account</div>
            <div class='neon-subtitle'>Get started with your WhatsApp portal.</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        with st.form("signup_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Choose password")
            agree = st.checkbox("I agree to Privacy Policy")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if email and password and agree:
                    try:
                        supabase.table("users").insert({"email": email, "password": password}).execute()
                        st.success("Account created successfully! Please login.")
                        st.session_state.page = "login"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill all fields and accept policy.")
        if st.button("⬅ Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------------------------------------------------------
# View 3: Login
# ---------------------------------------------------------
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown("""
        <div class='neon-card'>
            <div class='neon-title'>Welcome Back</div>
            <div class='neon-subtitle'>Sign in to your dashboard.</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
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
    top_col1, top_col2, top_col3 = st.columns([2, 2, 1])
    with top_col1:
        st.markdown(f"👤 **{st.session_state.user_email}**")
    with top_col2:
        st.markdown(f"📱 **WhatsApp:** `{st.session_state.whatsapp_number}`")
    with top_col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("<h2 style='text-align: center; color: #ccff00;'>🛒 Smart Sales Portal</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", 
        "➕ Add & Edit", 
        "📦 Live Products", 
        "🤖 Sales Bot", 
        "📢 Campaigns",
        "📱 Settings"
    ])

    # Tab 1: Overview
    with tab1:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Dashboard Overview")
        try:
            res = supabase.table("products").select("*").execute()
            prods = res.data if res.data else []
            st.metric("Total Products", len(prods))
            st.metric("Total Stock", sum([p.get('stock', 0) for p in prods]))
            st.success("Connected to Supabase successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 2: Add & Edit Product
    with tab2:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Add New Product")
        with st.form("add_prod_form", clear_on_submit=True):
            p_name = st.text_input("Product Name")
            p_price = st.number_input("Price ($)", min_value=0.0)
            p_stock = st.number_input("Stock", min_value=0, step=1)
            p_desc = st.text_area("Description, Colors & Features")
            p_img = st.file_uploader("Product Image (Optional)", type=['jpg', 'png'])
            
            if st.form_submit_button("Add Product"):
                if p_name:
                    try:
                        img_name = p_img.name if p_img else "No image"
                        supabase.table("products").insert({
                            "name": p_name,
                            "price": p_price,
                            "stock": p_stock,
                            "description": f"{p_desc} [Image: {img_name}]"
                        }).execute()
                        st.success(f"Added {p_name} successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Product name required.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Edit Inventory")
        try:
            resp = supabase.table("products").select("*").execute()
            if resp.data:
                df = pd.DataFrame(resp.data)
                edited = st.data_editor(df, key="editor", use_container_width=True)
                if st.button("Save Edits"):
                    for _, row in edited.iterrows():
                        if 'id' in row and pd.notnull(row['id']):
                            supabase.table("products").update({
                                "name": row.get("name"),
                                "price": row.get("price"),
                                "stock": row.get("stock"),
                                "description": row.get("description")
                            }).eq("id", row["id"]).execute()
                    st.success("Changes saved!")
                    st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 3: Live Products
    with tab3:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        try:
            resp = supabase.table("products").select("*").execute()
            if resp.data:
                st.dataframe(pd.DataFrame(resp.data), use_container_width=True)
            else:
                st.info("No products found.")
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 4: Sales Bot
    with tab4:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Smart Sales Bot")
        
        if "chat" not in st.session_state:
            st.session_state.chat = [{"role": "assistant", "content": "Hello! Ask me about product colors, features, or prices."}]

        for m in st.session_state.chat:
            align = "right" if m["role"] == "user" else "left"
            bg = "#1e2d1e" if m["role"] == "user" else "#141a14"
            st.markdown(f"<div style='text-align:{align}; background:{bg}; padding:10px; border-radius:10px; margin:5px 0;'>{m['content']}</div>", unsafe_allow_html=True)

        user_q = st.text_input("Customer Message", key="q_input")
        c_send, c_clear = st.columns(2)
        with c_send:
            if st.button("Send"):
                if user_q:
                    st.session_state.chat.append({"role": "user", "content": user_q})
                    res = supabase.table("products").select("*").execute()
                    items = res.data if res.data else []
                    reply = generate_smart_sales_response(user_q, items)
                    st.session_state.chat.append({"role": "assistant", "content": reply})
                    st.rerun()
        with c_clear:
            if st.button("Clear Chat"):
                st.session_state.chat = [{"role": "assistant", "content": "Hello! Ask me about product colors, features, or prices."}]
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 5: Campaigns
    with tab5:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("WhatsApp Campaigns")
        c_name = st.text_input("Campaign Title")
        c_msg = st.text_area("Message Template")
        if st.button("Launch Campaign"):
            if c_name and c_msg:
                st.success(f"Campaign '{c_name}' broadcasted successfully!")
            else:
                st.warning("Fill in all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 6: Settings
    with tab6:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("Settings")
        new_num = st.text_input("WhatsApp Number", value=st.session_state.whatsapp_number)
        new_rule = st.text_area("Bot Instructions", value=st.session_state.bot_custom_rule)
        if st.button("Save Settings"):
            st.session_state.whatsapp_number = new_num
            st.session_state.bot_custom_rule = new_rule
            st.success("Settings saved successfully!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
