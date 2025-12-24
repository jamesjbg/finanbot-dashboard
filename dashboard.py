# FORMA CORRETA: O código chama pelo NOME da chave, não pelo valor
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") # Ou st.secrets["SUPABASE_KEY"]
