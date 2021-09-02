from fastapi import FastAPI
from starlette.websockets import WebSocket
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
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# 接続中のクライアントを識別するためのIDを格納
clientstab = {}

class WSClient:
    clients = {}
    def register(self, key: str, ws: WebSocket):
        self.clients[key] = ws

        logger.info("registered: %s", key)
        logger.info("test")

    def all(self) -> list:
        return list(self.clients.values())

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    wsc = WSClient()
    key = ws.headers.get('sec-websocket-key')
    wsc.register(key, ws)
    logging.info("registered")
    try:
        while True:
            data = await ws.receive_text()
            logging.info("received %s", data)
            for client in wsc.all():
                await client.send_text(f"ID: {key} | Message: {data}")
    except:
       await ws.close()
