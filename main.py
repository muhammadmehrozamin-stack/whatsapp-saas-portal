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
    .neon-subtitle { color: #9e9e9e; font-size: 14px; text-align
