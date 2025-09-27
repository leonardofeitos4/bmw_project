import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ================================
# 🎨 Configuração de estilo global
# ================================
plt.style.use('default')
sns.set_palette("husl")

# ================================
# 💲 Formatações numéricas
# ================================
def format_currency(value):
    """Formata valores monetários com sufixos (K, M, B, T)"""
    if pd.isna(value):
        return "-"
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"${value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"${value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"${value / 1e3:.2f}K"
    else:
        return f"${value:.2f}"

def format_number(value):
    """Formata números inteiros grandes com sufixos (K, M, B)"""
    if pd.isna(value):
        return "-"
    if value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"{value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.2f}K"
    else:
        return f"{value:.0f}"

def format_large_number(num):
    """Formata números grandes com sufixos (K, M, B, T) para exibição em indicadores"""
    if pd.isna(num):
        return "-"
    if num >= 1_000_000_000_000:
        return f"{num / 1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return str(int(num))

# ================================
# 📈 Criação de Gráficos
# ================================
def create_trend_line_chart(df, x_col, y_col, title, color='blue'):
    """
    Cria gráfico de linha com tendência linear (regressão simples)
    """
    fig = go.Figure()
    
    # Linha principal
    fig.add_trace(go.Scatter(
        x=df[x_col], 
        y=df[y_col],
        mode='lines+markers',
        name=y_col,
        line=dict(color=color, width=3),
        marker=dict(size=8)
    ))
    
    # Linha de tendência
    if len(df[x_col]) > 1:
        z = np.polyfit(df[x_col], df[y_col], 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=p(df[x_col]),
            mode='lines',
            name='Tendência',
            line=dict(color='red', width=2, dash='dash')
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        template='plotly_white',
        height=400
    )
    
    return fig

def create_bar_chart(df, x_col, y_col, title, color='blue'):
    """
    Cria gráfico de barras básico
    """
    fig = px.bar(df, x=x_col, y=y_col, title=title, color_discrete_sequence=[color])
    fig.update_layout(template='plotly_white', height=400)
    return fig

def create_comparison_chart(df, x_col, y_col, category_col, title):
    """
    Cria gráfico de linha para comparação entre categorias (ex: evolução por região)
    """
    fig = px.line(df, x=x_col, y=y_col, color=category_col, title=title, markers=True)
    fig.update_layout(template='plotly_white', height=400)
    return fig
