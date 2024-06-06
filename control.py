


import asyncio
import websockets


WS = "ws://stream.trailcam.link:8080/websocket"


async def hello():
    uri = WS
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(hello())