# \script\maquina\Scripts>activate
# \script>streamlit run app_data_viz.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import sqlalchemy
import numpy as np


st.title('Analise dos Candidatos Presentes do Enem 2023')
st.sidebar.header('Filtros')

@st.cache_data
def carregar_dados():
    engine = create_engine('sqlite:///banco.db')
    query = "SELECT * FROM dados"
    enem = pd.read_sql(query, con=engine)
    return enem

dados = carregar_dados()
#st.dataframe(dados)

############ EXPANSÃO 1 #################
caixa1 = st.expander('DADOS GERAIS DOS CANDIDATOS PRESENTES')
with caixa1:
    col1, col2, col3 =st.columns(3)

    cand_F = dados['TP_SEXO'] == 'F'
    contagemF = dados[cand_F]
    contagemF = contagemF['TP_SEXO'].count()
    cand_M = dados['TP_SEXO'] == 'M'
    contagemM = dados[cand_M]
    contagemM = contagemM['TP_SEXO'].count()
    
    col1.metric('Total de candidatos', dados['TP_SEXO'].count())
    col2.metric("Média de notas de redação", round(dados.NU_NOTA_REDACAO.mean(), 2))
    col3.metric('Mediana de Notas de Redação', round(dados.NU_NOTA_REDACAO.median(),2))
    col1.metric('Desvio Padrão da Nota de Redação', round(dados.NU_NOTA_REDACAO.std(),2))
    col2.metric('Média de Notas Matemática', round(dados.NU_NOTA_MT.mean(), 2))
    col3.metric('Mediana de Notas de Redação', round(dados.NU_NOTA_MT.median(),2))
    col1.metric('Desvio Padrão da Nota de Redação', round(dados.NU_NOTA_MT.std(),2))

    # Gráfico de Pizza da qnt de alunos por sexo    
    st.subheader('Quantidades de alunos por sexo') 
    sexo_contagem = dados['TP_SEXO'].value_counts().reset_index().rename(columns={'TP_SEXO': 'SEXO', 'count': 'Quantidade'})
    figTorta = px.pie(sexo_contagem, values='Quantidade', names='SEXO')
    st.plotly_chart(figTorta)

    # Boxplot Notas de Redação  
    st.subheader('BoxPlot Notas de Redação')  
    box_notas = dados['NU_NOTA_REDACAO'].reset_index().drop('index', axis=1).rename(columns={'NU_NOTA_REDACAO': 'NOTA_REDACAO'})
    figBOX = px.box(box_notas, x='NOTA_REDACAO')
    st.plotly_chart(figBOX)
    
    # Boxplot Notas de Matematica
    st.subheader('BoxPlot Notas de Matematica')  
    box_notas_mat = dados['NU_NOTA_MT'].reset_index().drop('index', axis=1).rename(columns={'NU_NOTA_MT': 'NOTA_MATEMATICA'})
    figBOXmat = px.box(box_notas_mat, x='NOTA_MATEMATICA')
    st.plotly_chart(figBOXmat)

    # Histograma das notas de redacao
    st.subheader('Histograma Notas Redação')  
    hist_nota_redacao = dados['NU_NOTA_REDACAO'].reset_index().rename(columns={'NU_NOTA_REDACAO':'NOTA DE REDACAO'})
    fig_hist_redacao = px.histogram(hist_nota_redacao, x = 'NOTA DE REDACAO')
    st.plotly_chart(fig_hist_redacao)

    # Histograma das notas de Matemática
    st.subheader('Histograma Notas Matematica') 
    hist_nota_mat = dados['NU_NOTA_MT'].reset_index().rename(columns={'NU_NOTA_MT':'NOTA DE MATEMATICA'})
    fig_hist_mat = px.histogram(hist_nota_mat, x = 'NOTA DE MATEMATICA', nbins = 60)
    st.plotly_chart(fig_hist_mat)

##################SideBar Filtro de Sexo#################
sidesexo = dados['TP_SEXO'].drop_duplicates()
opc1 = st.sidebar.selectbox('Sexo do Candidato',sidesexo)
sexo_escolha = dados.loc[dados['TP_SEXO'] == opc1] # dF da Escolha de Gênero

##################### Expansão 2#####################
caixa2 = st.expander(f'Filtro por sexo : {opc1}')
with caixa2:
    #Informações Gerais da escolha
    col1, col2, col3 =st.columns(3)
    col1.metric(f'Quantidade de candidatos {opc1}:', sexo_escolha['TP_SEXO'].count())
    col2.metric(f'Média das notas de Redação:', round(sexo_escolha['NU_NOTA_REDACAO'].mean(), 2))
    col3.metric(f'Media das notas de Matemática', round(sexo_escolha['NU_NOTA_MT'].mean(), 2))
    col1.metric('Mediana da Nota de Redação', round(sexo_escolha['NU_NOTA_REDACAO'].median(),2))
    col2.metric('Desvio Padrão da Nota de Redação', round(sexo_escolha['NU_NOTA_REDACAO'].std(),2))

    # Histograma das notas de Redação
    st.subheader('Histograma Notas Redacão')
    notas_reda = sexo_escolha['NU_NOTA_REDACAO'].reset_index().rename(columns={'NU_NOTA_REDACAO': 'NOTA DE REDACAO'})
    fig_red = px.histogram(notas_reda, x='NOTA DE REDACAO')
    st.plotly_chart(fig_red)

    # Histograma das notas de Matemática
    st.subheader('Histograma Notas Matemática')
    notas_mat = sexo_escolha['NU_NOTA_MT'].reset_index().rename(columns={'NU_NOTA_MT': 'NOTA DE MATEMATICA'})
    fig_mat = px.histogram(notas_mat, x='NOTA DE MATEMATICA', nbins = 40)
    st.plotly_chart(fig_mat)
    
    #Gráfico de Barras Média de notas de Redação por Renda Familiar
    st.subheader('Média de notas de Redação pela renda Familiar declarada')
    agrupados_por_renda = sexo_escolha.groupby('R_Q006')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q006': 'Renda Familiar', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
    st.bar_chart(agrupados_por_renda, x_label = 'Renda Familiar', y_label = 'Media Notas de Redação')

    # Filtro da Escolaridade da Mãe
    mae_escolaridade = sexo_escolha['R_Q002'].drop_duplicates()
    mae_escolaridade_se = st.selectbox('Grau de Escolaridade da Mãe', mae_escolaridade)
    mae_escolaridade_escolha = sexo_escolha[sexo_escolha['R_Q002'] == mae_escolaridade_se] # dF com a escolaridade da mãe escolhida

    # BoxPlot das Notas de Redação pela Escolaridade da mãe
    st.subheader('Notas de Redação pela escolaridade da mãe do candidato')
    box_mae_escolha = mae_escolaridade_escolha['NU_NOTA_REDACAO'].reset_index().drop('index', axis = 1).rename(columns={'NU_NOTA_REDACAO': 'Notas Redação'})
    fig_mae_escolha = px.box(box_mae_escolha, x = 'Notas Redação')
    st.plotly_chart(fig_mae_escolha)
    st.write(f'Media da Nota de Redação {round(mae_escolaridade_escolha['NU_NOTA_REDACAO'].mean(),2)}')
    st.write(f'Mediana da Nota de Redação {round(mae_escolaridade_escolha['NU_NOTA_REDACAO'].median(),2)}')
    st.write(f'Desvio Padrão da Nota de Redação {round(mae_escolaridade_escolha['NU_NOTA_REDACAO'].std(),2)}')

    # BoxPlot das Notas de Redação pela Escolaridade da mãe
    st.subheader('Notas de Matematica pela escolaridade da mãe do candidato')
    box_mae_escolha_mat = mae_escolaridade_escolha['NU_NOTA_MT'].reset_index().drop('index', axis = 1).rename(columns={'NU_NOTA_MT': 'Notas Matematica'})
    fig_mae_escolha_mat = px.box(box_mae_escolha_mat, x = 'Notas Matematica')
    st.plotly_chart(fig_mae_escolha_mat)
    st.write(f'Media da Nota de Matematica {round(mae_escolaridade_escolha['NU_NOTA_MT'].mean(),2)}')
    st.write(f'Mediana da Nota de Matematica {round(mae_escolaridade_escolha['NU_NOTA_MT'].median(),2)}')
    st.write(f'Desvio Padrão da Nota de Matematica {round(mae_escolaridade_escolha['NU_NOTA_MT'].std(),2)}')
 
###################### SideBar Filtro de Tipo de Escola####################
escola = dados['R_TP_ESCOLA'].drop_duplicates()
opc2 = st.sidebar.selectbox('Tipo de Escola', escola)
escolha_escola = dados.loc[dados['R_TP_ESCOLA'] == opc2] # dF da Escolha do tipo de Escola

#################### Expansão 3 ########################
caixa3 = st.expander(f' Filtro "tipo de escola": {opc2}')
with caixa3:
    #Informações Gerais da escolha
    col1, col2, col3 =st.columns(3)
    contagem_opc2 = escolha_escola['TP_SEXO'].count()
    col1.metric('Quantidade de alunos', contagem_opc2)
    col2.metric('Média das Notas de Redação', round(escolha_escola.NU_NOTA_REDACAO.mean(),2))
    col1.metric('Mediana das notas de Redação', round(escolha_escola['NU_NOTA_REDACAO'].median(),2))
    col2.metric('Desvio Padrão das notas de Redação', round(escolha_escola['NU_NOTA_REDACAO'].std(),2))

    # Histograma das notas de Redacão    
    st.subheader('Histograma das nostas de Redação')
    hist_nota_redacao_escola = escolha_escola['NU_NOTA_REDACAO'].reset_index().rename(columns={'NU_NOTA_REDACAO': 'NOTA DE REDACAO'})
    fig_hist_redacao_escola = px.histogram(hist_nota_redacao_escola, x = 'NOTA DE REDACAO')
    st.plotly_chart(fig_hist_redacao_escola)

    # Gráfico de qnt de escolas por Estado
    st.subheader(f'Quantidades de Escolas {opc2} por Estado')
    agrupado_estado = escolha_escola.groupby('SG_UF_ESC')[['R_TP_ESCOLA']].count().rename(columns={'SG_UF_ESC': 'Estado', 'R_TP_ESCOLA': 'Quantidade'})
    st.bar_chart(agrupado_estado, x_label = 'Estados', y_label = f'Quantidade de escola {opc2}')

    #Filtro de renda familiar.
    st.subheader('Média de notas de Redação pela renda declarada')
    agrupado_renda = escolha_escola.groupby('R_Q006')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q006': 'Renda:', 'NU_NOTA_REDACAO': 'Media'}).round(2)
    st.bar_chart(agrupado_renda, x_label = 'Rendas', y_label = 'Media Notas de Redação')

    #Filtro de Escolaridade da Mãe
    st.write('Média de notas de Redação pela escolaridade da mãe')
    agrupado_escolaridade = escolha_escola.groupby('R_Q002')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q002': 'Escolaridade da Mãe', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
    st.bar_chart(agrupado_escolaridade, x_label = 'Escolaridade da Mãe', y_label = 'Media Notas de Redação')

    # Filtro de Sexo
    genero = dados['TP_SEXO'].drop_duplicates()
    g_escolha = st.selectbox('Filtro Escolha o Sexo', genero)
    escolha_genero = escolha_escola[escolha_escola['TP_SEXO'] == g_escolha] # dF do genero escolhido
    st.write(f'Média de notas do gênero {g_escolha} dê escolas "{opc2}": {round(escolha_genero.NU_NOTA_REDACAO.mean(), 2)}')
    st.write(f'Quantidade do gênero {g_escolha} dê escolas "{opc2}": {escolha_genero.TP_SEXO.count()}')   
    
    # Gráfico BoxPlot
    st.subheader(f'BoxPlot Notas de Redação pelo gênero {g_escolha}')
    notas_reda = escolha_genero['NU_NOTA_REDACAO'].reset_index().drop('index', axis=1).rename(columns={'NU_NOTA_REDACAO': 'NOTA_REDACAO'})
    fig1 = px.box(notas_reda, x='NOTA_REDACAO')
    st.plotly_chart(fig1)
    st.write(f'Média da nota de redação pelo sexo {g_escolha}: {notas_reda.NOTA_REDACAO.mean().round(2)}')
    st.write(f'Mediana da nota de redação pelo sexo {g_escolha}: {notas_reda.NOTA_REDACAO.median().round(2)}')
    st.write(f'Desvio Padrão da nota de redação pelo sexo {g_escolha}: {notas_reda.NOTA_REDACAO.std().round(2)}')
    
###################### SideBar Filtro Estado ###################
estado = dados['SG_UF_ESC'].drop_duplicates()
opc4 = st.sidebar.selectbox('Estado', estado)
estado_escolha = dados.loc[dados['SG_UF_ESC'] == opc4] # dF da Escolha do Estado

#################### Expansão 4 ########################
caixa4 = st.expander(f'Filtro por Estado: {opc4}')
with caixa4:
     #Informações Gerais da escolha
     col1, col2, col3 = st.columns(3)
     col1.metric('Quantidade de candidatos: ', estado_escolha['TP_SEXO'].count())
     feminino = estado_escolha[estado_escolha['TP_SEXO'] == 'F']
     masculino = estado_escolha[estado_escolha['TP_SEXO'] == 'M']
     feminino = feminino['TP_SEXO'].count()
     masculino = masculino['TP_SEXO'].count()
     col2.metric('Candidatos Femininos ', feminino)
     col3.metric('Candidatos Masculinos ', masculino)
     col1.metric('Média de notas Redação', round(estado_escolha['NU_NOTA_REDACAO'].mean(),2))
     col2.metric('Média de notas Matemática', round(estado_escolha['NU_NOTA_MT'].mean(),2))
     col1.metric('Mediana da Nota de Redação', round(estado_escolha['NU_NOTA_REDACAO'].median(),2))
     col2.metric('Desvio Padrão da Nota de Redação', round(estado_escolha['NU_NOTA_REDACAO'].std(),2))

     # Histograma das notas de Redação por Estado
     st.subheader(f'Histograma das notas de Redação pelo Estado do {opc4}')
     hist_nota_redacao_estado = estado_escolha['NU_NOTA_REDACAO'].reset_index().rename(columns={'NU_NOTA_REDACAO': 'NOTA DE REDACAO'})  
     fig_hist_redacao_estado = px.histogram(hist_nota_redacao_estado, x = 'NOTA DE REDACAO')
     st.plotly_chart(fig_hist_redacao_estado)

     # Histograma das notas de Matematica por Estado
     st.subheader(f'Histograma das notas de Matemática pelo Estado do {opc4}')
     hist_nota_mat_estado = estado_escolha['NU_NOTA_MT'].reset_index().rename(columns={'NU_NOTA_MT': 'NOTA DE MATEMATICA'})  
     fig_hist_mat_estado = px.histogram(hist_nota_mat_estado, x = 'NOTA DE MATEMATICA', nbins = 60)
     st.plotly_chart(fig_hist_mat_estado)

     #Gráfico de Pizza de Quantidades de alunos por tipo de escola
     st.subheader('Quantidades de alunos por Tipo de Escola')
     escola_contagem = estado_escolha['R_TP_ESCOLA'].value_counts().reset_index().rename(columns={'R_TP_ESCOLA': 'Tipo de Escola', 'count': 'Quantidade'})
     figTorta2 = px.pie(escola_contagem, values='Quantidade', names='Tipo de Escola')
     st.plotly_chart(figTorta2)

     #Gráfico de Barras Média de notas de Redação por Escolaridade da Mãe
     st.subheader('Média de notas de Redação pela Escolaridade da Mãe')
     agrupado_escolaridade_mae = estado_escolha.groupby('R_Q002')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q002': 'Escolaridade da Mãe', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
     st.bar_chart(agrupado_escolaridade_mae, x_label = 'Escolaridade da Mãe', y_label = 'Media Notas de Redação')

     #Gráfico de Barras Média de notas de Redação por Renda Familiar 
     st.subheader('Média de notas de Redação pela renda Familiar declarada')
     agrupado_escolaridade_mae = estado_escolha.groupby('R_Q006')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q006': 'Renda Familiar', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
     st.bar_chart(agrupado_escolaridade_mae, x_label = 'Renda Familiar', y_label = 'Media Notas de Redação')
