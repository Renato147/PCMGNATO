import streamlit as st
import pandas as pd
import geopandas as gpd
import streamlit.components.v1 as components
from PIL import Image
import folium
from folium import plugins
st.set_page_config(layout="wide")
merged_df = pd.DataFrame()
img = Image.open('minas.png')
new_width = int(img.width * 0.1)
new_height = int(img.height * 0.1)
img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
# Calcular as novas dimensões (10% do tamanho original)

st.image(img_resized, caption='')
st.title('Visão Regional dos Investimentos Parlamentares em Minas Gerais ')
# Redimensionar a imagem

caminho_do_arquivo = 'PCMG.csv'
df2 = pd.read_excel("nato2.xlsx")
#f2= df2.groupby(['Município Beneficiado (Padronizado)', 'Parlamentar','Unidade Beneficiária (Padronizado)','Ação Orçamentária','Categoria (Padronizado)']).agg({
    #'Valor Total LIQUIDADO': 'sum',
    #'Código SIAD': 'first'
#}).reset_index()
df2 = df2[df2["Município Beneficiado (Padronizado)"] != ""]
df_municipios = pd.read_csv('municipios.csv')
df_merged = pd.merge(df2, df_municipios, left_on='Município Beneficiado (Padronizado)', right_on='nome', how='inner')
geojson_path = 'municipios.geojson.json'
gdf = gpd.read_file(geojson_path)
gdf["id"] = gdf["id"].astype(int)
gdfj = gdf.merge(df_merged, left_on='id', right_on='codigo_ibge', how='inner')
#gdfj =pd.read_csv('PCMG23.csv',sep=",")
# Carregar a imagem

df = pd.read_csv(caminho_do_arquivo,sep=",")
#df2 = pd.read_csv(caminho_do_arquivo2,sep=",")
#df2['Parlamentar'] = df2['Parlamentar'].replace('        DELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)
#df2['Parlamentar'] = df2['Parlamentar'].replace("\tDELEGADA SHEILA", 'DELEGADA SHEILA', regex=True)

# Crie um mapa Folium
m3 = folium.Map(
    location=[-19.235, -51.925],  # Coordenadas aproximadas do Brasil
    zoom_start=6,
    tiles='cartodb positron'  # Estilo do mapa
)

# Suponha que você tenha um arquivo GeoJSON chamado "municipios.geojson"
# Substitua esta linha pelo caminho correto do seu arquivo GeoJSON ou pela fonte de dados geográficos


# Faça o merge entre os DataFrames
#gdf = gdf.merge(df_merged, left_on='id', right_on='codigo_ibge', how='inner')

# Aplique o logaritmo à coluna de proporção
#gdfj ['log_proporcao_vitimas'] = np.log1p(gdfj['qtde_vitimas_x'])  # Use log1p para evitar problemas com valores zero

# Crie a sobreposição de municípios preenchidos com base na coluna de proporção logarítmica
folium.Choropleth(
    geo_data=gdfj,
    name='choropleth',
    data=gdfj,
    columns=['codigo_ibge', 'Valor Total LIQUIDADO'],  # Use a coluna logarítmica aqui
    key_on='feature.properties.codigo_ibge',
    fill_color='YlOrRd',  # Esquema de cores (YlOrRd é um exemplo)
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Valor Total LIQUIDADO'
).add_to(m3)

# Adicione um controle de camadas (layers control) ao mapa
folium.LayerControl().add_to(m3)

# Salve o mapa em um arquivo HTML
m3.save('municipios_com_proporcao_log.html')
HtmlFile = open("municipios_com_proporcao_log.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
st.subheader(f'Mapa de Valor Liquidado ')
#components.html(source_code,height = 600)
components.html(source_code,height = 600)
# Exibir a imagem redimensionada no Streamlit
# Exibir a imagem redimensionada no Streamlit

# Supondo que 'df' seja o seu DataFrame original
# Criando um novo DataFrame sem a quarta coluna
novo_df = df.drop(df.columns[3], axis=1)
print(novo_df["Parlamentar"].value_counts())
novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('        DELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)
novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('\tDELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)
#novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('  DELEGADA SHEILA', 'Del. SHEILA')
#st.image('minas.png', caption='', use_column_width=True)

#st.table(novo_df.head(20))

m = folium.Map(location=[novo_df['latitude'].mean(), novo_df['longitude'].mean()], zoom_start=7)
# Crie um mapa com base na escolha do usuário
for index, row in novo_df.iterrows():  # Corrija o erro de sintaxe na linha do loop
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,  # Ajuste o tamanho do marcador conforme necessário
                popup = (
                            f'Parlamentar: {row["Parlamentar"]}, '
                            f'Valor Total Liquidado: R${round(row["Valor Total LIQUIDADO"]*100, 2)}, '
                            f'Categoria: {row["Categoria (Padronizado)"]}, '
                            f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                        ),
  # Exibe o valor da probabilidade no pop-up
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)
            # Adicionar controle de camadas (para alternar entre as camadas)


    # Exiba o mapa no Streamlit
        
else:
    st.write('Os marcadores estão desativados. Marque a caixa para mostrá-los no mapa.')
folium.LayerControl().add_to(m)

# Salve o mapa em um arquivo HTML no diretório do projeto
m.save('mapa_de_calor_interativo.html')
HtmlFile = open("mapa_de_calor_interativo.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
st.subheader(f'Mapa de Valor Liquidado ')
#components.html(source_code,height = 600)
components.html(source_code,height = 600)







parlamentares_unicos = novo_df['Parlamentar'].unique()
show_markers2 = st.checkbox('Exibir mapa por Atuação de Parlamentar', key='show_markers2')
if show_markers2:
    parlamentar_selecionado = st.selectbox('Selecione um Parlamentar', parlamentares_unicos)
    df_parlamentar=novo_df[novo_df['Parlamentar'] == parlamentar_selecionado]
    
    
    m2 = folium.Map(location=[df_parlamentar['latitude'].mean(), df_parlamentar['longitude'].mean()], zoom_start=7)
    # Criar uma caixa de seleção com os valores únicos
    

    # Agora você pode usar a variável parlamentar_selecionado para outras operações
    # Por exemplo, mostrar dados filtrados por esse parlamentar
    

    # Adicione um checkbox para controlar a exibição dos marcadores
    
    # Substitua as coordenadas e o nível de zoom conforme necessário

    # Adicionar marcadores de círculo
    for index, row in df_parlamentar.iterrows():  # Corrija o erro de sintaxe na linha do loop
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,  # Ajuste o tamanho do marcador conforme necessário
                popup = (
                            f'Parlamentar: {row["Parlamentar"]}, '
                            f'Valor Total Liquidado: R${round(row["Valor Total LIQUIDADO"]*100, 2)}, '
                            f'Categoria: {row["Categoria (Padronizado)"]}, '
                            f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                        ),
  # Exibe o valor da probabilidade no pop-up
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m2)
    # Adicionar controle de camadas (para alternar entre as camadas)
    folium.LayerControl().add_to(m)

    # Salve o mapa em um arquivo HTML no diretório do projeto
    m2.save('mapa_de_calor_interativo2.html')
    HtmlFile = open("mapa_de_calor_interativo2.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.subheader(f'Mapa de Valor Liquidado / Parlamentar {parlamentar_selecionado }')
    #components.html(source_code,height = 600)
    components.html(source_code,height = 600)
    st.write(df_parlamentar)
    # Exiba o mapa no Streamlit
        
else:
    st.write('Os marcadores estão desativados. Marque a caixa para mostrá-los no mapa.')

