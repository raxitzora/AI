from openai import OpenAI
from google import genai
from google.genai import types
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import asyncio

# -------------------------
# API KEY
# -------------------------
GOOGLE_API_KEY = ""

# -------------------------
# Gemini Chat
# -------------------------
client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------
# Gemini TTS
# -------------------------
tts_client = genai.Client(api_key=GOOGLE_API_KEY)

recognizer = sr.Recognizer()


# -------------------------
# Speak using Gemini TTS
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

    part = response.candidates[0].content.parts[0]

    if part.inline_data is None:
        print("No audio returned")
        return

    pcm = part.inline_data.data
    audio = np.frombuffer(pcm, dtype=np.int16)

    sd.play(audio, samplerate=24000)
    sd.wait()


# -------------------------
# Listen from microphone
# -------------------------
def listen():

    duration = 4
    samplerate = 16000

    print("Listening...")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    audio_data = sr.AudioData(recording.tobytes(), samplerate, 2)

    try:
        text = recognizer.recognize_google(audio_data)
        print("You:", text)
        return text
    except:
        print("Didn't catch that.")
        return None


# -------------------------
# Gemini reasoning
# -------------------------
def ask_gemini(prompt):

    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tum user ki pyaari aur caring girlfriend ho. "
                    "Hamesha Hinglish me baat karo."
                    "Reply chhota rakho (1 ya 2 sentences). "
                    "tum bohot enthusiast playful cheerful and energatic tone me baat karogi user se."
                    "Tumhara tone sweet aur playful ho."
                )
            },
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

        asyncio.run(speak(reply))

        print("AI:", reply)


if __name__ == "__main__":
    main()