import json
import asyncio
import aio_pika


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:
        routing_key = "test_queue"

        with open('data.json', 'r') as f:
            data = json.load(f)
            body = json.dumps(data).encode()

        channel = await connection.channel()

        print(body.decode())

        await channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=routing_key,
        )


if __name__ == "__main__":
    asyncio.run(main())
