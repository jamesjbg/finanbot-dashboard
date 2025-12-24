import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# Configuração Segura (Secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Interface
st.set_page_config(page_title="DeltaBot Dashboard", layout="wide", page_icon="📈")

st.title("📊 DeltaBot - Inteligência Financeira Estratégica")
st.markdown("---")

with st.sidebar:
    st.header("👤 Identificação")
    numero_telefone = st.text_input("WhatsApp (ex: 559293530326):")
    st.info("O DeltaBot organiza seus dados em tempo real.")

if numero_telefone:
    try:
        res = supabase.table("chat_financeiro").select("*").eq("telefone", numero_telefone).execute()
        
        if res.data:
            df = pd.DataFrame(res.data)
            df['created_at'] = pd.to_datetime(df['created_at'])
            
            # Métricas
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Gasto", f"R$ {df['valor'].sum():.2f}")
            gastos_ir = df[df['dedutivel_ir'] == True]['valor'].sum()
            c2.metric("Total p/ IR", f"R$ {gastos_ir:.2f}")
            c3.metric("Lançamentos", len(df))

            # Gráficos
            col_a, col_b = st.columns(2)
            with col_a:
                fig_bar = px.bar(df, x='created_at', y='valor', title="Gastos no Tempo", color='estabelecimento')
                st.plotly_chart(fig_bar, use_container_width=True)
            with col_b:
                fig_pie = px.pie(df, names='dedutivel_ir', values='valor', title="Gastos Dedutíveis (IR)", color_discrete_sequence=['#00CC96', '#EF553B'])
                st.plotly_chart(fig_pie, use_container_width=True)

            st.subheader("📝 Extrato de Transações")
            st.dataframe(df[['created_at', 'estabelecimento', 'valor']].sort_values(by='created_at', ascending=False), use_container_width=True)
        else:
            st.warning("Nenhum dado encontrado para este número.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
else:
    st.write("👈 Introduza o seu número de WhatsApp na barra lateral para começar.")
