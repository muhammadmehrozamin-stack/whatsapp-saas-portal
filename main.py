import gradio as gr
from supabase import create_client, Client
import pandas as pd

# Initialize Supabase
SUPABASE_URL = "https://toymkibgrdopljphayar.supabase.co"  
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRveW1raWJncmRvcGxqcGhheWFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyNDA4MTcsImV4cCI6MjEwNzgxNjgxN30.HLseuSvJAAWVxPRropNAMlTdmJyWownLt9YDqiVKXJM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user(email, password):
    if not email or not password:
        return "Please fill in all fields."
    try:
        response = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
        if response.data:
            user = response.data[0]
            return f"✅ Login Successful! Welcome {user['email']}"
        else:
            return "❌ Invalid email or password."
    except Exception as e:
        return f"Error: {e}"

def signup_user(email, password, whatsapp):
    if not email or not password:
        return "Please fill in email and password."
    try:
        supabase.table("users").insert({
            "email": email,
            "password": password,
            "whatsapp_token": whatsapp
        }).execute()
        return "✅ Account created successfully!"
    except Exception as e:
        return f"Error: {e}"

def add_product(name, price, stock, description):
    if not name or not price:
        return "Please provide product name and price."
    try:
        supabase.table("products").insert({
            "name": name,
            "price": float(price),
            "stock": int(stock) if stock else 0,
            "description": description
        }).execute()
        return f"✅ Product '{name}' added successfully!"
    except Exception as e:
        return f"Error: {e}"

def fetch_products():
    try:
        response = supabase.table("products").select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame(columns=["name", "price", "stock", "description"])
    except Exception:
        return pd.DataFrame(columns=["name", "price", "stock", "description"])

# Build Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 WhatsApp AI SaaS - Inventory Portal")
    
    with gr.Accordion("🔑 User Login", open=True):
        l_email = gr.Textbox(label="Email")
        l_pass = gr.Textbox(label="Password", type="password")
        l_btn = gr.Button("Login")
        l_output = gr.Textbox(label="Status")
        l_btn.click(login_user, inputs=[l_email, l_pass], outputs=l_output)
        
    with gr.Accordion("📝 User Sign Up", open=False):
        s_email = gr.Textbox(label="Email")
        s_pass = gr.Textbox(label="Password", type="password")
        s_wa = gr.Textbox(label="WhatsApp Business Number", placeholder="+923001234567")
        s_btn = gr.Button("Create Account")
        s_output = gr.Textbox(label="Status")
        s_btn.click(signup_user, inputs=[s_email, s_pass, s_wa], outputs=s_output)

    with gr.Accordion("📦 Manage Store Products & Inventory", open=False):
        gr.Markdown("Add products for your AI WhatsApp Bot inventory:")
        p_name = gr.Textbox(label="Product Name")
        p_price = gr.Number(label="Price")
        p_stock = gr.Number(label="Stock Quantity")
        p_desc = gr.Textbox(label="Product Description")
        p_btn = gr.Button("Add Product to Supabase")
        p_output = gr.Textbox(label="Status")
        
        gr.Markdown("### 📋 Live Inventory Table:")
        refresh_btn = gr.Button("Refresh Inventory List")
        product_table = gr.DataFrame()

        p_btn.click(add_product, inputs=[p_name, p_price, p_stock, p_desc], outputs=p_output)
        refresh_btn.click(fetch_products, outputs=product_table)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)