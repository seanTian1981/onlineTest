from __future__ import annotations

import threading
from typing import Optional


class TextToSpeech:
    def __init__(self) -> None:
        self._engine = self._init_engine()
        self._lock = threading.Lock()

    @property
    def available(self) -> bool:
        return self._engine is not None

    def speak(self, text: str) -> None:
        if not self.available:
            return
        if not text:
            return
        with self._lock:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception:
                self._engine = None

    def _init_engine(self) -> Optional[object]:
        try:
            import pyttsx3  # type: ignore

            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            engine.setProperty("volume", 1.0)
            return engine
        except Exception:
            return None


def build_tts() -> TextToSpeech:
    return TextToSpeech()
