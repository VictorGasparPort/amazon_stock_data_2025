# Importações necessárias
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import sys

# Configurações iniciais da página
def configurar_pagina():
    """Configura os parâmetros iniciais da página Streamlit"""
    st.set_page_config(
        page_title="Análise de Ações AMZN",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Aplicar estilos CSS personalizados
    aplicar_estilos()

def aplicar_estilos():
    """Define os estilos CSS customizados para o dashboard"""
    st.markdown("""
        <style>
            /* Fonte profissional e cores básicas */
            html, body, [class*="css"] {
                font-family: 'Arial', sans-serif;
                color: #333;
                background-color: #FFFFFF;
            }
            
            /* Cabeçalhos com emojis */
            h1, h2, h3 {
                color: #000000 !important;
                margin-bottom: 1.5rem;
            }
            
            /* Espaçamento entre elementos */
            .block-container {
                padding: 2rem 1rem;
            }
            
            /* Cards de relatório estilizados */
            .report-card {
                padding: 1.5rem;
                background-color: #F8F9FA;
                border-radius: 0.5rem;
                margin: 1rem 0;
                border-left: 4px solid #2C3E50;
            }
        </style>
    """, unsafe_allow_html=True)

@st.cache_data
def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Carrega e processa os dados do CSV com tratamento de erros
    
    Parâmetros:
    caminho (str): Caminho do arquivo CSV
    
    Retorna:
    pd.DataFrame: DataFrame processado
    """
    try:
        df = pd.read_csv(caminho, parse_dates=['date'])
        df.sort_values('date', inplace=True)
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado!")
        sys.exit(1)
    except KeyError:
        st.error("Coluna 'date' não encontrada nos dados!")
        sys.exit(1)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        sys.exit(1)

def processar_maximos_minimos(df: pd.DataFrame) -> dict:
    """
    Processa os valores máximos e mínimos das colunas numéricas
    
    Parâmetros:
    df (pd.DataFrame): DataFrame para análise
    
    Retorna:
    dict: Dicionário estruturado com os resultados
    """
    resultados = {}
    colunas_numericas = df.select_dtypes(include=['number']).columns
    
    for coluna in colunas_numericas:
        try:
            max_val = df[coluna].max()
            min_val = df[coluna].min()
            data_max = df.loc[df[coluna].idxmax(), 'date']
            data_min = df.loc[df[coluna].idxmin(), 'date']
            
            resultados[coluna] = {
                'maximo': max_val,
                'data_max': data_max,
                'minimo': min_val,
                'data_min': data_min
            }
        except Exception as e:
            st.error(f"Erro ao processar coluna {coluna}: {str(e)}")
    
    return resultados

def criar_grafico_interativo(df: pd.DataFrame, coluna: str, resultados: dict):
    """
    Cria gráfico interativo com Plotly destacando máximos e mínimos
    
    Parâmetros:
    df (pd.DataFrame): DataFrame com dados
    coluna (str): Coluna selecionada para visualização
    resultados (dict): Resultados do processamento
    """
    fig = go.Figure()
    
    # Linha principal
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df[coluna],
        mode='lines',
        name=coluna,
        line=dict(color='#2C3E50')
    ))
    
    # Destacar máximo e mínimo
    if coluna in resultados:
        max_data = resultados[coluna]['data_max']
        min_data = resultados[coluna]['data_min']
        
        fig.add_trace(go.Scatter(
            x=[max_data],
            y=[resultados[coluna]['maximo']],
            mode='markers',
            name='Máximo',
            marker=dict(color='#27AE60', size=10)
        ))
        
        fig.add_trace(go.Scatter(
            x=[min_data],
            y=[resultados[coluna]['minimo']],
            mode='markers',
            name='Mínimo',
            marker=dict(color='#E74C3C', size=10)
        ))
    
    fig.update_layout(
        template='plotly_white',
        title=f"Variação Histórica - {coluna}",
        xaxis_title='Data',
        yaxis_title='Valor',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def exibir_relatorio(resultados: dict, coluna_selecionada: str):
    """
    Exibe o relatório formatado em cards estilizados
    
    Parâmetros:
    resultados (dict): Dados processados
    coluna_selecionada (str): Coluna para exibição detalhada
    """
    if coluna_selecionada in resultados:
        dados = resultados[coluna_selecionada]
        
        relatorio = f"""
        ## 📈 Análise Detalhada - {coluna_selecionada}
        
        **Máximo Histórico:**  
        🟢 {dados['maximo']:.2f} em {dados['data_max'].strftime('%d/%m/%Y')}
        
        **Mínimo Histórico:**  
        🔴 {dados['minimo']:.2f} em {dados['data_min'].strftime('%d/%m/%Y')}
        """
        
        st.markdown(f"""
            <div class="report-card">
                {relatorio}</div>
        """, unsafe_allow_html=True)

def criar_filtro_data(df: pd.DataFrame) -> tuple:
    """
    Cria slider de data com limites do dataset
    
    Parâmetros:
    df (pd.DataFrame): DataFrame com dados
    
    Retorna:
    tuple: (data_inicio, data_fim) selecionadas
    """
    min_date = df['date'].min().to_pydatetime()
    max_date = df['date'].max().to_pydatetime()
    
    return st.slider(
        "Selecione o Período de Análise:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD/MM/YYYY"
    )

def main():
    # Configurar página
    configurar_pagina()
    
    # Carregar dados
    st.title("📊 Máximas e Mínimas Históricas - AMAZON")
    df = carregar_dados('../data/processed/AMZN_1997-05-15_2025-02-21_atualizado.csv')
    
    # Seção de Filtros
    with st.container():
        st.header("🔍 Filtros de Análise")
        
        # Filtro de data
        data_inicio, data_fim = criar_filtro_data(df)
        df_filtrado = df[(df['date'] >= data_inicio) & (df['date'] <= data_fim)]
        
        # Dropdown para seleção de coluna
        colunas_numericas = df_filtrado.select_dtypes(include=['number']).columns
        coluna_selecionada = st.selectbox(
            "Selecione a Métrica para Análise:",
            options=colunas_numericas,
            index=0
        )
    
    # Processar dados
    resultados = processar_maximos_minimos(df_filtrado)
    
    # Layout em Grid
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        # Exibir relatório
        exibir_relatorio(resultados, coluna_selecionada)
    
    with col2:
        # Exibir gráfico
        criar_grafico_interativo(df_filtrado, coluna_selecionada, resultados)

if __name__ == "__main__":
    main()