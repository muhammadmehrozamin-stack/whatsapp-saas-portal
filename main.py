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
        "You are an elite, intelligent AI sales closer. Answer any customer question in any language (English, Urdu, Arabic, etc.), "
        "be extremely helpful and friendly like Gemini, and seamlessly bridge the conversation back to our live store products to close the sale."
    )

# ---------------------------------------------------------
# Advanced Intelligent Multilingual Sales Engine
# ---------------------------------------------------------
def generate_smart_sales_response(prompt, items, custom_rule):
    prompt_lower = prompt.lower()
    
    # Detect language / greetings
    is_urdu_hindi = any(word in prompt_lower for word in ['aoa', 'kya', 'hai', 'kaise', 'bhai', 'price', 'kitna', 'mujhe', 'chahiye'])
    
    # Match product
    matched_item = None
    for item in items:
        if item['name'].lower() in prompt_lower or any(w in prompt_lower for w in item['name'].lower().split()):
            matched_item = item
            break

    if is_urdu_hindi:
        if matched_item:
            return f"Waalikum Assalam! Ji bilkul, *{matched_item['name']}* hamare paas available hai! 🔥 Price sirf **${matched_item['price']}** hai aur stock mein **{matched_item['stock']} units** baqi hain. _{matched_item['description']}_. \n\n*(Trainer Rule: {custom_rule})*\n\nKia mein apka order confirm kar dun taake express delivery karwa dein?"
        elif any(w in prompt_lower for w in ['kaise', 'haal', 'kya ho raha']):
            return f"Alhamdulillah bilkul theek! Aap sunayein, aaj aapko konsi gaming gear ya item chahiye? Humare paas best items mojood hain. *(Trainer Rule: {custom_rule})*"
        else:
            best_item = items[0] if items else {"name": "Gaming Product", "price": "200,000", "stock": 10}
            return f"Aapka sawal bohat acha hai! Humare store par is waqt top-rated **{best_item['name']}** mojood hai sirf **${best_item['price']}** mein. *(Trainer Rule: {custom_rule})* Bataiye, kya isko lock kar dein?"
    else:
        if matched_item:
            return f"Hello! Yes, the *{matched_item['name']}* is currently in stock! 🔥 Price is **${matched_item['price']}** with {matched_item['stock']} units ready. _{matched_item['description']}_. \n\n*(Trainer Rule: {custom_rule})*\n\nShall I lock this order in for you right now?"
        elif "hello" in prompt_lower or "hi" in prompt_lower:
            return f"Hello! 👋 Welcome to our store. How can I help you today? *(Trainer Rule: {custom_rule})*"
        else:
            best_item = items[0] if items else {"name": "Gaming Gear", "price": "200,000"}
            return f"That's a fascinating question! Regarding your query, while we assist with that, I also wanted to highlight our best-selling **{best_item['name']}** for **${best_item['price']}**. *(Trainer Rule: {custom_rule})* Would you like me to reserve one for you today?"

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
    st.sidebar.markdown(f"### 👤 {st.session_state.user_email}")
    st.sidebar.markdown(f"📱 **WhatsApp:** `{st.session_state.whatsapp_number}`")
    if st.sidebar.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.page = 'landing'
        st.rerun()

    st.markdown("<h2 style='text-align: center; color: #ccff00;'>🛒 Smart Sales Portal</h2>", unsafe_allow_html=True)
    st.write("")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        '📊 Overview', 
        '➕ Add & Edit', 
        '📦 Live Products', 
        '🤖 Smart Sales Bot', 
        '📢 Campaigns',
        '📱 WhatsApp & Trainer'
    ])

    # ---------------------------------------------------------
    # Tab 1: Overview
    # ---------------------------------------------------------
    with tab1:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("📊 Dashboard Overview")
        try:
            res = supabase.table('products').select('*').execute()
            prods = res.data
            total_items = len(prods) if prods else 0
            total_stock = sum([p.get('stock', 0) for p in prods]) if prods else 0
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Store Products", total_items)
            with col_b:
                st.metric("Total Warehouse Stock", total_stock)
                
            st.success("🟢 Supabase & Smart Sales Bot Fully Synced")
        except Exception as e:
            st.error(f"Error loading overview stats: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Tab 2: Add & Edit Product
    # ---------------------------------------------------------
    with tab2:
        st.markdown("<div class='neon-card' style='max-width:800px;'>", unsafe_allow_html=True)
        st.subheader('➕ Add a New Product')
        with st.form('add_product_form', clear_on_submit=True):
            p_name = st.text_input('Product Name')
            p_price = st.number_input('Price ($)', min_value=0.0, step=1.0)
            p_stock = st.number_input('Stock Quantity', min_value=0, step=1)
            p_desc = st.text_area('Product Description')
            
            submit_prod = st.form_submit_button('Add Product to Store')

            if submit_prod:
                if not p_name:
                    st.error('Product name is required.')
                else:
                    try:
                        supabase.table('products').insert({
                            'name': p_name,
                            'price': p_price,
                            'stock': p_stock,
                            'description': p_desc
                        }).execute()
                        st.success(f"Successfully added '{p_name}' to inventory!")
                        st.rerun()
                    except Exception as e:
                        st.error(f'Failed to add product: {e}')
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='neon-card' style='max-width:800px;'>", unsafe_allow_html=True)
        st.subheader('✏️ Manage Product Details')
        try:
            resp = supabase.table('products').select('*').execute()
            if resp.data:
                df_edit = pd.DataFrame(resp.data)
                edited_grid = st.data_editor(df_edit, num_rows='dynamic', key='manage_products_grid', use_container_width=True)
                
                if st.button('💾 Save Product Edits'):
                    try:
                        for idx, row in edited_grid.iterrows():
                            if 'id' in row and pd.notnull(row['id']):
                                supabase.table('products').update({
                                    'name': row.get('name'),
                                    'price': row.get('price'),
                                    'stock': row.get('stock'),
                                    'description': row.get('description')
                                }).eq('id', row['id']).execute()
                        st.success('Product details updated successfully!')
                        st.rerun()
                    except Exception as e:
                        st.error(f'Error saving edits: {e}')
            else:
                st.info("No products found to edit.")
        except Exception as e:
            st.error(f"Error loading inventory editor: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Tab 3: Live Products
    # ---------------------------------------------------------
    with tab3:
        st.markdown("<div class='neon-card' style='max-width: 900px;'>", unsafe_allow_html=True)
        st.subheader('📦 Live Inventory Manager')
        try:
            response = supabase.table('products').select('*').execute()
            data = response.data
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No products found in live store.")
        except Exception as e:
            st.error(f'Error loading products: {e}')
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Tab 4: Smart Sales Bot & Chat
    # ---------------------------------------------------------
    with tab4:
        st.markdown("<div class='neon-card' style='max-width: 850px;'>", unsafe_allow_html=True)
        st.subheader("🤖 Smart Multilingual Sales Bot")
        st.write("Test customer queries in any language (English, Urdu/Roman Urdu, etc.). The bot answers intelligently and closes sales using live inventory.")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "👋 Hello! Ask me anything in any language. I'm ready to assist and close sales!"}
            ]

        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"<div style='text-align:right; background:#1e2d1e; padding:10px 15px; border-radius:15px; margin:5px 0; color:#ccff00;'><b>Customer:</b> {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left; background:#141a14; padding:10px 15px; border-radius:15px; margin:5px 0; color:#ffffff; border: 1px solid #283328;'><b>🤖 Sales Closer:</b> {message['content']}</div>", unsafe_allow_html=True)

        customer_input = st.text_input("Ask a question or raise a query", placeholder="e.g., Aoa kya haal hai / Is the PS5 in stock?", key="sales_chat_input")
        
        col_send, col_clear = st.columns([2, 1])
        with col_send:
            send_btn = st.button("Send to Sales Bot")
        with col_clear:
            clear_btn = st.button("Clear Chat")

        if clear_btn:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "👋 Hello! Ask me anything in any language. I'm ready to assist and close sales!"}
            ]
            st.rerun()

        if send_btn and customer_input:
            st.session_state.chat_history.append({"role": "user", "content": customer_input})
            
            try:
                res = supabase.table('products').select('*').execute()
                items = res.data if res.data else []

                ai_reply = generate_smart_sales_response(
                    customer_input, 
                    items, 
                    st.session_state.bot_custom_rule
                )

                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.rerun()
            except Exception as e:
                st.error(f"Error in sales bot: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Tab 5: Campaigns
    # ---------------------------------------------------------
    with tab5:
        st.markdown("<div class='neon-card' style='max-width: 800px;'>", unsafe_allow_html=True)
        st.subheader("📢 WhatsApp Campaign Broadcasts")
        camp_title = st.text_input("Campaign Name", placeholder="e.g. Flash Sale")
        camp_msg = st.text_area("Broadcast Message Template", placeholder="Hello! Massive discounts available now.")
        if st.button("🚀 Launch Campaign"):
            if camp_title and camp_msg:
                st.success(f"✅ Campaign '{camp_title}' broadcasted via {st.session_state.whatsapp_number}!")
            else:
                st.warning("Please fill in all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Tab 6: WhatsApp & AI Trainer Settings
    # ---------------------------------------------------------
    with tab6:
        st.markdown("<div class='neon-card' style='max-width: 750px;'>", unsafe_allow_html=True)
        st.subheader("⚙️ WhatsApp & AI Sales Trainer")
        st.write("Update your business number and train your sales chatbot rules on the fly.")
        
        new_whatsapp_input = st.text_input("WhatsApp Business Number", value=st.session_state.whatsapp_number)
        rule_input = st.text_area("Sales Bot Persona & Closing Rules", value=st.session_state.bot_custom_rule)
        
        if st.button("💾 Save Settings & Training Rules"):
            st.session_state.whatsapp_number = new_whatsapp_input
            st.session_state.bot_custom_rule = rule_input
            st.success("🎉 Settings and sales training rules updated successfully!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
