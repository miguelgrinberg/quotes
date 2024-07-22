# Quotes
Quotes database with vector search, implemented with Elasticsearch, FastAPI and
React.

![Quotes app screenshot](screenshot.png)

## What is this?

This repository contains a small application that demonstrates how easy it is
to set up a vector database using [Elasticsearch](https://www.elastic.co/elasticsearch)
and the [Elasticsearch-DSL](https://elasticsearch-dsl.readthedocs.io/) client
for Python.

The application includes a FastAPI back end and a React front end written in
TypeScript. The quotes are stored in an Elasticsearch index, and for each quote
an embedding is generated using the
[all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
Sentence Transformers model.

The dataset used by this application has about 37,000 famous quotes, each with
their author and tags. The data originates from a
[Kaggle dataset](https://www.kaggle.com/datasets/akmittal/quotes-dataset).

## Requirements

Please make sure you have the following installed:

- Python 3.8 or newer
- Node.js 18 or newer
- Docker

## How To Run

Follow these steps to install this demo on your computer:

### Clone this repository

```bash
git clone https://github.com/miguelgrinberg/quotes
cd quotes
```

### Install the Node and Python dependencies

```bash
npm install
```

### Start a development Elasticsearch container

```bash
docker run -p 9200:9200 -d --name elasticsearch \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.security.http.ssl.enabled=false" \
  -e "xpack.license.self_generated.type=basic" \
  -v "./data:/usr/share/elasticsearch/data" \
  docker.elastic.co/elasticsearch/elasticsearch:8.14.2
```

### Create the quotes database

```bash
npm run ingest
```

Note that depending on your computer speed and wether you have a GPU or not this
may take a few minutes.

### Start the back end

```bash
npm run backend
```

### Open a second terminal window and start the front end

```bash
npm start
```

You can now navigate to `http://localhost:3000` on your web browser to access
the application.
