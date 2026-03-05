from google import genai
from dotenv import load_dotenv
import requests

load_dotenv()


client = genai.Client()

print("Chat started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Exiting chat...")
        break

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_input,
        )

        print("Agent:", response.text)
        print()

    except Exception as e:
        print("Error:", e)