import os
import signal

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel

from dotenv import load_dotenv

import asyncio

load_dotenv()

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=api_key)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

conversation = None
websocket_connection = None

main_event_loop = None

@app.post("/start")
async def startup_event():
    global conversation, websocket_connection, main_event_loop
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)

    # Always create a new Conversation for each call/session
    conversation = Conversation(
        client,
        agent_id,
        requires_auth=bool(api_key),
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=send_agent_message,
        callback_agent_response_correction=send_agent_correction,
        callback_user_transcript=send_user_message,
    )
    conversation.start_session()
    return {"status": "started"}


@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("static/index.html") as f:
        return f.read()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global websocket_connection, main_event_loop
    await websocket.accept()
    websocket_connection = websocket
    main_event_loop = asyncio.get_running_loop()  # THIS IS THE FIX
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        websocket_connection = None

class TextInput(BaseModel):
    message: str

@app.post("/send_text")
async def send_text(input: TextInput):
    if websocket_connection and main_event_loop:
        asyncio.run_coroutine_threadsafe(
            websocket_connection.send_text(f"User: {input.message}"), main_event_loop
        )

# @app.post("/start")
# def start_conversation():
#     global conversation
#     if conversation:
#         conversation.start_session()
#         return {"status": "started"}
#     return {"error": "Conversation not initialized"}


@app.post("/end")
def end_conversation():
    global conversation
    if conversation:
        conversation.end_session()
        return {"status": "ended"}
    return {"error": "Conversation not initialized"}


def send_user_message(transcript):
    if websocket_connection and main_event_loop:
        asyncio.run_coroutine_threadsafe(
            websocket_connection.send_text(f"User: {transcript}"), main_event_loop
        )

def send_agent_message(response):
    if websocket_connection and main_event_loop:
        asyncio.run_coroutine_threadsafe(
            websocket_connection.send_text(f"Agent: {response}"), main_event_loop
        )

def send_agent_correction(original, corrected):
    if websocket_connection and main_event_loop:
        asyncio.run_coroutine_threadsafe(
            websocket_connection.send_text(f"Agent corrected: {original} -> {corrected}"), main_event_loop
        )

# Run app with following
# uvicorn main:app --reload --port 8134
