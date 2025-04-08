# Dupla do trabalho: Pedro Paulo Carvalho Vieira e Rodrigo Santana Esperidião
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")

#Obter os dados do arquivo CSV
df = pd.read_csv("frota.csv" , encoding='latin-1', sep=';')
colunas_desejadas = {
    'Ano': 'Ano',
    'Localidade': 'Localidade',
    'Frota de Veículos - Total (número)': 'Frota de Veículos - Total',
    'Frota de Veículos - Automóvel (número)': 'Frota de Automóveis',
    'Frota de Veículos - Motocicleta (número)': 'Frota de Motocicletas',
    'Frota de Veículos - Ônibus (número)': 'Frota de Ônibus'
}

#Tratamento dos dados
df = df.replace(' -   ', '1')
df = df.rename(columns=colunas_desejadas)

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
    


df['População Total'] = df['População - Projeção  - Masculina - Total -UFRN (habitantes)'] + df['População - Projeção  - Feminina - Total - UFRN (habitantes)']

# Criar os filtros com a sidebar
with st.sidebar:
    st.header("Municípios")
    municipios = df['Localidade'].unique()
    municipio = st.selectbox("Selecione um município", municipios)

    categorias = ['Todas', 'Frota de Veículos - Total', 'Frota de Automóveis', 'Frota de Motocicletas', 'Frota de Ônibus']
    categoria = st.selectbox("Selecione uma categoria", categorias)

    anos = df['Ano'].unique()
    anos = ['Todos'] + anos.tolist()
    ano = st.selectbox("Selecione um ano", anos)

#Arquivo Principal

st.title("Frota de Veículos no Estado de Goiás")
st.subheader(f"Município selecionado: {municipio}")	

# Filtra os dados com base nas seleções
df_filtrado = df.copy()

if municipio != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Localidade'] == municipio]

if ano != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Ano'] == ano]

# Se uma categoria específica for selecionada
if categoria != 'Todas':
    colunas_para_mostrar = ['Ano','População Total', categoria]
else:
    colunas_para_mostrar = ['Ano', 'População Total',
                            'Frota de Veículos - Total', 'Frota de Automóveis',
                            'Frota de Motocicletas', 'Frota de Ônibus']
    
# Mostra o DataFrame filtrado
st.dataframe(df_filtrado[colunas_para_mostrar], hide_index=True)


#Cálculo dos KPI's para Business Intelligence
veiculos_por_pessoa = df_filtrado['Frota de Veículos - Total'].values.mean() / df_filtrado['População Total'].values.mean()
automoveis_por_pessoa = df_filtrado['Frota de Automóveis'].values.mean() / df_filtrado['População Total'].values.mean()
motocicletas_por_pessoa = df_filtrado['Frota de Motocicletas'].values.mean() / df_filtrado['População Total'].values.mean()
onibus_por_pessoa = 70 * df_filtrado['Frota de Ônibus'].values.mean() / df_filtrado['População Total'].values.mean()


with st.expander("Observação", expanded=True):
    st.write("A coluna 'Frota de Veículos - Total' inclui todos os tipos de veículos (automóvel, caminhão, caminhão trator, caminhonete, camioneta, ciclomotor, micro-ônibus, motocicleta, motoneta, ônibus, reboque, semi reboque, trator rodas, triciclo e outros.")

with st.expander("KPI's", expanded=True):
    columns = st.columns(4)
    columns[0].metric(label="Total de veículos por habitante", value=veiculos_por_pessoa.round(2))
    columns[1].metric(label="Automóveis por habitante", value=automoveis_por_pessoa.round(2))
    columns[2].metric(label="Motocicletas por habitante", value=motocicletas_por_pessoa.round(2))
    columns[3].metric(label="Ônibus para cada grupo de 70 habitantes", value=onibus_por_pessoa.round(2))


#Layout com Gráficos
if categoria != 'Todas':
    colunas = ['População Total', categoria]
else:
    colunas = [
        'População Total',
        'Frota de Veículos - Total',
        'Frota de Automóveis',
        'Frota de Motocicletas',
        'Frota de Ônibus'
    ]
# Filtragem e preparação dos dados
df_plot = df_filtrado[colunas + ['Ano']].set_index('Ano').T
df_plot = df_plot.loc[colunas]  # Garante a orde m

# Criação do gráfico de barras com plotly express
# O plotly express foi escolhido por permitir a ordenação das colunas do gráfico de acordo com a ordem do DataFrame
fig = px.bar(
    df_plot,
    barmode='group',
    labels={'value': 'Quantidade', 'index': 'Categoria', 'variable': 'Ano'},
)

fig.update_layout(
    title=f'Evolução por Ano - {municipio}',
    xaxis_title='Categoria',
    yaxis_title='Quantidade',
    bargap=0.15,
    bargroupgap=0.1
)
# Apresentação do gráfico
st.plotly_chart(fig, use_container_width=True)
