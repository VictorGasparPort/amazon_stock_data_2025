# Importações necessárias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime

# Configuração da página
st.set_page_config(
    page_title="📈 Análise de Ações Amazon",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Função de carregamento de dados com cache
@st.cache_data
def load_data(file_path):
    """
    Carrega os dados do arquivo CSV e realiza validações básicas.
    """
    try:
        path = Path(__file__).parent / file_path
        df = pd.read_csv(path, parse_dates=['date'])
        
        # Verifica se as colunas essenciais estão presentes
        if not all(col in df.columns for col in ['date', 'close']):
            raise ValueError("Colunas essenciais faltando no arquivo CSV.")
        
        return df.sort_values('date')
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.stop()

# Função de plotagem interativa
def plotar_evolucao_acoes(df, periodo='total'):
    """
    Plota a evolução das ações com opção de filtro por período.
    """
    plt.style.use('ggplot')  # Estilo mais claro e válido
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Mapeamento de períodos
    period_map = {
        'semanal': 7, 'mensal': 30, 'trimestral': 90,
        'semestral': 180, 'anual': 365, '10anos': 3650, 'total': None
    }
    
    # Define o intervalo de datas
    data_final = df['date'].max()
    data_inicial = df['date'].min() if periodo == 'total' else data_final - datetime.timedelta(days=period_map[periodo])
    
    # Filtra os dados
    df_filtrado = df[df['date'].between(data_inicial, data_final)]
    
    # Cria o gráfico
    ax.plot(df_filtrado['date'], df_filtrado['close'], color='#007BFF', linewidth=2)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Preço (USD)', fontsize=12)
    ax.set_title(f'Evolução das Ações - {periodo.capitalize()}', fontsize=16)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

# Função para gerar insights
def generate_insights(df, periodo):
    """
    Gera insights financeiros e estatísticos com base nos dados filtrados.
    """
    if df.empty:
        return "⚠️ Dados insuficientes para análise."
    
    latest = df.iloc[-1]
    initial = df.iloc[0]
    variation = ((latest['close'] - initial['close']) / initial['close']) * 100
    
    return f"""
    ### 📅 Período Analisado: {periodo.capitalize()}
    **📌 Data Inicial:** {initial['date'].strftime('%d/%m/%Y')}  
    **🏁 Data Final:** {latest['date'].strftime('%d/%m/%Y')}  
    
    ### 💰 Métricas Financeiras
    **📈 Preço Atual:** USD {latest['close']:.2f}  
    **📉 Variação Total:** {variation:+.2f}%  
    **📊 Volatilidade:** USD {df['close'].std():.2f}  
    
    ### 📊 Estatísticas Temporais
    **🗓️ Dias de Trading:** {len(df):,}  
    **📅 Duração Total:** {(latest['date'] - initial['date']).days} dias"""

# Função principal
def main():
    """
    Função principal para renderizar o dashboard.
    """
    # Carrega os dados
    df = load_data('../data/processed/AMZN_1997-05-15_2025-02-21_atualizado.csv')
    
    # Cabeçalho estilizado
    st.markdown("""
        <div style='border-bottom: 2px solid #007BFF; margin-bottom: 30px;'>
            <h1 style='color: black;'>📈 Dashboard Analítico - Amazon</h1>
            <p style='color: #555;'>Análise histórica de 1997 a 2025</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Seleção de período
    st.markdown("### 🔍 Selecione o Período de Análise")
    periodo = st.selectbox(
        label="Período",
        options=['total', '10anos', 'anual', 'semestral', 'trimestral', 'mensal', 'semanal'],
        index=0,
        label_visibility='collapsed'
    )
    
    # Gráfico principal
    fig = plotar_evolucao_acoes(df, periodo)
    st.pyplot(fig)
    
    # Divisor visual
    st.markdown("---")
    
    # Insights principais
    st.markdown("## 📌 Insights Principais")
    df_filtrado = df[df['date'].between(
        df['date'].max() - datetime.timedelta(days=365) if periodo != 'total' else df['date'].min(),
        df['date'].max()
    )]
    insights = generate_insights(df_filtrado, periodo)
    st.markdown(f"""
        <div style='
            background: #f9f9f9;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: black;
        '>
            {insights}
        </div>
    """, unsafe_allow_html=True)
    
    # Performance histórica
    st.markdown("## 🚀 Performance Histórica")
    if not df_filtrado.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Máximo do Período", 
                value=f"USD {df_filtrado['close'].max():.2f}",
                help="Valor máximo alcançado no período selecionado"
            )
        with col2:
            st.metric(
                label="Mínimo do Período", 
                value=f"USD {df_filtrado['close'].min():.2f}",
                help="Valor mínimo registrado no período analisado"
            )
        
          
    # Rodapé
    st.markdown("""
        <div style='
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        '>
            © 2024 Análise de Mercado • Dados históricos Amazon
        </div>
    """, unsafe_allow_html=True)

# Executa o dashboard
if __name__ == "__main__":
    main()