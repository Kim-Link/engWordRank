from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


class OpenAiService:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, word: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"'{word}'의 뜻과 사용 예시 알려줘."},
        ]
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"},
        )
        print("completion >> ", completion.choices[0].message.content)
        return completion.choices[0].message.content
