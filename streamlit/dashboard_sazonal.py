# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import find_peaks
from statsmodels.tsa.seasonal import STL
from sklearn.linear_model import LinearRegression

# =================================================================================
# Configurações da Página
# =================================================================================
st.set_page_config(
    page_title="Análise Técnica AMZN",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para estilização
st.markdown("""
    <style>
    .main {background-color: #FFFFFF; color: #000000;}
    .metric-box {padding: 20px; border-radius: 5px; background-color: #f8f9fa;}
    .insight-section {margin-top: 2rem; padding: 1.5rem; border-left: 4px solid #2A9FD8;}
    </style>
    """, unsafe_allow_html=True)

# =================================================================================
# Funções de Análise (Original do Jupyter Notebook - PRESERVADAS)
# =================================================================================
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Carrega e cacheia dados com tratamento de erros"""
    try:
        df = pd.read_csv(file_path, parse_dates=['date'])
        df = df[['date', 'adj_close']].sort_values('date').set_index('date')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Trata dados ausentes e garante integridade temporal"""
    try:
        df = df.asfreq('D', method='ffill')
        df['adj_close'] = df['adj_close'].interpolate()
        return df
    except Exception as e:
        st.error(f"Erro no pré-processamento: {e}")
        return df

def analyze_trends(df: pd.DataFrame) -> tuple:
    """Calcula médias móveis e tendência linear"""
    try:
        df['ma_30'] = df['adj_close'].rolling(30).mean()
        df['ma_90'] = df['adj_close'].rolling(90).mean()
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['adj_close'].values
        model = LinearRegression().fit(X, y)
        df['trend_line'] = model.predict(X)
        return df, model.coef_[0]
    except Exception as e:
        st.error(f"Erro na análise de tendências: {e}")
        return df, 0

def analyze_seasonality(df: pd.DataFrame, period: int = 365) -> tuple:
    """Decompõe a série temporal em componentes sazonais"""
    try:
        decomposition = STL(df['adj_close'], period=period).fit()
        seasonal_strength = np.abs(decomposition.seasonal).mean()
        return decomposition.seasonal, seasonal_strength
    except Exception as e:
        st.error(f"Erro na análise sazonal: {e}")
        return pd.Series(), 0

def identify_critical_points(series: pd.Series, prominence: float = 0.1) -> tuple:
    """Identifica picos e vales na série temporal"""
    try:
        peaks, _ = find_peaks(series, prominence=prominence * series.std())
        valleys, _ = find_peaks(-series, prominence=prominence * series.std())
        return peaks, valleys
    except Exception as e:
        st.error(f"Erro na identificação de pontos críticos: {e}")
        return np.array([]), np.array([])

# =================================================================================
# Funções de Interface Streamlit
# =================================================================================
def create_interactive_controls():
    """Cria componentes interativos na sidebar"""
    with st.sidebar:
        st.header("⚙️ Controles Analíticos")
        prominence = st.slider("Sensibilidade de Picos/Vales", 0.05, 0.5, 0.15, 0.05,
                             help="Ajusta a sensibilidade na detecção de pontos críticos")
        window_ma = st.selectbox("Janela Média Móvel", [30, 60, 90], index=2,
                               help="Selecione o período para cálculo das médias móveis")
    return prominence, window_ma

def display_main_metrics(trend_slope, seasonal_strength):
    """Exibe métricas-chave em layout responsivo"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Tendência Diária", f"${abs(trend_slope):.2f}", 
                "Alta" if trend_slope > 0 else "Baixa")
    with col2:
        st.metric("🔄 Força Sazonal", f"{seasonal_strength:.1f} pts",
                "Forte" if seasonal_strength > 5 else "Fraca")
    with col3:
        st.metric("📅 Período Analisado", "1997-2025")

def plot_interactive_chart(df, peaks, valleys):
    """Converte o gráfico matplotlib para Plotly mantendo estilo original"""
    fig = go.Figure()
    
    # Linha base
    fig.add_trace(go.Scatter(x=df.index, y=df['adj_close'],
                          name='Preço Ajustado', line=dict(color='lightgrey')))
    
    # Elementos interativos
    fig.add_trace(go.Scatter(x=df.index, y=df['ma_30'],
                          name='MM 30 Dias', line=dict(color='blue', width=1.5)))
    
    fig.add_trace(go.Scatter(x=df.index, y=df['ma_90'], 
                          name='MM 90 Dias', line=dict(color='green', width=1.5)))
    
    fig.add_trace(go.Scatter(x=df.index, y=df['trend_line'],
                          name='Tendência', line=dict(color='red', dash='dot')))
    
    # Marcadores interativos
    fig.add_trace(go.Scatter(x=df.index[peaks], y=df['adj_close'].iloc[peaks],
                          mode='markers', name='Picos', marker=dict(symbol='triangle-up', size=10)))
    
    fig.add_trace(go.Scatter(x=df.index[valleys], y=df['adj_close'].iloc[valleys],
                          mode='markers', name='Vales', marker=dict(symbol='triangle-down', size=10)))
    
    # Layout customizado
    fig.update_layout(
        title='Análise Técnica - Preço Ajustado AMZN',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        hovermode="x unified",
        template='plotly_white',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

def display_insights(df, peaks, valleys, trend_slope):
    """Exibe insights em formato profissional com emojis"""
    with st.expander("💡 Insights Estratégicos", expanded=True):
        latest_peak = df.index[peaks[-1]].strftime('%d/%m/%Y') if len(peaks) > 0 else "N/A"
        latest_valley = df.index[valleys[-1]].strftime('%d/%m/%Y') if len(valleys) > 0 else "N/A"
        
        st.markdown(f"""
        **📊 Dinâmica de Mercado**  
        - Tendência diária de **{"alta" if trend_slope > 0 else "baixa"}** com variação média de ${abs(trend_slope):.2f}
        - {len(peaks)} eventos de pico identificados
        - {len(valleys)} oportunidades de vale detectadas


        **🎯 Recomendações Operacionais**  
        - Estratégia de compra nos próximos vales identificados
        - Monitoramento contínuo da volatilidade sazonal
        - Utilização das médias móveis como indicadores de timing


        **🎯 Últimos Eventos Relevantes**  

        ▶️ Pico mais recente: {latest_peak}  
        ◀️ Vale mais recente: {latest_valley}
        """)

# =================================================================================
# Função Principal
# =================================================================================
def main():
    """Função principal do dashboard"""
    # Controles e Dados
    prominence, window_ma = create_interactive_controls()
    df = load_data('../data/processed/AMZN_1997-05-15_2025-02-21_atualizado.csv')
    
    if df is None:
        return
    
    # Processamento
    df = preprocess_data(df)
    df, trend_slope = analyze_trends(df)
    seasonal_component, seasonal_strength = analyze_seasonality(df)
    peaks, valleys = identify_critical_points(df['adj_close'], prominence)
    
    # Layout Principal
    st.title('📈 Análise Técnica de Ações AMZN')
    display_main_metrics(trend_slope, seasonal_strength)
    
    # Visualização
    plot_interactive_chart(df, peaks, valleys)
    
    # Insights
    display_insights(df, peaks, valleys, trend_slope)

if __name__ == "__main__":
    main()