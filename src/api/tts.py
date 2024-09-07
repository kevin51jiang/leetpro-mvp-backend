import base64
import httpx
import os
from typing import Literal
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import aiofiles

load_dotenv()

VoiceName = Literal["tanya", "ana", "joy", "brittany", "tyler"]

tts_base_url = "https://users.rime.ai/v1/rime-tts"
RIME_API_KEY = os.environ.get("RIME_API_KEY")

deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")
deepgram_client = DeepgramClient(deepgram_api_key)


async def generate_tts_rime(
    speaker: str = "tanya",
    text: str = "",
    id: str = "",
    model_id: str = "mist",
    audio_format: str = "mp3",
    sampling_rate: int = 22050,
    speed_alpha: float = 1.0,
    reduce_latency: bool = False,
) -> None:
    """
    Generate text-to-speech audio using the Rime API.

    Args:
        speaker (str): The voice to use for TTS. Default is "tanya".
        text (str): The text to convert to speech.
        id (str): Unique identifier for the generated audio file.
        model_id (str): The model to use for TTS. Default is "mist".
        audio_format (str): The format of the output audio. Default is "mp3".
        sampling_rate (int): The sampling rate of the output audio. Default is 22050.
        speed_alpha (float): The speed of the speech. Default is 1.0.
        reduce_latency (bool): Whether to reduce latency. Default is False.

    Raises:
        ValueError: If the normalized text exceeds 1000 characters.
    """
    payload = {
        "speaker": speaker,
        "text": text.replace("\n", " "),
        "modelId": model_id,
        "audioFormat": audio_format,
        "samplingRate": sampling_rate,
        "speedAlpha": speed_alpha,
        "reduceLatency": reduce_latency,
    }

    MAX_LEN = 1000
    if len(payload["text"]) > MAX_LEN:
        raise ValueError(
            f"Normalized text is too long. Max length is {MAX_LEN} characters"
        )

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {RIME_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(tts_base_url, json=payload, headers=headers)
            response.raise_for_status()

            ascii_mp3 = response.json()
            audio_content = ascii_mp3["audioContent"]
            audio_bytes = base64.b64decode(audio_content)

            await write_audio(id=id, audio=audio_bytes)
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


async def generate_tts_deepgram(
    speaker: str = "aura-asteria-en",
    text: str = "",
    id: str = "",
):
    """
    Generate text-to-speech audio using the Deepgram API.

    Args:
        speaker (str): The voice to use for TTS. Default is "aura-asteria-en".
        text (str): The text to convert to speech.
        id (str): Unique identifier for the generated audio file.

    Raises:
        ValueError: If the text is empty.
    """
    if not text:
        raise ValueError("Text is required")

    try:
        deepgram_options = SpeakOptions(model=speaker, encoding="linear16")
        payload = {"text": text}
        res = await deepgram_client.speak.asyncrest.v("1").stream_memory(
            payload,
            options=deepgram_options,
        )
        await write_audio(id=id, audio=res.stream_memory.getbuffer())
    except Exception as e:
        print(f"An error occurred: {e}")


async def write_audio(id: str, audio: bytes) -> None:
    """
    Write audio data to a file.

    Args:
        id (str): Unique identifier for the audio file.
        audio (bytes): The audio data to write.
    """
    async with aiofiles.open(f"public/vo/{id}.wav", "wb") as out:
        await out.write(audio)
        await out.flush()


def clean_tts_text(text: str) -> str:
    """
    Clean the input text for TTS processing.

    Args:
        text (str): The input text to clean.

    Returns:
        str: The cleaned text.
    """
    return text.replace("*", " ").replace("~", " ").replace("\n", "...")


async def generate_tts(speaker: str, text: str, id: str) -> None:
    """
    Generate text-to-speech audio.

    Args:
        speaker (str): The voice to use for TTS.
        text (str): The text to convert to speech.
        id (str): Unique identifier for the generated audio file.
    """
    # await generate_tts_rime(speaker=speaker, text=clean_tts_text(text), id=id)
    await generate_tts_deepgram(text=clean_tts_text(text), id=id)
