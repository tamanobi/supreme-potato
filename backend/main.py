from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from db import database

import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

app = FastAPI()

@app.on_event("startup")
async def startup():
    logger.info("startup")
    return
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    logger.info("shutdown")
    return
    await database.disconnect()

# 接続中のクライアントを識別するためのIDを格納
clientstab = {}

class WSClient:
    clients = {}
    def register(self, key: str, ws: WebSocket):
        self.clients[key] = ws
        logger.info("registered: %s", key)

    def unregister(self, key: str):
        self.clients.pop(key)
        logger.info("unregistered: %s", key)

    def all(self) -> list:
        return list(self.clients.values())

    async def broadcast(self, message: str):
        for client in self.all():
            await client.send_text(message)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    wsc = WSClient()
    key = ws.headers.get('sec-websocket-key')
    wsc.register(key, ws)
    await wsc.broadcast(f"join {key}")

    try:
        while True:
            data_string = await ws.receive_text()
            import json
            try:
                data = json.loads(data_string)
            except Exception as e:
                logger.exception(e)
                continue
            logger.info("received %s", data)
            for client in wsc.all():
                await client.send_text(f"ID: {key} | Message: {data}")
    except WebSocketDisconnect as e:
       await ws.close()
       wsc.unregister(key)
    except Exception as e:
       logger.exception(e)
       await ws.close()
       wsc.unregister(key)
