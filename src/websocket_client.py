import asyncio
import websockets
import json

async def listen():
    uri = "ws://127.0.0.1:5011/gs-guide-websocket"
    # uri = "http://192.168.1.104:5011/gs-guide-websocket"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received message: {data}")

asyncio.get_event_loop().run_until_complete(listen())