import streamlit as st
import os, sys

# Permite importar controllers e páginas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.config import set_page_configuration, show_title
from controllers.sidebar import streamlit_menu, sidebar_content

from paginas.dashboard_principal import main as main_dashboard
from paginas.analise_vendas import main as main_vendas
from paginas.analise_regional import main as main_regional
from paginas.analise_modelos import main as main_modelos

# Configurações de página: apenas aqui, antes de qualquer st.*
set_page_configuration()
show_title()

# Menu lateral
selected_option = streamlit_menu()

# Roteamento das páginas
if selected_option == 'Dashboard Principal':
    main_dashboard()
elif selected_option == 'Análise de Vendas':
    main_vendas()
elif selected_option == 'Análise Regional':
    main_regional()
elif selected_option == 'Análise de Modelos':
    main_modelos()