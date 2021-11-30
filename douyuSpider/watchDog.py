import asyncio
import datetime

import websockets


async def echo(websocket):
    async for message in websocket:
        print(message)
        # if(datetime.datetime.now()-message).seconds>10:
        #     with open('main.py',encoding='utf-8') as f:
        #         exec(f.read())


asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
