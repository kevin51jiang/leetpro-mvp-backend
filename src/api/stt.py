import os
import aiofiles
from quart_schema.pydantic import File
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from uuid_extensions import uuid7str
from dotenv import load_dotenv

load_dotenv()

deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")
deepgram_client = DeepgramClient(deepgram_api_key)

deepgram_options = PrerecordedOptions(
    model="nova-2",
    language="en",
    filler_words=True,
    smart_format=True,
)


async def write_speech_file(audio_file: File) -> str:
    speech_file_id = uuid7str()
    await audio_file.save(f"public/speech_in/{speech_file_id}.wav")
    return speech_file_id


async def transcribe_audio(speech_file_id: str) -> str:
    async with aiofiles.open(f"public/speech_in/{speech_file_id}.wav", "rb") as file:
        buffer_data = await file.read()

    payload: FileSource = {"buffer": buffer_data}

    res = await deepgram_client.listen.asyncrest.v("1").transcribe_file(
        payload,
        options=deepgram_options,
    )

    # print("transcription res ", res)

    return res.results.channels[0].alternatives[0].transcript
