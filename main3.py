import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.header("Previsão de Vendas")

# Dados: [Investimento em Marketing] -> Faturamento
dados_vendas = pd.DataFrame({
    'investimento': [100, 200, 300, 400, 500, 600],
    'faturamento': [1200, 2500, 3200, 4800, 5100, 6300]
})

# objetivo: previsão de FATURAMENTO baseado nos investimentos

st.line_chart(dados_vendas, x = 'investimento', y= 'faturamento')
modelo_faturamento=LinearRegression()
modelo_faturamento.fit(dados_vendas[['investimento']],dados_vendas[['faturamento']])

invest = st.slider('investimento', 100,600,300)
faturamento_final = modelo_faturamento.predict([[invest]])
print(faturamento_final)


st.metric(f'Seu faturamento seria' ,f'{min(faturamento_final[0],):.2f}')

