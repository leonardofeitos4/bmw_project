import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_bmw_data, get_data_summary
from utils.chart_utils import format_currency, format_number

def main():
    st.header("📊 Dashboard Principal - Visão Geral")

    # Carrega os dados
    df = load_bmw_data()
    if df is None:
        st.error("❌ Não foi possível carregar os dados.")
        return

    # 🎛️ FILTROS GLOBAIS
    st.sidebar.header("🎚️ Filtros Globais")

    anos = sorted(df["Year"].unique())
    regioes = sorted(df["Region"].unique())
    combustiveis = sorted(df["Fuel_Category"].unique())

    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        ano_sel = st.multiselect("Ano", anos, default=anos)
    with col2:
        reg_sel = st.multiselect("Região", regioes, default=regioes)
    with col3:
        comb_sel = st.multiselect("Combustível", combustiveis, default=combustiveis)

    df_filtered = df[
        (df["Year"].isin(ano_sel)) &
        (df["Region"].isin(reg_sel)) &
        (df["Fuel_Category"].isin(comb_sel))
    ]

    # KPIs principais
    summary = get_data_summary(df_filtered)
    st.markdown("### 📌 Indicadores-Chave")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Receita Total", format_currency(summary["total_revenue"]))
    with col2:
        st.metric("🚗 Volume de Vendas", format_number(summary["total_sales_volume"]))
    with col3:
        st.metric("🌍 Regiões Atendidas", summary["regions"])
    with col4:
        st.metric("🏎️ Modelos no Portfólio", summary["models"])

    st.markdown("---")

    # ======================
    # GRÁFICOS DE EVOLUÇÃO
    # ======================
    st.subheader("📅 Evolução Temporal")

    yearly_data = (
        df_filtered.groupby("Year")
        .agg({"Sales_Volume": "sum", "Revenue": "sum"})
        .reset_index()
    )

    # 📊 Evolução das Vendas com linha + rótulos
    fig_sales = px.line(
        yearly_data,
        x="Year",
        y="Sales_Volume",
        title="📈 Evolução do Volume de Vendas (com linha de tendência)",
        markers=True,
        color_discrete_sequence=["#007bff"]
    )
    fig_sales.update_traces(
        text=yearly_data["Sales_Volume"].apply(lambda x: format_number(x)),
        textposition="top center",
        mode="lines+markers+text",  # 👈 garante exibição dos rótulos
        line=dict(width=3)
    )
    fig_sales.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_sales, use_container_width=True)

    # 💰 Receita com linha + rótulos formatados
    fig_rev = px.line(
        yearly_data,
        x="Year",
        y="Revenue",
        title="💰 Receita Total ao Longo do Tempo",
        markers=True,
        color_discrete_sequence=["#00cc96"]
    )
    fig_rev.update_traces(
        text=yearly_data["Revenue"].apply(lambda x: format_currency(x)),
        textposition="top center",
        mode="lines+markers+text",
        line=dict(width=3)
    )
    fig_rev.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("---")

    # ======================
    # ANÁLISE POR COMBUSTÍVEL
    # ======================
    st.subheader("⚡ Evolução por Tipo de Combustível")

    fuel_data = (
        df_filtered.groupby(["Year", "Fuel_Category"])
        .agg({"Sales_Volume": "sum"})
        .reset_index()
    )

    fig_fuel = px.line(
        fuel_data,
        x="Year",
        y="Sales_Volume",
        color="Fuel_Category",
        title="📉 Participação de Mercado: Eletrificados vs Combustão",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_fuel.update_traces(
        mode="lines+markers+text",
        text=fuel_data["Sales_Volume"].apply(lambda x: format_number(x)),
        textposition="top center",
        line=dict(width=2)
    )
    fig_fuel.update_layout(template="plotly_white", height=420, legend_title_text="Combustível")
    st.plotly_chart(fig_fuel, use_container_width=True)

    st.markdown("---")

    # ======================
    # INSIGHTS NARRATIVOS
    # ======================
    st.subheader("🎯 Insights Narrativos")

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **📈 Crescimento Consistente:**  
        As vendas vêm crescendo de forma sólida, com destaque nos anos mais recentes.
        """)
        st.success("""
        **🌍 Expansão Global:**  
        A BMW mantém presença robusta em diversas regiões com portfólio diversificado.
        """)
    with col2:
        st.warning("""
        **⚡ Transição Energética:**  
        Crescimento expressivo dos veículos eletrificados nos últimos anos.
        """)
        st.info("""
        **🎯 Oportunidades:**  
        Avaliar regiões e modelos com maior potencial de eletrificação.
        """)

    # ======================
    # DADOS RECENTES
    # ======================
    st.markdown("---")
    st.subheader("📋 Amostra de Dados Recentes")

    recent_year = df_filtered["Year"].max()
    st.caption(f"🔎 Exibindo registros de {recent_year}")

    recent_data = df_filtered[df_filtered["Year"] == recent_year].head(10)
    st.dataframe(
        recent_data[["Model", "Year", "Region", "Fuel_Type", "Price_USD", "Sales_Volume", "Revenue"]],
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()
