# Asynchronous Example
import asyncio
import os
from mistralai import Mistral
from config import MISTRAL_API_KEY
async def generate(content):
    s = Mistral(
        api_key=MISTRAL_API_KEY,
    )
    res = await s.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "content": content,
                "role": "user",
            },
        ])
    if res is not None:
        return res
