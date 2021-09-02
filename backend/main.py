from fastapi import FastAPI
from starlette.websockets import WebSocket
from db import database


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# 接続中のクライアントを識別するためのIDを格納
clientstab = {}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    key = ws.headers.get('sec-websocket-key')
    from clients.schemas import ClientCreate
    from clients.models import clients
    c = ClientCreate(key=key)
    await database.execute(clients.insert(), c.dict())
    clientstab[key] = ws
    try:
        while True:
            data = await ws.receive_text()
            for client in clientstab.values():
                await client.send_text(f"ID: {key} | Message: {data}")
    except:
        await ws.close()
        del clientstab[key]
