from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from typing import List
import os
from constants import MODEL,TEMP
from prompts import resume_template
load_dotenv()

openai_api_key = os.environ.get('OPENAI_KEY')
client_async = AsyncOpenAI(
    api_key=openai_api_key, max_retries=3
)

async def query_llm(query:str,context:List[str]):
    try:
        response = await client_async.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": resume_template.substitute(
                        resume_dic=str(context), query=query
                    ),
                }
            ],
            temperature=TEMP,

        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return None