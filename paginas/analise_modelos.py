import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Adiciona o diretório pai ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_bmw_data
from utils.chart_utils import format_currency, format_number, format_large_number

def main():
    """Página de análise de modelos"""
    st.header("🏎️ Análise de Modelos - Performance do Portfólio")
    
    # Carrega os dados
    df = load_bmw_data()
    if df is None:
        st.error("Não foi possível carregar os dados.")
        return
    
    # -----------------------
    # 🔍 Filtros
    # -----------------------
    st.sidebar.subheader("🔍 Filtros")
    
    years = sorted(df['Year'].unique())
    selected_years = st.sidebar.multiselect(
        "Selecione os anos:",
        years,
        default=years
    )
    
    regions = sorted(df['Region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Selecione as regiões:",
        regions,
        default=regions
    )
    
    filtered_df = df[
        (df['Year'].isin(selected_years)) &
        (df['Region'].isin(selected_regions))
    ]
    
    if filtered_df.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
        return
    
    # -----------------------
    # 📊 Agregação
    # -----------------------
    model_data = filtered_df.groupby('Model').agg({
        'Sales_Volume': 'sum',
        'Revenue': 'sum',
        'Price_USD': 'mean'
    }).reset_index()
    
    model_data['Average_Price'] = model_data['Revenue'] / model_data['Sales_Volume']
    model_data = model_data.sort_values('Sales_Volume', ascending=False)
    
    total_volume = filtered_df['Sales_Volume'].sum()
    total_revenue = filtered_df['Revenue'].sum()
    avg_price = filtered_df['Revenue'].sum() / filtered_df['Sales_Volume'].sum()
    
    # -----------------------
    # 📈 Indicadores gerais
    # -----------------------
    st.markdown("### 📈 Indicadores Gerais do Portfólio")
    col1, col2, col3 = st.columns(3)
    col1.metric("🚗 Volume Total de Vendas", format_large_number(total_volume))
    col2.metric("💰 Receita Total", format_large_number(total_revenue))
    col3.metric("🏷️ Preço Médio", format_large_number(avg_price))
    
    # -----------------------
    # 📊 Top 10 Modelos - Volume e Receita
    # -----------------------
    st.subheader("📊 Performance por Modelo")
    col1, col2 = st.columns(2)
    
    model_data['Volume_Share'] = (model_data['Sales_Volume'] / total_volume * 100)
    model_data['Revenue_Share'] = (model_data['Revenue'] / total_revenue * 100)
    
    with col1:
        fig_volume = px.bar(
            model_data.head(10),
            x='Sales_Volume',
            y='Model',
            orientation='h',
            title='Top 10 Modelos - Volume de Vendas',
            color='Sales_Volume',
            color_continuous_scale='Blues',
            text=model_data.head(10).apply(
                lambda x: f"{format_large_number(x['Sales_Volume'])} ({x['Volume_Share']:.1f}%)", axis=1
            )
        )
        fig_volume.update_traces(textposition='outside')
        fig_volume.update_layout(template='plotly_white', height=500)
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        fig_revenue = px.bar(
            model_data.head(10),
            x='Revenue',
            y='Model',
            orientation='h',
            title='Top 10 Modelos - Receita',
            color='Revenue',
            color_continuous_scale='Greens',
            text=model_data.head(10).apply(
                lambda x: f"{format_large_number(x['Revenue'])} ({x['Revenue_Share']:.1f}%)", axis=1
            )
        )
        fig_revenue.update_traces(textposition='outside')
        fig_revenue.update_layout(template='plotly_white', height=500)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # -----------------------
    # 💰 Preço Médio por Modelo
    # -----------------------
    st.subheader("💰 Preço Médio por Modelo")
    
    model_price_sorted = model_data.sort_values('Average_Price', ascending=False)
    
    fig_price = px.bar(
        model_price_sorted.head(10),
        x='Average_Price',
        y='Model',
        orientation='h',
        title='Top 10 Modelos - Preço Médio',
        color='Average_Price',
        color_continuous_scale='Oranges',
        text=model_price_sorted.head(10)['Average_Price'].apply(format_large_number)
    )
    fig_price.update_traces(textposition='outside')
    fig_price.update_layout(template='plotly_white', height=500)
    st.plotly_chart(fig_price, use_container_width=True)
    
    # -----------------------
    # 📈 Matriz de Performance
    # -----------------------
    st.subheader("📈 Matriz de Performance: Volume vs Preço")
    
    fig_scatter = px.scatter(
        model_data,
        x='Sales_Volume',
        y='Average_Price',
        size='Revenue',
        color='Model',
        hover_name='Model',
        title='Matriz de Performance: Volume de Vendas vs Preço Médio',
        labels={
            'Sales_Volume': 'Volume de Vendas',
            'Average_Price': 'Preço Médio (USD)',
            'Revenue': 'Receita'
        }
    )
    fig_scatter.update_layout(
        template='plotly_white',
        height=500,
        legend_title_text="Modelo"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # -----------------------
    # 📈 Evolução dos Modelos Selecionados
    # -----------------------
    st.subheader("📈 Evolução dos Modelos Selecionados")
    
    all_models = model_data['Model'].unique().tolist()
    selected_models = st.multiselect(
        "Selecione os modelos para comparar:",
        all_models,
        default=["7 Series", "i8"]
    )
    
    top_models_yearly = filtered_df[filtered_df['Model'].isin(selected_models)].groupby(['Year', 'Model']).agg({
        'Sales_Volume': 'sum'
    }).reset_index()
    
    fig_evolution = px.line(
        top_models_yearly,
        x='Year',
        y='Sales_Volume',
        color='Model',
        title='Evolução dos Modelos Selecionados ao Longo do Tempo',
        markers=True
    )
    fig_evolution.update_traces(mode='lines+markers', text=None)
    fig_evolution.update_layout(template='plotly_white', height=500)
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # -----------------------
    # ⚡ Análise de Combustível por Modelo
    # -----------------------
    st.subheader("⚡ Análise de Combustível por Modelo (Top 10)")
    
    top_10_models = model_data.head(10)['Model'].tolist()
    fuel_model = filtered_df[filtered_df['Model'].isin(top_10_models)].groupby(['Model', 'Fuel_Category']).agg({
        'Sales_Volume': 'sum'
    }).reset_index()
    
    fig_fuel_model = px.bar(
        fuel_model,
        x='Model',
        y='Sales_Volume',
        color='Fuel_Category',
        text=fuel_model['Sales_Volume'].apply(format_large_number),
        title='Volume de Vendas por Modelo e Tipo de Combustível',
        barmode='stack'
    )
    fig_fuel_model.update_traces(textposition='inside')
    fig_fuel_model.update_layout(template='plotly_white', height=500)
    fig_fuel_model.update_xaxes(tickangle=45)
    st.plotly_chart(fig_fuel_model, use_container_width=True)
    
    # -----------------------
    # 📋 Tabela Detalhada
    # -----------------------
    st.subheader("📋 Dados Detalhados por Modelo")
    
    display_data = model_data.copy()
    display_data['Sales_Volume'] = display_data['Sales_Volume'].apply(format_number)
    display_data['Revenue'] = display_data['Revenue'].apply(format_currency)
    display_data['Average_Price'] = display_data['Average_Price'].apply(format_currency)
    display_data['Volume_Share'] = display_data['Volume_Share'].apply(lambda x: f"{x:.1f}%")
    display_data['Revenue_Share'] = display_data['Revenue_Share'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_data, use_container_width=True)
