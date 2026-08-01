import asyncio
import websockets
import json
import threading

# USERNAME = "Peter"

async def main():
    async with websockets.connect("ws://localhost:8080") as client:
        # await client.send(USERNAME)
        # message = await asyncio.to_thread(input, f"{USERNAME}: ")
        # if message.strip():
        #     await client.send(message)
        loop = asyncio.get_running_loop()
        await client.send(input("Enter username: "))
        send_thread = threading.Thread(target=send_message, args=(loop, client), daemon=True)
        send_thread.start()
        async with asyncio.TaskGroup() as group:
            # group.create_task(send_message(client))
            group.create_task(read_messages(client))
    print("----------------------------------------------------------")
    print()
    print("Connection closed")

def send_message(loop, client):
    while True:
        # message = input(f"{USERNAME}: ")
        message = input()
        if message.strip():
            asyncio.run_coroutine_threadsafe(client.send(message), loop)
            
async def read_messages(client):
    async for message in client:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())