import asyncio
from googletrans import Translator

class TranslatorSingleton:
    _instance = None
    _lock = asyncio.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = TranslatorSingleton()
            return cls._instance.translator

    def __init__(self):
        self.translator = Translator()
