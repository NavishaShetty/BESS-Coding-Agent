## Script to test OpenRouter API key for OpenAI client
# This script checks if the OpenRouter API key is valid by making a simple request to the OpenAI API.

from openai import OpenAI
from config.helper import get_openrouter_api_key


client = OpenAI(
  base_url= "https://openrouter.ai/api/v1",
  api_key= get_openrouter_api_key(),
)

completion = client.chat.completions.create(
  model="qwen/qwen-2.5-72b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)