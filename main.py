import streamlit as st
from supabase import create_client
import pandas as pd
import urllib.request
import json
import random

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
        padding: 35px 25px;
        background-color: #0b0f0b;
        box-shadow: 0 0 30px rgba(204, 255, 0, 0.25);
        max-width: 650px;
        margin: 20px auto;
        text-align: center;
    }
    .neon-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    .neon-subtitle {
        color: #9e9e9e;
        font-size: 14px;
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
        padding: 12px 20px !important;
        font-size: 15px !important;
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
SUPABASE_URL = "
