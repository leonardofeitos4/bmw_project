import streamlit as st

def set_page_configuration():
    """Configurações da página Streamlit"""
    st.set_page_config(
        page_title="Dashboard Estratégico BMW",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def show_title():
    """Exibe o título principal da aplicação"""
    st.title("🚗 Dashboard Estratégico BMW")
    st.markdown("---")
    st.markdown("""
    **Análise de Evolução e Tendências Estratégicas**
    
    Este dashboard foi desenvolvido para apoiar decisões estratégicas baseadas em dados de vendas da BMW,
    com foco na análise de tendências, performance regional e insights sobre o portfólio de modelos.
    """)
    st.markdown("---")

