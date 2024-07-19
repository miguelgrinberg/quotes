import asyncio
import csv
from time import time
import elasticsearch_dsl as dsl
from sentence_transformers import SentenceTransformer

dsl.async_connections.create_connection(hosts='http://localhost:9200')
model = SentenceTransformer("all-MiniLM-L6-v2")


class QuoteDoc(dsl.AsyncDocument):
    quote: str
    author: str = dsl.mapped_field(dsl.Keyword())
    tags: list[str] = dsl.mapped_field(dsl.Keyword())
    embedding: list[float] = dsl.mapped_field(dsl.DenseVector(), init=False)

    class Index:
        name = "quotes"

    def clean(self):
        if not self.embedding:
            self.embedding = model.encode(self.quote).tolist()


async def ingest_quotes():
    if await QuoteDoc._index.exists():
        await QuoteDoc._index.delete()
    await QuoteDoc.init()

    async def get_next_quote_internal():
        start = time()
        with open('quotes.csv') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                yield QuoteDoc(quote=row['quote'], author=row['author'], tags=row['tags'].split(','))
                count += 1
                if count % 100 == 0:
                    elapsed = time() - start
                    print(f"Indexed {count} quotes ({count / elapsed:.2f}/s)")
            print(f"Indexed {count} quotes")

    async def get_next_quote():
        quotes = []
        async for quote in get_next_quote_internal():
            quotes.append(quote)
            if len(quotes) == 512:
                embeddings = model.encode([quote.quote for quote in quotes])
                for _quote, embedding in zip(quotes, embeddings):
                    _quote.embedding = embedding.tolist()
                    yield _quote
                quotes = []
        if len(quotes) > 0:
            embeddings = model.encode([quote.quote for quote in quotes])
            for _quote, embedding in zip(quotes, embeddings):
                _quote.embedding = embedding.tolist()
                yield _quote

    await QuoteDoc.bulk(get_next_quote())


async def search_quotes(q: str, tags: list[str], use_knn: bool=True, start: int=0, size: int=25):
    s = QuoteDoc.search()[start:start + size]
    if not q:
        s = s.query('match_all')
    elif use_knn:
        s = s.query('knn', field='embedding', query_vector=model.encode(q).tolist())
    else:
        s = s.query('match', quote=q)
    if tags:
        s = s.filter('terms', tags=tags)
    s.aggs.bucket('tags', 'terms', field='tags', size=100)
    response = await s.execute()
    results = list(response)
    buckets = [[tag.key, tag.doc_count] for tag in response.aggs.tags.buckets]
    return results, buckets


if __name__ == '__main__':
    asyncio.run(ingest_quotes())
