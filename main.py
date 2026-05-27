import feedparser
import pandas as pd
import openai
from coletornoticia import coletar_noticias
from analysis import analise
from gerar_interface import gerar_interface


print("Coletando notícias dos feeds RSS...")
noticias_lista = coletar_noticias()
df = pd.DataFrame(noticias_lista)

resultado = analise(df)
if not df.empty:
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df = df.sort_values('data', ascending=False).reset_index(drop=True)

    print("\nPrimeiras notícias:")
    print(df[['fonte', 'titulo', 'data', 'url']].head(10).to_string(index=False))

    print("\nContagem por fonte:")
    print(df['fonte'].value_counts())

    print("\nContagem por data (top 5):")
    print(df['data'].dt.date.value_counts().head())

    if resultado:
        gerar_interface(resultado, titulo="Análise Econômica")
   
print(resultado)


