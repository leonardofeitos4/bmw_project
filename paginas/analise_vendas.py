import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sys
import os

# Adiciona o diretório pai ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_bmw_data
from utils.chart_utils import format_currency, format_number

def main():
    """Página de Análise de Vendas"""
    st.header("📈 Análise de Vendas - Evolução Temporal")
    
    # Carrega os dados
    df = load_bmw_data()
    if df is None:
        st.error("❌ Não foi possível carregar os dados.")
        return
    
    # 🎚️ Filtros laterais
    st.sidebar.subheader("🔍 Filtros de Visualização")
    
    anos = sorted(df['Year'].unique())
    regioes = sorted(df['Region'].unique())

    anos_selecionados = st.sidebar.multiselect("Selecione os anos:", anos, default=anos)
    regioes_selecionadas = st.sidebar.multiselect("Selecione as regiões:", regioes, default=regioes)
    
    # 🔎 Aplica filtros
    df_filtrado = df[
        (df['Year'].isin(anos_selecionados)) & 
        (df['Region'].isin(regioes_selecionadas))
    ]
    
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        return
    
    # 📊 Evolução Temporal
    st.subheader("📊 Evolução Temporal das Vendas e Receita")
    
    dados_anuais = df_filtrado.groupby('Year').agg({
        'Sales_Volume': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    dados_anuais.rename(columns={'Year': 'Ano', 'Sales_Volume': 'Vendas', 'Revenue': 'Receita'}, inplace=True)
    dados_anuais['Preço Médio'] = dados_anuais['Receita'] / dados_anuais['Vendas']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 📦 Evolução das Vendas
        fig_vendas = px.line(
            dados_anuais,
            x='Ano',
            y='Vendas',
            title='📦 Evolução do Volume de Vendas',
            markers=True,
            text=dados_anuais['Vendas'].apply(format_number),
            color_discrete_sequence=['#1f77b4']
        )
        fig_vendas.update_traces(
            textposition='top center',
            mode='lines+markers+text',
            line=dict(width=3)
        )
        fig_vendas.update_layout(template='plotly_white', height=420)
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    with col2:
        # 💰 Evolução da Receita
        fig_receita = px.line(
            dados_anuais,
            x='Ano',
            y='Receita',
            title='💰 Evolução da Receita Total',
            markers=True,
            text=dados_anuais['Receita'].apply(format_currency),
            color_discrete_sequence=['#00cc96']
        )
        fig_receita.update_traces(
            textposition='top center',
            mode='lines+markers+text',
            line=dict(width=3)
        )
        fig_receita.update_layout(template='plotly_white', height=420)
        st.plotly_chart(fig_receita, use_container_width=True)
    
    # 💵 Preço médio
    st.subheader("💵 Evolução do Preço Médio")
    
    fig_preco = px.line(
        dados_anuais,
        x='Ano',
        y='Preço Médio',
        title='💵 Evolução do Preço Médio dos Veículos',
        markers=True,
        text=dados_anuais['Preço Médio'].apply(format_currency),
        color_discrete_sequence=['#ffa500']
    )
    fig_preco.update_traces(
        textposition='top center',
        mode='lines+markers+text',
        line=dict(width=3)
    )
    fig_preco.update_layout(template='plotly_white', height=420)
    st.plotly_chart(fig_preco, use_container_width=True)
    
    # ⚡ Crescimento por Tipo de Combustível
    st.subheader("⚡ Crescimento por Tipo de Combustível")
    
    combustivel_ano = df_filtrado.groupby(['Year', 'Fuel_Category']).agg({
        'Sales_Volume': 'sum'
    }).reset_index()
    combustivel_ano.rename(columns={'Year': 'Ano', 'Fuel_Category': 'Categoria de Combustível', 'Sales_Volume': 'Vendas'}, inplace=True)
    
    fig_combustivel = px.line(
        combustivel_ano,
        x='Ano',
        y='Vendas',
        color='Categoria de Combustível',
        title='⚡ Vendas: Eletrificados vs Combustão',
        markers=True,
        text=combustivel_ano['Vendas'].apply(format_number),
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_combustivel.update_traces(
        textposition='top center',
        mode='lines+markers+text',
        line=dict(width=2)
    )
    fig_combustivel.update_layout(template='plotly_white', height=420)
    st.plotly_chart(fig_combustivel, use_container_width=True)
    
    # 📈 Análise de Crescimento
    st.subheader("📈 Taxas de Crescimento Anual")
    
    if len(dados_anuais) > 1:
        dados_anuais['Crescimento Vendas (%)'] = dados_anuais['Vendas'].pct_change() * 100
        dados_anuais['Crescimento Receita (%)'] = dados_anuais['Receita'].pct_change() * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_crescimento_vendas = px.bar(
                dados_anuais[1:],  # ignora o primeiro ano
                x='Ano',
                y='Crescimento Vendas (%)',
                title='📈 Crescimento Anual - Volume de Vendas (%)',
                color='Crescimento Vendas (%)',
                color_continuous_scale='RdYlGn',
                text=dados_anuais[1:]['Crescimento Vendas (%)'].apply(lambda x: f"{x:.1f}%")
            )
            fig_crescimento_vendas.update_traces(textposition='outside')
            fig_crescimento_vendas.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_crescimento_vendas, use_container_width=True)
        
        with col2:
            fig_crescimento_receita = px.bar(
                dados_anuais[1:],
                x='Ano',
                y='Crescimento Receita (%)',
                title='💹 Crescimento Anual - Receita (%)',
                color='Crescimento Receita (%)',
                color_continuous_scale='RdYlGn',
                text=dados_anuais[1:]['Crescimento Receita (%)'].apply(lambda x: f"{x:.1f}%")
            )
            fig_crescimento_receita.update_traces(textposition='outside')
            fig_crescimento_receita.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_crescimento_receita, use_container_width=True)
    
    # 🎯 Métricas Resumo
    st.subheader("🎯 Métricas de Desempenho")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vendas = df_filtrado['Sales_Volume'].sum()
        st.metric("📦 Vendas Totais", format_number(total_vendas))
    
    with col2:
        total_receita = df_filtrado['Revenue'].sum()
        st.metric("💰 Receita Total", format_currency(total_receita))
    
    with col3:
        preco_medio = total_receita / total_vendas
        st.metric("💵 Preço Médio", format_currency(preco_medio))
    
    with col4:
        if len(dados_anuais) > 1:
            crescimento_total = (dados_anuais['Vendas'].iloc[-1] / dados_anuais['Vendas'].iloc[0] - 1) * 100
            st.metric("📈 Crescimento Total", f"{crescimento_total:.1f}%")
        else:
            st.metric("📈 Crescimento Total", "N/A")
    
    # 📋 Dados Detalhados
    st.subheader("📋 Dados Detalhados por Ano")
    
    tabela = dados_anuais.copy()
    tabela['Vendas'] = tabela['Vendas'].apply(format_number)
    tabela['Receita'] = tabela['Receita'].apply(format_currency)
    tabela['Preço Médio'] = tabela['Preço Médio'].apply(format_currency)
    
    if 'Crescimento Vendas (%)' in tabela.columns:
        tabela['Crescimento Vendas (%)'] = tabela['Crescimento Vendas (%)'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
        tabela['Crescimento Receita (%)'] = tabela['Crescimento Receita (%)'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    
    st.dataframe(tabela, use_container_width=True)

if __name__ == "__main__":
    main()
