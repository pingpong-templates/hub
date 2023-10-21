# elastic-query-generator

We can use LLMs to interact with Elasticsearch analytics databases in natural language.

This chain builds search queries via the Elasticsearch DSL API (filters and aggregations).

The Elasticsearch client must have permissions for index listing, mapping description and search queries.



## Setup

See [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) for instructions on how to run Elasticsearch locally.

In addition to the instructions there, you will want to run

> export ELASTIC_SEARCH_SERVER="https://elastic:pass@localhost:9200"

Note that if you already have an Elastic cluster running you can just replace the code to call out to that.

If you want to populate the DB with some example info, you can run `python ingest.py`.
