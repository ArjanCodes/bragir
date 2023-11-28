
from openai import OpenAI


def translate_content(client: OpenAI, text: str, language: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"You are a translator machine, you can only translate to the following language {language}. You need to keep the exact same format as the file. only translate the pieces of text. Make sure that all the text is translated and that there are no timestamps missing",
            },
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content or ""