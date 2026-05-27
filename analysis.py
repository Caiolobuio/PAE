import openai

api_key = ''
def analise(df):
    client = openai.OpenAI(api_key=api_key)
    
    colunas = ['fonte', 'titulo', 'resumo', 'data', 'url']
    colunas_presentes = [col for col in colunas if col in df.columns]
    conteudo = df[colunas_presentes].to_csv(index=False, sep=';')
    
    prompt = f"""Analise economicamente as seguintes notícias recentes coletadas de fontes brasileiras:\n\n{conteudo}\n\nForneça uma análise profissional e resumida dos principais temas econômicos, tendências e impactos potenciais. Responda em português brasileiro."""
    
    system_prompt = """Você é um analista econômico sênior com mais de 20 anos de experiência nos mercados financeiros brasileiro e internacional. 
Possui profundo conhecimento em macroeconomia, política monetária, mercado de capitais, câmbio, inflação e conjuntura econômica brasileira. 
Suas análises são reconhecidas pela profundidade, rigor técnico e capacidade de identificar conexões entre eventos aparentemente isolados, 
antecipando tendências e impactos de curto, médio e longo prazo. Você sempre fundamenta suas conclusões em dados, contexto histórico e 
frameworks econômicos consolidados, entregando insights acionáveis, de alto valor para tomadores de decisão e gere o resultado exclusivamente em markdown."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        analise = response.choices[0].message.content
        print("\nAnálise econômica gerada pela OpenAI:")
        print(analise)
    except Exception as e:
        print(f"Erro na API OpenAI: {e}")
        print("Verifique a chave API e instale 'pip install openai feedparser pandas'.")
    return analise
