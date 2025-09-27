import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Adiciona o diretório pai ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_bmw_data
from utils.chart_utils import format_currency, format_number

def main():
    """Página de Análise Regional"""
    st.header("🌍 Análise Regional - Performance por Região")
    
    # 📦 Carrega os dados
    df = load_bmw_data()
    if df is None:
        st.error("❌ Não foi possível carregar os dados.")
        return
    
    # 🎚️ Filtros Laterais
    st.sidebar.subheader("🔍 Filtros de Visualização")
    
    # Filtro por ano
    anos = sorted(df['Year'].unique())
    anos_selecionados = st.sidebar.multiselect(
        "Selecione os anos:",
        anos,
        default=anos
    )
    
    # Filtro por região
    regioes = sorted(df['Region'].unique())
    regioes_selecionadas = st.sidebar.multiselect(
        "Selecione as regiões:",
        regioes,
        default=regioes
    )
    
    # Filtro por tipo de combustível
    combustiveis = sorted(df['Fuel_Category'].unique())
    combustiveis_selecionados = st.sidebar.multiselect(
        "Selecione o tipo de combustível:",
        combustiveis,
        default=combustiveis
    )
    
    # 🔎 Aplica filtros
    df_filtrado = df[
        (df['Year'].isin(anos_selecionados)) &
        (df['Region'].isin(regioes_selecionadas)) &
        (df['Fuel_Category'].isin(combustiveis_selecionados))
    ]
    
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        return
    
    # 📊 Performance por Região
    st.subheader("📊 Performance por Região")
    
    regional_data = df_filtrado.groupby('Region').agg({
        'Sales_Volume': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    regional_data['Preço Médio'] = regional_data['Revenue'] / regional_data['Sales_Volume']
    regional_data = regional_data.sort_values('Sales_Volume', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_volume = px.bar(
            regional_data,
            x='Region',
            y='Sales_Volume',
            title='📦 Volume de Vendas por Região',
            color='Sales_Volume',
            color_continuous_scale='Blues',
            text=regional_data['Sales_Volume'].apply(format_number)
        )
        fig_volume.update_traces(textposition='outside')
        fig_volume.update_layout(
            template='plotly_white',
            height=420,
            xaxis_title="Região",
            yaxis_title="Volume de Vendas"
        )
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        fig_revenue = px.bar(
            regional_data,
            x='Region',
            y='Revenue',
            title='💰 Receita por Região',
            color='Revenue',
            color_continuous_scale='Greens',
            text=regional_data['Revenue'].apply(format_currency)
        )
        fig_revenue.update_traces(textposition='outside')
        fig_revenue.update_layout(
            template='plotly_white',
            height=420,
            xaxis_title="Região",
            yaxis_title="Receita (US$)"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # 📈 Evolução Temporal por Região
    st.subheader("📈 Evolução Temporal das Vendas por Região")
    
    st.markdown("**Selecione as regiões que deseja comparar:**")
    regioes_temporais = sorted(df_filtrado['Region'].unique())
    
    regioes_temporais_sel = st.multiselect(
        "Regiões (padrão: África e Europa):",
        regioes_temporais,
        default=["Africa", "Europe"]
    )
    
    df_temporal = df_filtrado[df_filtrado['Region'].isin(regioes_temporais_sel)]
    
    if df_temporal.empty:
        st.warning("⚠️ Nenhuma região selecionada contém dados.")
    else:
        regional_yearly = df_temporal.groupby(['Year', 'Region']).agg({
            'Sales_Volume': 'sum'
        }).reset_index()
        
        fig_evolution = px.line(
            regional_yearly,
            x='Year',
            y='Sales_Volume',
            color='Region',
            title='📈 Evolução das Vendas por Região ao Longo do Tempo',
            markers=True,
            text=regional_yearly['Sales_Volume'].apply(format_number)
        )
        fig_evolution.update_traces(mode='lines+markers+text', textposition='top center')
        fig_evolution.update_layout(
            template='plotly_white',
            height=500,
            xaxis_title="Ano",
            yaxis_title="Volume de Vendas"
        )
        st.plotly_chart(fig_evolution, use_container_width=True)
    
    # 🥧 Participação de Mercado
    st.subheader("🥧 Participação de Mercado por Região")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie_volume = px.pie(
            regional_data,
            values='Sales_Volume',
            names='Region',
            title='Participação no Volume Total',
            hole=0.4
        )
        fig_pie_volume.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie_volume, use_container_width=True)
    
    with col2:
        fig_pie_revenue = px.pie(
            regional_data,
            values='Revenue',
            names='Region',
            title='Participação na Receita Total',
            hole=0.4
        )
        fig_pie_revenue.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie_revenue, use_container_width=True)
    
    # 💰 Preço Médio
    st.subheader("💰 Preço Médio por Região")
    
    fig_price = px.bar(
        regional_data.sort_values('Preço Médio', ascending=False),
        x='Region',
        y='Preço Médio',
        title='💎 Preço Médio por Região',
        color='Preço Médio',
        color_continuous_scale='Oranges',
        text=regional_data.sort_values('Preço Médio', ascending=False)['Preço Médio'].apply(format_currency)
    )
    fig_price.update_traces(textposition='outside')
    fig_price.update_layout(template='plotly_white', height=420, xaxis_title="Região", yaxis_title="Preço Médio (US$)")
    st.plotly_chart(fig_price, use_container_width=True)
    
    # ⚡ Combustível por Região
    st.subheader("⚡ Análise por Tipo de Combustível e Região")
    
    fuel_regional = df_filtrado.groupby(['Region', 'Fuel_Category']).agg({
        'Sales_Volume': 'sum'
    }).reset_index()
    
    fig_fuel_region = px.bar(
        fuel_regional,
        x='Region',
        y='Sales_Volume',
        color='Fuel_Category',
        title='Volume de Vendas por Região e Tipo de Combustível',
        barmode='group',
        text=fuel_regional['Sales_Volume'].apply(format_number)
    )
    fig_fuel_region.update_traces(textposition='outside')
    fig_fuel_region.update_layout(template='plotly_white', height=420, xaxis_title="Região", yaxis_title="Volume de Vendas")
    st.plotly_chart(fig_fuel_region, use_container_width=True)
    
    # 🏆 Ranking de Regiões
    st.subheader("🏆 Ranking de Regiões")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**🥇 Top Volume de Vendas**")
        top_volume = regional_data.nlargest(3, 'Sales_Volume')[['Region', 'Sales_Volume']]
        for _, row in top_volume.iterrows():
            st.write(f"• {row['Region']}: {format_number(row['Sales_Volume'])}")
    
    with col2:
        st.write("**💰 Top Receita**")
        top_revenue = regional_data.nlargest(3, 'Revenue')[['Region', 'Revenue']]
        for _, row in top_revenue.iterrows():
            st.write(f"• {row['Region']}: {format_currency(row['Revenue'])}")
    
    with col3:
        st.write("**💎 Top Preço Médio**")
        top_price = regional_data.nlargest(3, 'Preço Médio')[['Region', 'Preço Médio']]
        for _, row in top_price.iterrows():
            st.write(f"• {row['Region']}: {format_currency(row['Preço Médio'])}")
    
    # 🎯 Insights Regionais
    st.subheader("🎯 Insights Regionais")
    
    regiao_top = regional_data.iloc[0]['Region']
    volume_top = regional_data.iloc[0]['Sales_Volume']
    regiao_premium = regional_data.loc[regional_data['Preço Médio'].idxmax(), 'Region']
    preco_premium = regional_data['Preço Médio'].max()
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"""
        **🏆 Região Líder: {regiao_top}**
        
        A região **{regiao_top}** lidera em volume com **{format_number(volume_top)}** unidades vendidas.
        """)
        st.info("""
        **📈 Oportunidades de Crescimento**
        
        Regiões com menor participação podem representar novos mercados estratégicos.
        """)
    with col2:
        st.warning(f"""
        **💎 Mercado Premium: {regiao_premium}**
        
        A região **{regiao_premium}** apresenta o maior preço médio (**{format_currency(preco_premium)}**).
        """)
        st.info("""
        **⚡ Adoção de Eletrificação**
        
        A penetração de veículos eletrificados varia conforme o perfil regional.
        """)
    
    # 📋 Dados Detalhados
    st.subheader("📋 Dados Detalhados por Região")
    
    tabela = regional_data.copy()
    tabela['Sales_Volume'] = tabela['Sales_Volume'].apply(format_number)
    tabela['Revenue'] = tabela['Revenue'].apply(format_currency)
    tabela['Preço Médio'] = tabela['Preço Médio'].apply(format_currency)
    
    total_vendas = df_filtrado['Sales_Volume'].sum()
    total_receita = df_filtrado['Revenue'].sum()
    tabela['% Volume'] = (regional_data['Sales_Volume'] / total_vendas * 100).apply(lambda x: f"{x:.1f}%")
    tabela['% Receita'] = (regional_data['Revenue'] / total_receita * 100).apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(tabela, use_container_width=True)
