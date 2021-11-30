import asyncio
import datetime

import websockets


async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        recv_text = await websocket.recv()
        print(recv_text)


asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:8765'))
