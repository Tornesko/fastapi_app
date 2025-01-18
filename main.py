from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.database import database, init_db
from app.routes.user_routes import router as user_router
from app.routes.product_routes import router as product_router
from app.websocket_manager import websocket_manager

app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(product_router, prefix="/api")


@app.websocket("/admin")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


@app.on_event("startup")
async def startup():
    init_db()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
