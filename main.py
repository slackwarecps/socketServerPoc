import asyncio
import websockets
import json
import time

# Dados da mensagem JSON
mensagem_json = {
    "e": "trade",
    "E": 1722766102790,
    "s": "BTCUSDT",
    "t": 3718209179,
    "p": "60610.00000000",
    "q": "0.00154000",
    "T": 1722766102789,
    "m": True,
    "M": True
}

async def hello(websocket):
    while True:
        await websocket.send(json.dumps(mensagem_json))
        await asyncio.sleep(2)

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
