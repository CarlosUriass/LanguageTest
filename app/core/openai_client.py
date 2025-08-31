import openai
from app.core.settings import settings 

class OpenAIClient:
    def __init__(self, model: str = None):
        self.model = model or settings.OPENAI_MODEL  
        self.api_key = settings.OPENAI_API_KEY

    def send_prompt(self, prompt: str) -> str:
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
