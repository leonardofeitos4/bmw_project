import streamlit as st

def streamlit_menu():
    """Menu lateral do Streamlit"""
    with st.sidebar:
        st.header("🚗 BMW Dashboard")
        st.markdown("---")
        
        # Menu de navegação
        selected_option = st.selectbox(
            "Selecione uma análise:",
            [
                "Dashboard Principal",
                "Análise de Vendas", 
                "Análise Regional",
                "Análise de Modelos"
            ]
        )
        
        st.markdown("---")
        
        # Informações adicionais
        st.markdown("""
        ### 📊 Sobre o Dashboard
        
        Este dashboard apresenta análises estratégicas baseadas em dados de vendas da BMW, incluindo:
        
        - **Dashboard Principal**: Visão geral dos KPIs
        - **Análise de Vendas**: Evolução temporal das vendas
        - **Análise Regional**: Performance por região
        - **Análise de Modelos**: Desempenho por modelo
        """)
        
        st.markdown("---")
        st.markdown("**Desenvolvido para análise estratégica BMW**")
        
    return selected_option

def sidebar_content():
    """Conteúdo adicional da sidebar (se necessário)"""
    pass

