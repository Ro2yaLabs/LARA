from lara import Lara
from lara import load_and_embedd
from lara import encode
from lara import create_memory
from lara import Args

from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import StreamingResponse
from starlette.websockets import WebSocketDisconnect
from contextlib import asynccontextmanager
from schema import Message
import shutil
import yaml
import hashlib
from typing import List
import base64
import os

lara = Lara()
args = Args()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_text(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    def encode_audio(self, audio_bytes):
        return base64.b64encode(audio_bytes).decode('utf-8')


@asynccontextmanager
async def lifespan(app: FastAPI):
    embeddings = encode(
        args.model_id['multilingual-e5-base'], device=args.device, use_open_ai=False)
    memory = create_memory(args.k)
    config = yaml.load(open('configs/config.default.yaml',
                       'r'), Loader=yaml.FullLoader)

    lara.g_vars['embedding'] = embeddings
    lara.g_vars['dp'] = ''
    lara.g_vars['memory'] = memory
    lara.g_vars['config'] = config
    yield
    lara.g_vars.clear()


app = FastAPI(lifespan=lifespan)
connection_manager = ConnectionManager()


@app.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    """ Create embedding of the uploaded book

    :param file: the uploaded file (.docs, .pdf)
    """

    books_folder = "books"
    if not os.path.exists(books_folder):
        os.makedirs(books_folder)

    file_location = f"books/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    name = file.filename

    hash = hashlib.sha1(name.encode("UTF-8")).hexdigest()

    lara.g_vars['dp'] = load_and_embedd(
        file_location, lara.g_vars['embedding'], hash, is_json=True)

    return {"filename": file.filename, "location": file_location}


@app.post("/text")
async def message(message: Message):

    return StreamingResponse(lara.stream_text(message.message), media_type="text/plain")


@app.post("/audio")
async def message(message: Message):

    return StreamingResponse(lara.stream_audio(message.message), media_type="text/mpeg")


@app.websocket("/socket_audio")
async def message(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_content = data.split(":", 1)[1][:-1]
            async for audio_data in lara.stream_text_audio_ws(message_content):
                await websocket.send_bytes(audio_data)

            await websocket.send_text("".join(lara.memo))
            lara.memo = []

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
