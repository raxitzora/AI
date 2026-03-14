from openai import OpenAI
from google import genai
from google.genai import types
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
import asyncio
import os

# -------------------------
# API KEY
# -------------------------
GOOGLE_API_KEY = "PASTE_YOUR_GEMINI_KEY_HERE"

# -------------------------
# Gemini Chat (OpenAI style)
# -------------------------
client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------
# Gemini TTS
# -------------------------
tts_client = genai.Client(api_key=GOOGLE_API_KEY)


# -------------------------
# Play Gemini audio
# -------------------------
async def speak(text):

    response = tts_client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            )
        )
    )

    pcm = response.candidates[0].content.parts[0].inline_data.data

    audio = np.frombuffer(pcm, dtype=np.int16)

    sd.play(audio, samplerate=24000)
    sd.wait()


# -------------------------
# Record microphone
# -------------------------
def record_audio():

    duration = 5
    samplerate = 16000

    print("Listening...")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write("input.wav", samplerate, recording)


# -------------------------
# Speech → text
# -------------------------
def listen():

    record_audio()

    r = sr.Recognizer()

    with sr.AudioFile("input.wav") as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text

    except Exception:
        print("Didn't catch that.")
        return None


# -------------------------
# Gemini reasoning
# -------------------------
def ask_gemini(prompt):

    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# -------------------------
# Assistant loop
# -------------------------
def main():

    print("AI Assistant started")

    while True:

        user_text = listen()

        if not user_text:
            continue

        if "exit" in user_text.lower() or "stop" in user_text.lower():
            print("Assistant stopped")
            break

        reply = ask_gemini(user_text)

        print("Gemini:", reply)

        asyncio.run(speak(reply))


if __name__ == "__main__":
    main()