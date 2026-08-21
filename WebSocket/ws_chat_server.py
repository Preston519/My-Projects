import websockets
import asyncio
import json
import time

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
    
    info = json.loads(await connection.recv())
    username = info["username"]
    colour = info["colour"]
    
    async for message in connection:
        print(f"Received message: {message}")
        timestamp = time.time()
        async with asyncio.TaskGroup() as tgroup:
            for user in connections:
                tgroup.create_task(user.send(json.dumps({"username": username, "colour": colour, "message": message, "time": timestamp})))
    connections.remove(connection)
    print("Client disconnected")

async def main():
    server = await websockets.serve(handler, "localhost", 8080)
    print("Server online")
    await server.serve_forever()
    print("Server offline")
    
        
if __name__ == "__main__":
    asyncio.run(main())