import os
import openai
from openai import OpenAI

def alice_ai_chat(messages):
    client = OpenAI(api_key = "your OAI key here.")
    model = "gpt-4o-mini"
    messages_list = []
    system_prompt = "You are a helpful assistant called Alice, 앨리스 in Korean. Your Answers must be concise and not too long. you must answer with honorable language. Answer with user's Language. reply under 400 letters(300 letters in Korean.)"
    messages_list.append({"role": "system", "content": system_prompt})
    for i in messages:
        messages_list.append(i)
    responce = client.chat.completions.create(
        model=model,
        messages = messages_list,
    )
    return (responce.choices[0].message.content)