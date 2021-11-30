import asyncio
import datetime

import websockets


async def echo(websocket):
    async for message in websocket:
        time = datetime.datetime.strptime(message,'%Y/%m/%d %H:%M:%S')

        message = "I got your message: {}".format(message)
        await websocket.send(message)
        print(datetime.datetime.now())

        while (datetime.datetime.now() - time).seconds > 10:
            with open('main.py',encoding='utf-8') as f:
                exec(f.read())

asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
