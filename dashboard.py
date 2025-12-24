import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="FinanBot Dashboard", layout="wide", page_icon="💰")

# Pegando os segredos de forma correta
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📊 FinanBot - Painel de Inteligência Financeira")
st.markdown("---")

# Barra Lateral para Identificação
with st.sidebar:
    st.header("👤 Área do Cliente")
    numero_telefone = st.text_input("Seu WhatsApp (com DDD):", placeholder="5592...")
    st.info("Digite apenas os números que você usa no bot.")

if numero_telefone:
    try:
        # Busca os dados reais no Supabase
        res = supabase.table("chat_financeiro").select("*").eq("telefone", numero_telefone).execute()
        
        if res.data:
            df = pd.DataFrame(res.data)
            df['created_at'] = pd.to_datetime(df['created_at'])
            
            # --- DASHBOARD DE MÉTRICAS ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Gasto", f"R$ {df['valor'].sum():.2f}")
            with col2:
                # Soma apenas o que a IA marcou como dedutível de IR
                gastos_ir = df[df['dedutivel_ir'] == True]['valor'].sum() if 'dedutivel_ir' in df.columns else 0
                st.metric("Potencial de Restituição IR", f"R$ {gastos_ir:.2f}")
            with col3:
                st.metric("Total de Lançamentos", len(df))

            st.markdown("---")

            # --- GRÁFICOS ---
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("📅 Gastos por Dia")
                fig_timeline = px.bar(df, x='created_at', y='valor', color='estabelecimento', 
                                    title="Histórico de Lançamentos", labels={'created_at': 'Data', 'valor': 'Valor (R$)'})
                st.plotly_chart(fig_timeline, use_container_width=True)

            with c2:
                st.subheader("🏥 Gastos Dedutíveis (IR)")
                if 'dedutivel_ir' in df.columns:
                    fig_ir = px.pie(df, names='dedutivel_ir', values='valor', 
                                   title="Composição de Gastos p/ IR",
                                   color_discrete_sequence=['#636EFA', '#EF553B'])
                    st.plotly_chart(fig_ir, use_container_width=True)
                else:
                    st.warning("Aguardando primeiros dados de IR...")

            # --- TABELA DETALHADA ---
            st.subheader("📝 Extrato Detalhado")
            st.dataframe(df[['created_at', 'estabelecimento', 'valor', 'tipo']].sort_values(by='created_at', ascending=False), use_container_width=True)

        else:
            st.warning("Ainda não temos registros para este número. Mande uma foto de nota fiscal no WhatsApp!")
            
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
else:
    st.write("👈 Digite seu número na barra lateral para ver seus gráficos.")
