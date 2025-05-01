from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from openai._exceptions import AuthenticationError, RateLimitError, OpenAIError

# Replace with your actual API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY_TEST')
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=5
    )
    message: ChatCompletionMessage = response.choices[0].message
    print("✅ API key is valid. Response:", message.content)

except AuthenticationError:
    print("❌ Invalid API key.")
except RateLimitError as e:
    print("❌ Rate limit or quota exceeded:", e)
except OpenAIError as e:
    print("❌ Other OpenAI error:", e)
