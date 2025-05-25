import psycopg2
#from fastapi import FastAPI
from dotenv import load_dotenv
import os
import pandas as pd
import geopandas as gpd
from shapely import wkt


load_dotenv()

'''
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

'''

db_settings = {
    'dbname': os.getenv('DATABASE'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST')
}

# Conectar ao banco de dados
conn = psycopg2.connect(**db_settings)

print("conectado com sucesso")

# Criar um cursor
cursor = conn.cursor()

# Consulta SQL
consulta_sql = """
    SELECT
    p.comunidades as comunidade,
    p.locais_apoio as local_apoio,
    p.endereco as sirene_adress,
    b.nome as bairro,
    ST_AsText(p.geometry) as geom_pontos,
    ST_AsText(b.geom) as geom_bairros
FROM
    pontos_de_apoio2 p
JOIN
    bairros b ON ST_Within(p.geometry, b.geom)
WHERE
    b.nome <> 'Centro' and  b.nome <> 'Sepetiba';
"""

# Executar a consulta
cursor.execute(consulta_sql)

# Recuperar os resultados
resultados = cursor.fetchall()

# Fechar a conexão
cursor.close()
conn.close()

# Criar um DataFrame do Pandas com os resultados
df = pd.DataFrame(resultados, columns=['Comunidade', 'Local de Apoio', 'Endereço', 'Bairro', 'GeomPontos', 'GeomBairros'])

print('Dataframe criado com sucesso')

print(df)

# Converter as colunas de geometria de WKT para objetos shapely
df['GeomPontos'] = df['GeomPontos'].apply(wkt.loads)
df['GeomBairros'] = df['GeomBairros'].apply(wkt.loads)

# Criar GeoDataFrames
gdf_pontos = gpd.GeoDataFrame(df, geometry='GeomPontos')
gdf_bairros = gpd.GeoDataFrame(df, geometry='GeomBairros')

# Definir o sistema de coordenadas (se conhecido, por exemplo, EPSG:4326)
gdf_pontos.set_crs(epsg=4326, inplace=True)
gdf_bairros.set_crs(epsg=4326, inplace=True)

# Exportar os GeoDataFrames para arquivos GeoJSON
gdf_pontos.to_file('pontos_de_apoio.geojson', driver='GeoJSON')
gdf_bairros.to_file('bairros.geojson', driver='GeoJSON')

print("GeoDataFrames exportados para GeoJSON com sucesso")