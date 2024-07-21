import asyncio
import csv
from time import time
import elasticsearch_dsl as dsl
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


async def ingest_quotes():
    # TODO!
    pass


async def search_quotes(q, tags, use_knn=True, start=0, size=25):
    # TODO!
    return [], [], 0


if __name__ == '__main__':
    asyncio.run(ingest_quotes())
