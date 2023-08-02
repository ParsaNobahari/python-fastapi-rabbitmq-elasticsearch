#  import json
#  from fastapi import FastAPI
#  from elasticsearch_dsl import Search
#  from elasticsearch import AsyncElasticsearch
#
#  app = FastAPI()
#
#  es = AsyncElasticsearch(
#      "https://localhost:9000",
#  )
#
#
#  @app.post('/search')
#  async def search(query: str):
#      s = Search(using=es, index='my_index').query('match', name=query)
#      response = await s.execute()
#      return response.to_dict()
import os
import sys
import asyncio
import aio_pika

num_of_async_proccesing_messages = 10


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    queue_name = "test_queue"

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=num_of_async_proccesing_messages)

        queue = await channel.declare_queue(queue_name, auto_delete=False)

        async with queue.iterator() as queue_iter:
            print(' [*] Waiting for messages. To exit press CTRL+C')
            async for message in queue_iter:
                async with message.process():
                    print(message.body.decode())

                    if queue.name in message.body.decode():
                        break


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
