from abc import ABC, abstractmethod
import hashlib
import re


class EmbeddingService(ABC):
    @property
    @abstractmethod
    def dimensions(self) -> int: ...

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class HashingEmbeddingService(EmbeddingService):
    """Deterministic offline baseline; replaceable by a semantic model later."""

    def __init__(self, dimensions: int = 512) -> None:
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        stopwords = {'a', 'an', 'and', 'are', 'for', 'in', 'is', 'of', 'on', 'the', 'to', 'use', 'uses', 'what'}
        tokens = [token for token in re.findall(r"[\w']+", text.lower()) if token not in stopwords]
        vector = [0.0] * self._dimensions
        if not tokens:
            return vector
        for index, token in enumerate(tokens):
            vector[self._bucket(token)] += 1.0
            if index:
                vector[self._bucket(f'{tokens[index - 1]} {token}')] += 0.5
        norm = sum(value * value for value in vector) ** 0.5
        return [value / norm for value in vector] if norm else vector

    def _bucket(self, token: str) -> int:
        digest = hashlib.sha256(token.encode('utf-8')).digest()
        return int.from_bytes(digest[:8], 'big') % self._dimensions
