from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from g4f.client import Client

client = Client()

def ask_gpt(messages: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4", #gpt-3.5-turbo
        messages=[{"role": "user", "content": messages}])
    return response.choices[0].message.content


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You: {data}", websocket)
            await manager.send_personal_message(f"Assistent: {ask_gpt(data)}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
