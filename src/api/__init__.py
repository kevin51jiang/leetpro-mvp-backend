"""
Main API module for the LeetPro application.

This module sets up the Quart application, defines routes, and handles API requests.
"""

import os
from datetime import datetime
from dataclasses import dataclass

from dotenv import load_dotenv
import uvicorn
from quart import Quart, Response, send_from_directory
from quart_cors import cors
from quart_schema import QuartSchema, DataSource, validate_request, validate_response
from quart_schema.pydantic import File

from api.stt import transcribe_audio, write_speech_file
from api.tts import generate_tts
from api.txt2txt import get_txt2txt_completion
from api.conversation import save_conversation, get_conversation_analysis
from api.models import (
    Conversation,
    ConversationOverallAnalysis,
)
from api.utils import generate_uuid


load_dotenv()

app = Quart(__name__)
app = cors(
    app,
    allow_origin=[
        "*",
        # "https://app.tryleetpro.com",
        # "https://tryleetpro.com",
        # "https://leetpro-mvp.netlify.app",
        # "http://localhost:5173",
        # "http://127.0.0.1:5173",
    ],
)
QuartSchema(app)

# Route definitions


@app.route("/vo/<vo_id>.wav")
async def vo(vo_id: str):
    """Serve voice output files."""
    return await send_from_directory("public/vo", f"{vo_id}.wav")


@app.route("/speech_in/<speech_file_id>.wav")
async def speech_in(speech_file_id: str):
    """Serve speech input files."""
    return await send_from_directory("public/speech_in", f"{speech_file_id}.wav")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return Response("OK", status=200)


# Data models for request/response validation


@dataclass
class TranscribeInput:
    file: File


@dataclass
class TranscribeOutput:
    text: str


@dataclass
class ChatInput:
    conversation: Conversation


@dataclass
class ChatOutput:
    content: str
    vo_id: str
    timestamp: datetime
    id: str


@dataclass
class SaveChatInput:
    conversation: Conversation


@dataclass
class SaveChatOutput:
    conversation_id: str


# API endpoints


@app.post("/transcribe")
@validate_request(TranscribeInput, source=DataSource.FORM_MULTIPART)
@validate_response(TranscribeOutput)
async def transcribe(data: TranscribeInput) -> TranscribeOutput:
    """Transcribe audio file to text."""
    if data.file.content_type != "audio/wav":
        return Response("audio/wav is required", status=415)
    if data.file.content_length > 10 * 1024 * 1024:  # 10 MB
        return Response("file too large", status=413)

    speech_file_id = await write_speech_file(data.file)
    text = await transcribe_audio(speech_file_id)
    return TranscribeOutput(text=text)


@app.post("/chat")
@validate_request(ChatInput)
@validate_response(ChatOutput)
async def chat(data: ChatInput) -> ChatOutput:
    """Process chat input and generate response."""
    
    messages = [
        {"role": msg.role, "content": msg.content} for msg in data.conversation.messages
    ]
    res = await get_txt2txt_completion(messages)

    vo_id = generate_uuid()
    if not res or res == "":
        return ChatOutput(content="", vo_id="", timestamp=datetime.now(), id='')

    await generate_tts(speaker="joy", text=res, id=vo_id)


    return ChatOutput(
        content=res,
        vo_id=f"vo/{vo_id}.wav",
        timestamp=datetime.now(),
        id=vo_id,
    )


@app.post("/chat/save")
@validate_request(SaveChatInput)
@validate_response(SaveChatOutput)
async def save_chat(data: SaveChatInput) -> SaveChatOutput:
    """Save chat conversation."""
    conversation_id = await save_conversation(data.conversation)
    return SaveChatOutput(conversation_id=conversation_id)


@app.get("/analysis/<conversation_id>")
async def analyze_conversation(conversation_id: str) -> ConversationOverallAnalysis:
    """Analyze a saved conversation."""

    overall_analysis = await get_conversation_analysis(conversation_id)

    if not overall_analysis:
        return Response("Conversation not found", status=404)

    return overall_analysis


# Application entry point


def run() -> None:
    """Run the Quart application."""
    app.run()


# async def run_prod() -> None:
#     """Run the Quart application in production mode."""
#     config = uvicorn.Config("main:app", port=5000, log_level="info")
#     server = uvicorn.Server(config)
#     await server.serve()


# if __name__ == "__main__":
#     config = uvicorn.Config("src.api:app", port=5000, log_level="info")
#     server = uvicorn.Server(config)
#     server.run()
