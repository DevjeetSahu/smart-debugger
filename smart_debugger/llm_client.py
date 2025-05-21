from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY")
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

def get_llm_suggestion(error_msg, frames_with_snippets):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a software debugging assistant. "
                "Given an error stack trace and relevant source code snippets, "
                "your task is to identify the root cause and suggest possible fixes."
            )
        },
        {
            "role": "user",
            "content": (
                f"Error message:\n{error_msg}\n\n"
                "Stack trace with code snippets:\n"
                + "\n\n".join(
                    f"File: {frame['file']} (line {frame['line']})\nCode:\n{frame['snippet']}"
                    for frame in frames_with_snippets
                )
            )
        }
    ]

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    return response.choices[0].message.content


    # dummytext="This is an ai generated suggestion for the error"
    # return dummytext
