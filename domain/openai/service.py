from openai import OpenAI
from typing import Dict
import os
from dotenv import load_dotenv
import json
import aiohttp
from domain.word.entities import Dictionary

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


class OpenAiService:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)

    async def get_word_info(self, word: str) -> Dict[str, str]:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": (
                    f"Please provide the definition, part of speech, two example sentences(as example_sentences), "
                    f"and the Korean meaning for the word '{word}' in JSON format. "
                    f"If you don't know the answer or if the word does not exist, please provide an empty string."
                ),
            },
        ]
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "response_format": {"type": "json_object"},
                },
            ) as response:
                response_data = await response.json()
                response_content = response_data["choices"][0]["message"]["content"]
                response_json = json.loads(response_content)
                print(" >>> response_json: ", response_json)
                word_info = Dictionary(
                    word=word,
                    word_class=response_json["part_of_speech"],
                    kr_meaning=response_json["korean_meaning"],
                    en_meaning=response_json["definition"],
                    example=response_json["example_sentences"],
                )
                print(" >>> complete word_info >>> ")
                return word_info
