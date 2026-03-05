from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyAmvF2RBUAVGotbSr7aFtCkpeyYqTcKdAo",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {   "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message)