import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

df = pd.read_csv("frota.csv" , encoding='latin-1', sep=';')
df = df.replace('-', '0')

st.dataframe(df.drop(columns=['Ano']))
df.iloc[:, 1:] = df.iloc[:, 1:].apply(
    lambda col: pd.to_numeric(
        col.astype(str)
        .str.replace(r'\.0$', '', regex=True)  # Remove o ".0" apenas no final
        .str.replace('.', '', regex=False)  # Remove separador de milhares
        .str.replace(',', '.', regex=False),  # Troca vírgula decimal por ponto
        errors='coerce'
    )
)
for col in df.columns[1:]:
    if col != 'Ano' and col != 'Localidade':
        df[col] = df[col].astype(int)

st.title("Frota de Veículos no Estado de Goiás")
with st.sidebar:
    st.header("Municípios")
    municipios = df['Localidade'].unique()
    municipio = st.selectbox("Selecione um município", municipios)

st.subheader(f"Município selecionado: {municipio}")	
st.dataframe(df[df['Localidade'] == municipio].drop(columns=['Ano', 'Localidade']))
veiculos_por_pessoa = df[df['Localidade'] == municipio]['Frota de Veículos - Total (número)'].values[0] / df[df['Localidade'] == municipio]['População Estimada - Total (habitantes)'].values[0]
onibus_por_pessoa = 70 * df[df['Localidade'] == municipio]['Frota de Veículos - Ônibus (número)'].values[0] / df[df['Localidade'] == municipio]['População Estimada - Total (habitantes)'].values[0]
st.write(f"Veículos por habitante: {veiculos_por_pessoa.round(2)}")
st.write(f"Ônibus para cada grupo de 70 habitantes: {onibus_por_pessoa.round(2)}")
st.bar_chart(df[df['Localidade'] == municipio].drop(columns=['Localidade']).set_index('Ano').T, use_container_width=True)