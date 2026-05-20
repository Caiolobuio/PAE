import feedparser
import pandas as pd
import openai
from coletornoticia import coletar_noticias



print("Coletando notícias dos feeds RSS...")
noticias_lista = coletar_noticias()
df = pd.DataFrame(noticias_lista)
if not df.empty:
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df = df.sort_values('data', ascending=False).reset_index(drop=True)
    print("\nPrimeiras notícias:")
    print(df[['fonte', 'titulo', 'data', 'url']].head(10).to_string(index=False))
    print("\nContagem por fonte:")
    print(df['fonte'].value_counts())
    print("\nContagem por data (top 5):")
    print(df['data'].dt.date.value_counts().head())
    # OpenAI
    api_key = ""
    client = openai.OpenAI(api_key=api_key)
    conteudo = df.to_csv(index=False, sep=';')
    prompt = f"""Analise economicamente as seguintes notícias recentes coletadas de fontes brasileiras:\n\n{conteudo}\n\nForneça uma análise profissional e resumida dos principais temas econômicos, tendências e impactos potenciais. Responda em português brasileiro."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        analise = response.choices[0].message.content
        print("\nAnálise econômica gerada pela OpenAI:")
        print(analise)
    except Exception as e:
        print(f"Erro na API OpenAI: {e}")
        print("Verifique a chave API e instale 'pip install openai feedparser pandas'.")
else:
    print("Nenhuma notícia coletada.")



