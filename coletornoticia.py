import feedparser
from sites import FEED


def coletar_noticias():
    noticias = []
    for feed_info in FEED:
        print(f"Coletando de {feed_info['fonte']}...")
        d = feedparser.parse(feed_info['url'])
        for entry in d.entries[:5]:
            categoria = None
            if entry.get('tags'):
                categoria = entry.tags[0].get('term')
            item = {
                'fonte': feed_info['fonte'],
                'titulo': entry.get('title', ''),
                'resumo': entry.get('summary', entry.get('description', '')),
                'data': entry.get('published', ''),
                'url': entry.get('link', ''),
                'categoria': categoria
            }
            noticias.append(item)
    return noticias
