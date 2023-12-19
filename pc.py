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
img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
st.title('Visão Regional dos Investimentos Parlamentares em Minas Gerais ')

# Calcular as novas dimensões (10% do tamanho original)
st.sidebar.title('Soluções Digitais ')
paginaSelecionada = st.sidebar.selectbox('Escolha uma opção', ['Valor Liquidado','Valor Previsto','Valor Empenhado'])


if paginaSelecionada == 'Valor Liquidado':
    
    #st.sidebar.image(img_resized, caption='', use_column_width=True)
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
    #st.table(df.head(10))
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

    show_markers22 = st.checkbox('Exibir Pontos no mapa', key='show_markers22')


    if show_markers22:
        for index, row in gdfj.iterrows():  # Corrija o erro de sintaxe na linha do loop
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=10,  # Ajuste o tamanho do marcador conforme necessário
                    popup = (
                                f'Parlamentar: {row["Parlamentar"]}, '
                                f'Valor Total Liquidado: R${round(row["Valor Total LIQUIDADO"], 2)}, '
                                f'Categoria: {row["Categoria (Padronizado)"]}, '
                                f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                            ),
    # Exibe o valor da probabilidade no pop-up
                    color='blue',
                    fill=True,
                    fill_color='blue'
                ).add_to(m3)
    # Exibir a imagem redimensionada no Streamlit
    # Exibir a imagem redimensionada no Streamlit
    # Salve o mapa em um arquivo HTML
    m3.save('municipios_com_proporcao_log.html')
    HtmlFile = open("municipios_com_proporcao_log.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.subheader(f'Mapa de Valor Liquidado ')
    #components.html(source_code,height = 600)

    components.html(source_code,height = 600)
    # Supondo que 'df' seja o seu DataFrame original
    # Criando um novo DataFrame sem a quarta coluna
    novo_df = df.drop(df.columns[3], axis=1)

    novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('        DELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)
    novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('\tDELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)





    parlamentares_unicos = novo_df['Parlamentar'].unique()
    parlamentares_unicos_ordenados = sorted(parlamentares_unicos)
    show_markers2 = st.checkbox('Exibir mapa por Atuação de Parlamentar', key='show_markers2')
    if show_markers2:
        parlamentar_selecionado = st.selectbox('Selecione um Parlamentar', parlamentares_unicos_ordenados)
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
                                f'Valor Total Liquidado: R${round(row["Valor Total LIQUIDADO"], 2)}, '
                                f'Categoria: {row["Categoria (Padronizado)"]}, '
                                f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                            ),
    # Exibe o valor da probabilidade no pop-up
                    color='blue',
                    fill=True,
                    fill_color='blue'
                ).add_to(m2)
        # Adicionar controle de camadas (para alternar entre as camadas)
        folium.LayerControl().add_to(m2)
   

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


elif paginaSelecionada == 'Valor Empenhado':
     #st.sidebar.image(img_resized, caption='', use_column_width=True)
    caminho_do_arquivo = 'PCMG235.csv'
    df2 = pd.read_excel("nato4.xlsx")
    #f2= df2.groupby(['Município Beneficiado (Padronizado)', 'Parlamentar','Unidade Beneficiária (Padronizado)','Ação Orçamentária','Categoria (Padronizado)']).agg({
        #'Valor Total LIQUIDADO': 'sum',
        #'Código SIAD': 'first'
    #}).reset_index()
    df2 = df2[df2["Município Beneficiado (Padronizado)"] != ""]
    df2 ['Valor Total EMPENHADO'] = pd.to_numeric(df2 ['Valor Total EMPENHADO'], errors='coerce')  # 'coerce' para converter não numéricos em NaN
    df2  = df2 .dropna(subset=['Valor Total EMPENHADO'])
    df_municipios = pd.read_csv('municipios.csv')
    df_merged = pd.merge(df2, df_municipios, left_on='Município Beneficiado (Padronizado)', right_on='nome', how='inner')
    geojson_path = 'municipios.geojson.json'
    gdf = gpd.read_file(geojson_path)
    gdf["id"] = gdf["id"].astype(int)
    gdfj = gdf.merge(df_merged, left_on='id', right_on='codigo_ibge', how='inner')
    #gdfj =pd.read_csv('PCMG23.csv',sep=",")
    # Carregar a imagem

    df = pd.read_csv(caminho_do_arquivo,sep=",")
    #st.table(df.head(10))
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
        columns=['codigo_ibge', 'Valor Total EMPENHADO'],  # Use a coluna logarítmica aqui
        key_on='feature.properties.codigo_ibge',
        fill_color='YlOrRd',  # Esquema de cores (YlOrRd é um exemplo)
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Valor Total EMPENHADO'
    ).add_to(m3)

    # Adicione um controle de camadas (layers control) ao mapa
    folium.LayerControl().add_to(m3)

    show_markers22 = st.checkbox('Exibir Pontos no mapa', key='show_markers22')


    if show_markers22:
        for index, row in gdfj.iterrows():  # Corrija o erro de sintaxe na linha do loop
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=10,  # Ajuste o tamanho do marcador conforme necessário
                    popup = (
                                f'Parlamentar: {row["Parlamentar"]}, '
                                f'Valor Total Liquidado: R${round(row["Valor Total EMPENHADO"], 2)}, '
                                f'Categoria: {row["Categoria (Padronizado)"]}, '
                                f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                            ),
    # Exibe o valor da probabilidade no pop-up
                    color='blue',
                    fill=True,
                    fill_color='blue'
                ).add_to(m3)
    # Exibir a imagem redimensionada no Streamlit
    # Exibir a imagem redimensionada no Streamlit
    # Salve o mapa em um arquivo HTML
    m3.save('municipios_com_proporcao_logu.html')
    HtmlFile = open("municipios_com_proporcao_logu.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.subheader(f'Mapa de Valor Empenhado ')
    #components.html(source_code,height = 600)

    components.html(source_code,height = 600)
    # Supondo que 'df' seja o seu DataFrame original
    # Criando um novo DataFrame sem a quarta coluna
    novo_df = df.drop(df.columns[3], axis=1)

    novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('        DELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)
    novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('\tDELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)





    parlamentares_unicos = novo_df['Parlamentar'].unique()
    parlamentares_unicos_ordenados = sorted(parlamentares_unicos)
    show_markers2 = st.checkbox('Exibir mapa por Atuação de Parlamentar', key='show_markers2')
    if show_markers2:
        parlamentar_selecionado = st.selectbox('Selecione um Parlamentar', parlamentares_unicos_ordenados)
        df_parlamentar=novo_df[novo_df['Parlamentar'] == parlamentar_selecionado]
        
        
        m2 = folium.Map(location=[df_parlamentar['latitude'].mean(), df_parlamentar['longitude'].mean()], zoom_start=7)
        # Criar uma caixa de seleção com os valores únicos
        

        # Agora você pode usar a variável parlamentar_selecionado para outras operações
        # Por exemplo, mostrar dados filtrados por esse parlamentar
        # Crie a sobreposição de municípios preenchidos com base na coluna de proporção logarítmica
        folium.Choropleth(
            geo_data=gdfj,
            name='choropleth',
            data=gdfj,
            columns=['codigo_ibge', 'Valor Total EMPENHADO'],  # Use a coluna logarítmica aqui
            key_on='feature.properties.codigo_ibge',
            fill_color='YlOrRd',  # Esquema de cores (YlOrRd é um exemplo)
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Valor Total EMPENHADO'
        ).add_to(m2)

        # Adicione um checkbox para controlar a exibição dos marcadores
        
        # Substitua as coordenadas e o nível de zoom conforme necessário

        # Adicionar marcadores de círculo
        for index, row in df_parlamentar.iterrows():  # Corrija o erro de sintaxe na linha do loop
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=10,  # Ajuste o tamanho do marcador conforme necessário
                    popup = (
                                f'Parlamentar: {row["Parlamentar"]}, '
                                f'Valor Total Empenhado: R${round(row["Valor Total EMPENHADO"], 2)}, '
                                f'Categoria: {row["Categoria (Padronizado)"]}, '
                                f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                            ),
    # Exibe o valor da probabilidade no pop-up
                    color='blue',
                    fill=True,
                    fill_color='blue'
                ).add_to(m2)
        # Adicionar controle de camadas (para alternar entre as camadas)
        folium.LayerControl().add_to(m2)
   

        # Salve o mapa em um arquivo HTML no diretório do projeto
        m2.save('mapa_de_calor_interativo2p.html')
        HtmlFile = open("mapa_de_calor_interativo2p.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        st.subheader(f'Mapa de Valor Empenhado / Parlamentar {parlamentar_selecionado }')
        #components.html(source_code,height = 600)
        components.html(source_code,height = 600)
        novos_dados = df_parlamentar.iloc[:, [4, 2, 6, 8, 9, 10]]
        st.write(novos_dados)
        
        # Exiba o mapa no Streamlit
            
    else:
        st.write('Os marcadores estão desativados. Marque a caixa para mostrá-los no mapa.')
elif paginaSelecionada == 'Valor Previsto':
     #st.sidebar.image(img_resized, caption='', use_column_width=True)
    caminho_do_arquivo = 'PCMG235.csv'
    df2 = pd.read_excel("nato4.xlsx")
    #f2= df2.groupby(['Município Beneficiado (Padronizado)', 'Parlamentar','Unidade Beneficiária (Padronizado)','Ação Orçamentária','Categoria (Padronizado)']).agg({
        #'Valor Total LIQUIDADO': 'sum',
        #'Código SIAD': 'first'
    #}).reset_index()
    df2 = df2[df2["Município Beneficiado (Padronizado)"] != ""]
    df2 ['Valor total PREVISTO'] = pd.to_numeric(df2 ['Valor total PREVISTO'], errors='coerce')  # 'coerce' para converter não numéricos em NaN
    df2  = df2 .dropna(subset=['Valor total PREVISTO'])
    df_municipios = pd.read_csv('municipios.csv')
    df_merged = pd.merge(df2, df_municipios, left_on='Município Beneficiado (Padronizado)', right_on='nome', how='inner')
    geojson_path = 'municipios.geojson.json'
    gdf = gpd.read_file(geojson_path)
    gdf["id"] = gdf["id"].astype(int)
    gdfj = gdf.merge(df_merged, left_on='id', right_on='codigo_ibge', how='inner')
    #gdfj =pd.read_csv('PCMG23.csv',sep=",")
    # Carregar a imagem

    df = pd.read_csv(caminho_do_arquivo,sep=",")
    #st.table(df.head(10))
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
        columns=['codigo_ibge', 'Valor total PREVISTO'],  # Use a coluna logarítmica aqui
        key_on='feature.properties.codigo_ibge',
        fill_color='YlOrRd',  # Esquema de cores (YlOrRd é um exemplo)
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Valor total PREVISTO'
    ).add_to(m3)

    # Adicione um controle de camadas (layers control) ao mapa
    folium.LayerControl().add_to(m3)

    show_markers22 = st.checkbox('Exibir Pontos no mapa', key='show_markers22')


    if show_markers22:
        for index, row in gdfj.iterrows():  # Corrija o erro de sintaxe na linha do loop
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=10,  # Ajuste o tamanho do marcador conforme necessário
                    popup = (
                                f'Parlamentar: {row["Parlamentar"]}, '
                                f'Valor  Previsto: R${round(row["Valor total PREVISTO"], 2)}, '
                                f'Categoria: {row["Categoria (Padronizado)"]}, '
                                f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                            ),
    # Exibe o valor da probabilidade no pop-up
                    color='blue',
                    fill=True,
                    fill_color='blue'
                ).add_to(m3)
    # Exibir a imagem redimensionada no Streamlit
    # Exibir a imagem redimensionada no Streamlit
    # Salve o mapa em um arquivo HTML
    m3.save('municipios_com_proporcao_logup.html')
    HtmlFile = open("municipios_com_proporcao_logup.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.subheader(f'Mapa de Valor Previsto ')
    #components.html(source_code,height = 600)

    components.html(source_code,height = 600)
    # Supondo que 'df' seja o seu DataFrame original
    # Criando um novo DataFrame sem a quarta coluna
    novo_df = df.drop(df.columns[3], axis=1)

    novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('        DELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)
    novo_df['Parlamentar'] = novo_df['Parlamentar'].replace('\tDELEGADA SHEILA', 'DELEGADA SHEILA', regex=True)





    parlamentares_unicos = novo_df['Parlamentar'].unique()
    parlamentares_unicos_ordenados = sorted(parlamentares_unicos)
    show_markers2 = st.checkbox('Exibir mapa por Atuação de Parlamentar', key='show_markers2')
    if show_markers2:
        parlamentar_selecionado = st.selectbox('Selecione um Parlamentar', parlamentares_unicos_ordenados)
        df_parlamentar=novo_df[novo_df['Parlamentar'] == parlamentar_selecionado]
        
        
        m2 = folium.Map(location=[df_parlamentar['latitude'].mean(), df_parlamentar['longitude'].mean()], zoom_start=7)
        # Criar uma caixa de seleção com os valores únicos
        

        # Agora você pode usar a variável parlamentar_selecionado para outras operações
        # Por exemplo, mostrar dados filtrados por esse parlamentar
        # Crie a sobreposição de municípios preenchidos com base na coluna de proporção logarítmica
        folium.Choropleth(
            geo_data=gdfj,
            name='choropleth',
            data=gdfj,
            columns=['codigo_ibge', 'Valor total PREVISTO'],  # Use a coluna logarítmica aqui
            key_on='feature.properties.codigo_ibge',
            fill_color='YlOrRd',  # Esquema de cores (YlOrRd é um exemplo)
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Valor total PREVISTO'
        ).add_to(m2)

        # Adicione um checkbox para controlar a exibição dos marcadores
        
        # Substitua as coordenadas e o nível de zoom conforme necessário

        # Adicionar marcadores de círculo
        for index, row in df_parlamentar.iterrows():  # Corrija o erro de sintaxe na linha do loop
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=10,  # Ajuste o tamanho do marcador conforme necessário
                    popup = (
                                f'Parlamentar: {row["Parlamentar"]}, '
                                f'Valor Previsto: R${round(row["Valor total PREVISTO"], 2)}, '
                                f'Categoria: {row["Categoria (Padronizado)"]}, '
                                f'Unidade Beneficiária: {row["Unidade Beneficiária (Padronizado)"]}'
                            ),
    # Exibe o valor da probabilidade no pop-up
                    color='blue',
                    fill=True,
                    fill_color='blue'
                ).add_to(m2)
        # Adicionar controle de camadas (para alternar entre as camadas)
        folium.LayerControl().add_to(m2)
   

        # Salve o mapa em um arquivo HTML no diretório do projeto
        m2.save('mapa_de_calor_interativo2pt.html')
        HtmlFile = open("mapa_de_calor_interativo2pt.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        st.subheader(f'Mapa de Valor Previsto / Parlamentar {parlamentar_selecionado }')
        #components.html(source_code,height = 600)
        components.html(source_code,height = 600)
        novos_dados = df_parlamentar.iloc[:, [4, 2, 6, 8, 9, 10]]
        st.write(novos_dados)
        
        # Exiba o mapa no Streamlit
            
    else:
        st.write('Os marcadores estão desativados. Marque a caixa para mostrá-los no mapa.')
