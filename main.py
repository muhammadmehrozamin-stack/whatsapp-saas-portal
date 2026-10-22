import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- Supabase Configuration ---
SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9mZSI6ImFub24iLCJpYXQiOjE2..."  # Keep your actual key here
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="WhatsApp AI SaaS Portal", page_icon="🤖", layout="wide")

st.title("🤖 WhatsApp AI Sales & Inventory Portal")
st.markdown("Manage your store products and view live inventory synced directly with your AI WhatsApp bot.")

# --- Tabs for Navigation ---
tab1, tab2, tab3 = st.tabs(["📦 Inventory Management", "👤 User Sign Up", "🔑 Login"])

# --- Tab 1: Inventory & Products ---
with tab1:
    st.subheader("Add Products to AI WhatsApp Bot Inventory")
    
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Product Name")
        p_price = st.number_input("Price", min_value=0.0, value=0.0)
    with col2:
        p_stock = st.number_input("Stock Quantity", min_value=0, value=0)
        
    p_desc = st.text_area("Product Description")
    
    if st.button("Add Product to Supabase", type="primary"):
        if p_name:
            try:
                response = supabase.table("products").insert({
                    "name": p_name,
                    "price": p_price,
                    "stock": p_stock,
                    "description": p_desc
                }).execute()
                st.success(f"Success! Product '{p_name}' added to Supabase.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter at least a product name.")

    st.divider()
    st.subheader("📊 Live Inventory Table")
    
    if st.button("Refresh Inventory List"):
        try:
            res = supabase.table("products").select("*").execute()
            data = res.data
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No products found in inventory.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

# --- Tab 2: User Sign Up ---
with tab2:
    st.subheader("Create a New Account")
    s_email = st.text_input("Email Address", key="s_email")
    s_pass = st.text_input("Password", type="password", key="s_pass")
    s_wa = st.text_input("WhatsApp Business Number", placeholder="+923001234567")
    
    if st.button("Create Account"):
        if s_email and s_pass:
            st.success(f"Account successfully created for {s_email}!")
        else:
            st.warning("Please fill in email and password.")

# --- Tab 3: Login ---
with tab3:
    st.subheader("Portal Login")
    l_email = st.text_input("Email Address", key="l_email")
    l_pass = st.text_input("Password", type="password", key="l_pass")
    
    if st.button("Login"):
        if l_email and l_pass:
            st.success("Logged in successfully!")
        else:
            st.warning("Please enter your login details.")