# python-fastapi-rabbitmq-elasticsearch

## Usage

### Create a Local Elasticsearch Cluster

The easiest way to run Elasticsearch locally is by using docker.
Open a terminal and run this code to start a single-node ES cluster you can use for local development:

```
docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0
```

### Using The DockerFile from Elasticsearch Official Website(recommended)

#### Build The Docker Image

```
docker build -t my-es-image .
```
#### Running The Docker Image

```
docker run --rm -it my-es-image /bin/bash
```

> Note: When running with logging to stdout/stderr Docker stores the log in a json file, and it is recommended to specify a max size for the log file to rotate, and a max number of files to keep. E.g. --log-opt max-size=50m --log-opt max-file=10

#### Running the Build file

```
docker run --rm -p 9200:9200 my-es-image
```

