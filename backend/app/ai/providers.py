from abc import ABC, abstractmethod
import json
import os
import socket
from typing import Iterator
from urllib.error import URLError
from urllib.request import Request, urlopen


class ModelUnavailableError(RuntimeError):
    pass


class LLMProvider(ABC):
    @property
    @abstractmethod
    def model_name(self) -> str: ...

    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def generate(self, prompt: str, history: list[dict[str, str]] | None = None) -> str: ...

    def stream(self, prompt: str, history: list[dict[str, str]] | None = None) -> Iterator[str]:
        yield self.generate(prompt, history)

    def generate_structured(self, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        return self.generate(prompt, history)


class OllamaProvider(LLMProvider):
    def __init__(self, model_name: str | None = None, base_url: str | None = None) -> None:
        self._model_name = model_name or os.getenv('SNAPMIND_OLLAMA_MODEL', 'llama3.2:latest')
        self.base_url = (base_url or os.getenv('SNAPMIND_OLLAMA_URL', 'http://127.0.0.1:11434')).rstrip('/')

    @property
    def model_name(self) -> str:
        return self._model_name

    def is_available(self) -> bool:
        try:
            request = Request(f'{self.base_url}/api/tags', method='GET')
            with urlopen(request, timeout=2) as response:
                models = json.loads(response.read()).get('models', [])
            return any(model.get('name') == self._model_name for model in models)
        except (OSError, URLError, ValueError):
            return False

    def generate(self, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        return self._generate(prompt, history, structured=False)

    def generate_structured(self, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        return self._generate(prompt, history, structured=True)

    def _generate(self, prompt: str, history: list[dict[str, str]] | None, structured: bool) -> str:
        if not self.is_available():
            raise ModelUnavailableError(f'Local model {self._model_name} is unavailable. Start Ollama and check the model installation.')
        messages = (history or []) + [{'role': 'user', 'content': prompt}]
        payload_data = {'model': self._model_name, 'messages': messages, 'stream': False, 'options': {'temperature': 0.1}}
        if structured:
            payload_data['format'] = 'json'
        payload = json.dumps(payload_data).encode()
        request = Request(f'{self.base_url}/api/chat', data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urlopen(request, timeout=float(os.getenv('SNAPMIND_LLM_TIMEOUT_SECONDS', '300'))) as response:
                result = json.loads(response.read())
            answer = result.get('message', {}).get('content', '').strip()
            if not answer:
                raise RuntimeError('The local model returned an empty response.')
            return answer
        except socket.timeout as exc:
            raise RuntimeError('The local model timed out while generating a response. Try a shorter source set or a smaller model.') from exc
        except (OSError, URLError, ValueError) as exc:
            raise RuntimeError('The local model could not complete generation.') from exc
