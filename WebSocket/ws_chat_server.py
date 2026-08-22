import websockets
import asyncio
import json
import time
import csv

connections = set()

async def send_message(message):
    async with websockets.connect("wahh") as ws:
        await ws.send(message)
        
async def handler(connection: websockets.ClientConnection): # Handler for a connected client
    print("Client connected")
    connections.add(connection)
    
    info = json.loads(await connection.recv())
    username = info["username"]
    colour = info["colour"]
    with open("chat-history/chat.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            await connection.send(json.dumps(row))

    filename = "chat-history/chat.csv"
    async for message in connection:
        print(f"Received message: {message}")
        timestamp = int(time.time())
        with open(filename, "a", newline='') as file:
            csv.writer(file, quoting=csv.QUOTE_MINIMAL).writerow([username, colour, message, timestamp])
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