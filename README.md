# 🚗 Dashboard Estratégico BMW

Este repositório apresenta um aplicativo interativo desenvolvido com **Streamlit**, voltado para análise estratégica de dados de vendas da BMW. O dashboard foi projetado para apoiar decisões estratégicas baseadas em dados, com foco na análise de tendências, performance regional e insights sobre o portfólio de modelos.

## 🧭 Funcionalidades Principais

- **Dashboard Principal**: Visão geral dos KPIs e métricas principais
- **Análise de Vendas**: Evolução temporal das vendas com linhas de tendência
- **Análise Regional**: Performance comparativa por região geográfica
- **Análise de Modelos**: Desempenho detalhado do portfólio de modelos

## 📊 Características do Dashboard

- Visualizações interativas com Plotly
- Filtros dinâmicos por ano e região
- Análise de tendências com linhas de regressão
- Comparativo entre veículos eletrificados e combustão
- Métricas de performance e crescimento
- Insights estratégicos automatizados

## 🧠 Metodologia

- **Design Thinking**: Foco na persona do usuário (Gerente de Vendas)
- **Storytelling com Dados**: Transformação de dados em narrativas claras
- **Análise Temporal**: Evolução de KPIs ao longo do tempo
- **Análise Comparativa**: Performance entre regiões e modelos

## 📊 Dados Utilizados

O dashboard utiliza dados de vendas da BMW com as seguintes informações:

- `Model`: Modelo do veículo
- `Year`: Ano de fabricação/venda
- `Region`: Região de venda
- `Color`: Cor do veículo
- `Fuel_Type`: Tipo de combustível
- `Transmission`: Tipo de transmissão
- `Engine_Size_L`: Tamanho do motor (litros)
- `Mileage_KM`: Quilometragem
- `Price_USD`: Preço em dólares
- `Sales_Volume`: Volume de vendas
- `Sales_Classification`: Classificação de vendas

## 📦 Instalação e Execução

### 🔧 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 🚀 Passos para instalação:

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd bmw_dashboard
   ```

2. **(Opcional) Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o aplicativo:**
   ```bash
   streamlit run app.py
   ```

5. **Acesse o dashboard:**
   - O aplicativo será aberto automaticamente no navegador
   - Ou acesse manualmente: `http://localhost:8501`

## 📁 Estrutura do Projeto

```
bmw_dashboard/
├── app.py                      # Arquivo principal da aplicação
├── requirements.txt            # Dependências do projeto
├── README.md                  # Documentação
├── controllers/               # Controladores da aplicação
│   ├── config.py             # Configurações da página
│   └── sidebar.py            # Menu lateral
├── dados/                     # Dados do projeto
│   └── base_bmww.csv         # Dataset BMW
├── paginas/                   # Páginas do dashboard
│   ├── dashboard_principal.py # Dashboard principal
│   ├── analise_vendas.py     # Análise de vendas
│   ├── analise_regional.py   # Análise regional
│   └── analise_modelos.py    # Análise de modelos
└── utils/                     # Utilitários
    ├── data_loader.py        # Carregamento de dados
    └── chart_utils.py        # Utilitários para gráficos
```

## 🎯 Insights Estratégicos

O dashboard fornece insights estratégicos incluindo:

- **Crescimento Sólido**: Análise de tendências de crescimento
- **Performance Regional**: Identificação de mercados líderes e oportunidades
- **Portfólio de Modelos**: Análise de pilares do negócio e oportunidades
- **Tendência Eletrificação**: Evolução dos veículos eletrificados vs combustão

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para aplicações web
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas
- **NumPy**: Computação numérica
- **Matplotlib/Seaborn**: Visualizações complementares

## 📈 Próximos Passos

- Integração com APIs de dados em tempo real
- Modelos preditivos para forecasting
- Análises mais granulares por segmento
- Dashboard mobile-friendly
- Exportação de relatórios em PDF

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido para análise estratégica BMW** 🚗📊

