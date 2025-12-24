import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# O código agora procura pelas "etiquetas" SUPABASE_URL e SUPABASE_KEY
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
