elif nav == "Add Product":
        st.markdown("<h1 style='color: #ccff00;'>Add New Product</h1>", unsafe_allow_html=True)
        st.write("Add a new item to your WhatsApp store catalog.")
        
        with st.form("add_product_form"):
            prod_name = st.text_input("Product Name", placeholder="e.g., Ps5")
            
            # Currency and Price columns
            col_curr, col_price = st.columns([1, 2])
            with col_curr:
                currency = st.selectbox("Currency", ["USD ($)", "EUR (€)", "GBP (£)", "PKR (Rs)", "INR (₹)", "AED (د.إ)"])
            with col_price:
                prod_price = st.number_input("Price", min_value=0.0, format="%.2f")
                
            prod_stock = st.number_input("Stock Quantity", min_value=0, step=1)
            submit_product = st.form_submit_button("Save Product")
            
            if submit_product:
                if not prod_name:
                    st.error("Please enter a product name.")
                else:
                    try:
                        # Extract clean currency symbol/code (e.g., USD, PKR)
                        curr_code = currency.split(" ")[0]
                        supabase.table('products').insert({
                            "name": prod_name,
                            "price": prod_price,
                            "currency": curr_code,
                            "stock": prod_stock,
                            "user_email": st.session_state.user_email
                        }).execute()
                        st.success(f"🎉 Product '{prod_name}' successfully added with price {curr_code} {prod_price}!")
                    except Exception as e:
                        st.error(f"Error adding product: {e}")
