from langchain.llms.base import LLM
from pydantic import PrivateAttr
from typing import Optional, List
from app.core.openai_client import OpenAIClient

class LangBuddyLLM(LLM):
    _client: OpenAIClient = PrivateAttr()

    def __init__(self, client: OpenAIClient, **kwargs):
        super().__init__(**kwargs)
        self._client = client

    @property
    def _llm_type(self) -> str:
        return "openai_custom"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return self._client.send_prompt(prompt)
