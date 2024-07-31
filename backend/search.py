import asyncio
import csv
from time import time
import elasticsearch_dsl as dsl
from elasticsearch import OrjsonSerializer
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
dsl.async_connections.create_connection(hosts=['http://localhost:9200']) #, serializer=OrjsonSerializer())


class QuoteDoc(dsl.AsyncDocument):
    quote: str
    author: str = dsl.mapped_field(dsl.Keyword())
    tags: list[str] = dsl.mapped_field(dsl.Keyword())
    embedding: list[float] = dsl.mapped_field(dsl.DenseVector(), init=False)

    class Index:
        name = 'quotes'

    def clean(self):
        if not self.embedding:
            self.embedding = model.encode(self.quote).tolist()


def ingest_progress(count, start):
    elapsed = time() - start
    print(f'\rIngested {count} quotes. ({count / elapsed:.0f}/sec)', end='')


def embed_quotes(quotes):
    embeddings = model.encode([q.quote for q in quotes])
    for q, e in zip(quotes, embeddings):
        q.embedding = e.tolist()


async def ingest_quotes():
    if await QuoteDoc._index.exists():
        await QuoteDoc._index.delete()
    await QuoteDoc.init()

    async def get_next_quote():
        quotes = []
        with open('quotes.csv') as f:
            reader = csv.DictReader(f)
            count = 0
            start = time()
            for row in reader:
                q = QuoteDoc(quote=row['quote'], author=row['author'],
                             tags=row['tags'].split(','))
                quotes.append(q)
                if len(quotes) == 512:
                    embed_quotes(quotes)
                    for q in quotes:
                        yield q
                    count += len(quotes)
                    ingest_progress(count, start)
                    quotes = []
            if len(quotes) > 0:
                embed_quotes(quotes)
                for q in quotes:
                    yield q
                ingest_progress(count, start)

    await QuoteDoc.bulk(get_next_quote())


async def search_quotes(q, tags, use_knn=True, start=0, size=25):
    s = QuoteDoc.search()
    if q == '':
        s = s.query(dsl.query.MatchAll())
    elif use_knn:
        s = s.query(dsl.query.Knn(field=QuoteDoc.embedding, query_vector=model.encode(q).tolist()))
    else:
        s = s.query(dsl.query.Match(quote=q))
    for tag in tags:
        s = s.filter(dsl.query.Terms(tags=[tag]))
    s.aggs.bucket('tags', dsl.aggs.Terms(field=QuoteDoc.tags, size=100))
    r = await s[start:start + size].execute()
    tags = [(tag.key, tag.doc_count) for tag in r.aggs.tags.buckets]
    return r.hits, tags, r['hits'].total.value


if __name__ == '__main__':
    asyncio.run(ingest_quotes())
