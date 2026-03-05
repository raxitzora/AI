from dotenv import load_dotenv
from google import genai
load_dotenv()

client = genai.Client(api_key="AIzaSyCO_TQQHSqh5tSvRyeouQ2QKgMDA6UAcHg")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

def main():
    query = input("> ")
    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=query,
    )

print(f"{response.text[0].text}")

main()