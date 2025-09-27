import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_bmw_data():
    """Carrega e processa os dados da BMW"""
    try:
        # Caminho para o arquivo de dados
        data_path = os.path.join(os.path.dirname(__file__), '..', 'dados', 'base_bmww.csv')
        
        # Carrega os dados
        df = pd.read_csv(data_path, sep=';')
        
        # Processamento básico dos dados
        df['Revenue'] = df['Price_USD'] * df['Sales_Volume']
        df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year
        
        # Categorização de combustível
        df['Fuel_Category'] = df['Fuel_Type'].apply(lambda x: 'Eletrificado' if x == 'Hybrid' else 'Combustão')
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None

def get_data_summary(df):
    """Retorna um resumo dos dados"""
    if df is None:
        return None
        
    summary = {
        'total_records': len(df),
        'years_range': f"{df['Year'].min()} - {df['Year'].max()}",
        'regions': df['Region'].nunique(),
        'models': df['Model'].nunique(),
        'total_revenue': df['Revenue'].sum(),
        'total_sales_volume': df['Sales_Volume'].sum()
    }
    
    return summary

