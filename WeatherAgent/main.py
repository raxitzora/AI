from openai import OpenAI



client = OpenAI(
    api_key="AIzaSyAmvF2RBUAVGotbSr7aFtCkpeyYqTcKdAo",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
) 

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role":"user","content":user_query}
        ]
        
    )
    
    print(response.choices[0].message.content)
    
main()
