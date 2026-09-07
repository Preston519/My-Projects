import websockets
import asyncio
import json

connections = set()

async def send_message(message):
    async with websockets.connect("wahh") as ws:
        await ws.send(message)
        
async def handler(connection: websockets.ClientConnection): # Handler for a connected client
    print("Client connected")
    connections.add(connection)
    # while True:
    #     try:
    #         message = await connection.recv()
    #     except websockets.exceptions.ConnectionClosedOK:
    #         break
    #     print(f"Received message: {message}")
    #     await connection.send(message)
    
    username = await connection.recv()
    
    async for message in connection:
        print(f"Received message: {message}")
        async with asyncio.TaskGroup() as tgroup:
            for user in connections:
                if user != connection:
                    tgroup.create_task(user.send(f"{username}: {message}"))
    connections.remove(connection)
    print("Client disconnected")

async def main():
    server = await websockets.serve(handler, "localhost", 8080)
    print("Server online")
    await server.serve_forever()
    # Replacing sleep will define server lifetime. Server closes when program terminates
    # await asyncio.sleep(30)
    print("Server offline")
    
        
if __name__ == "__main__":
    asyncio.run(main())