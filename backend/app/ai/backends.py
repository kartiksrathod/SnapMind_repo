from abc import ABC, abstractmethod
from dataclasses import dataclass

from .providers import LLMProvider


@dataclass(frozen=True)
class InferenceReport:
    backend: str
    runtime: str
    status: str
    evidence: str
    limitation: str | None = None


class InferenceBackend(ABC):
    @property
    @abstractmethod
    def report(self) -> InferenceReport: ...

    @abstractmethod
    def generate(self, provider: LLMProvider, prompt: str, history: list[dict[str, str]] | None = None) -> str: ...

    def generate_structured(self, provider: LLMProvider, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        return provider.generate_structured(prompt, history)


class CPUBackend(InferenceBackend):
    @property
    def report(self) -> InferenceReport:
        return InferenceReport(
            backend='CPU', runtime='Ollama local runtime', status='active',
            evidence='Generation is dispatched to the local Ollama service; accelerator usage is not exposed or independently verified.',
            limitation='CPU execution is the safe fallback. NPU execution not verified; no Qualcomm acceleration is claimed.',
        )

    def generate(self, provider: LLMProvider, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        return provider.generate(prompt, history)


class UnsupportedAcceleratorBackend(InferenceBackend):
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def report(self) -> InferenceReport:
        return InferenceReport(self.name, 'Not configured', 'unsupported', f'{self.name} backend is not implemented or verified in this environment.')

    def generate(self, provider: LLMProvider, prompt: str, history: list[dict[str, str]] | None = None) -> str:
        raise RuntimeError(f'{self.name} inference backend is not available.')


def select_backend() -> InferenceBackend:
    return CPUBackend()
