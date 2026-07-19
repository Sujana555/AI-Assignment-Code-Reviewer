'''
This file is used to just connect to an LLM.
It will take in the prompt and any files as input and return the response.
'''

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"

)

def get_llm_response(text:str, user_question:str, system_prompt:str):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Assignment content: \n{text}\n\n Question: {user_question}\n"}]
    )
    return response.choices[0].message.content.strip()
