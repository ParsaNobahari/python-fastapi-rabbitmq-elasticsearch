from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(['http://elastic:q7+ynUZu*iU=22jLcDrf@localhost:9200'])

# Define search query
query = {
    "query": {
        "match_all": {}
    }
}

# Search for documents in Elasticsearch
result = es.search(index='my_index', body=query)

# Print the retrieved documents
for hit in result['hits']['hits']:
    print(hit['_source'])
