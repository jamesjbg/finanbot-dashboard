import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px
import os

# CONFIGURAÇÃO DE ACESSO (O Streamlit vai buscar os valores nos Secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Inicializa o cliente do Banco de Dados
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Erro na conexão com o banco: {e}")

st.set_page_config(page_title="FinanBot Dashboard", layout="wide")
st.title("📊 FinanBot - O Seu Painel Financeiro")

# Input para o utilizador
numero_telefone = st.text_input("Introduza o seu número de WhatsApp (com DDD):", placeholder="5511999999999")

if numero_telefone:
    try:
        res = supabase.table("chat_financeiro").select("*").eq("telefone", numero_telefone).execute()
        
        if res.data:
            df = pd.DataFrame(res.data)
            # ... (resto do código de gráficos que passei antes)
            st.write(f"Conectado! Encontramos {len(df)} registros.")
            st.dataframe(df)
        else:
            st.warning("Nenhum dado encontrado para este número.")
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
