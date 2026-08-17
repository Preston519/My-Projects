import websockets
import asyncio

async def handler(connection: websockets.ClientConnection):
    print("Client connected")
    async for message in connection:
        print(f"Message: {message}")
        await connection.send(message)
    print("Client disconnected")

async def main():
    server = await websockets.serve(handler, 'localhost', 8080)
    print("Server online")
    await server.serve_forever()
    print("Server offline")
    
if __name__ == "__main__":
    asyncio.run(main())