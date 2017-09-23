import asyncio
import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/", loop=loop)

    queue_name = "test_queue"

    # Creating channel
    channel = await connection.channel()    # type: aio_pika.Channel

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=True)   # type: aio_pika.Queue

    async for message in queue:
        with message.process():
            print(message.body)

            if queue.name in message.body.decode():
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()