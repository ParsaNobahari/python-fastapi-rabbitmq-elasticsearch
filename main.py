import os
import sys
import asyncio
import aio_pika
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch

num_of_async_processing_messages = 10

app = FastAPI()

es = AsyncElasticsearch(hosts="elastic:q7+ynUZu*iU=22jLcDrf@localhost:9200/")


@app.post('/search')
async def search(query: str):
    s = AsyncElasticsearch(
        using=es, index='my_index').query('match', name=query)
    response = await s.execute()
    return response.to_dict()


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        data = message.body.decode()
        # json_data = json.loads(data) # leftover code
        await es.index(
            index='my_index', doc_type='_doc', document=data)
        print("received new data:\n" + data)


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    queue_name = "test_queue"
    async with connection:

        # Creating channel
        channel = await connection.channel()

        # Maximum message count which will be processing at the same time.
        await channel.set_qos(prefetch_count=num_of_async_processing_messages)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=False)
        await queue.consume(process_message)

        print('[*] Waiting for messages. To exit press CTRL+C')

        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await connection.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
