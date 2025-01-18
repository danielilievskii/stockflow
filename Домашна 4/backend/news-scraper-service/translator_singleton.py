import threading
from googletrans import Translator

class TranslatorSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TranslatorSingleton, cls).__new__(cls)
                    cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        self.translator = Translator()

    def get_translator(self):
        return self.translator
