from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from app.core.settings import settings

class MemoryService:
    def __init__(self, session_id: str | None = None):
        # Usar session_id proporcionado o "default"
        self.session_id = session_id or "default"
        self.redis_url = settings.redis_url()

        # Inicializar historial y memoria
        self._init_memory()

    def _init_memory(self):
        """Inicializa RedisChatMessageHistory y ConversationBufferMemory"""
        self.message_history = RedisChatMessageHistory(
            session_id=self.session_id,
            url=self.redis_url,
        )
        self.memory = ConversationBufferMemory(
            chat_memory=self.message_history,
            return_messages=True
        )

    def set_session_id(self, session_id: str):
        """Actualizar session_id dinámicamente y reinicializar memoria"""
        self.session_id = session_id
        self._init_memory()

    def save_context(self, inputs: dict, outputs: dict):
        """Guardar inputs y outputs en la memoria"""
        self.memory.save_context(inputs, outputs)

    def load_memory_variables(self):
        """Obtener historial para el contexto actual"""
        return self.memory.load_memory_variables({})
