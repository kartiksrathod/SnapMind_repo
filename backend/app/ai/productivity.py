import json
import re
from dataclasses import dataclass

from ..knowledge.models import KnowledgeChunk
from ..knowledge.service import KnowledgeService
from .backends import InferenceBackend
from .models import Citation
from .providers import LLMProvider


class ProductivityGenerationError(RuntimeError):
    pass


@dataclass
class StudyContext:
    chunks: list[KnowledgeChunk]
    citations: list[Citation]


class ProductivityService:
    def __init__(self, knowledge: KnowledgeService, provider: LLMProvider, backend: InferenceBackend) -> None:
        self.knowledge = knowledge
        self.provider = provider
        self.backend = backend

    def context(self, document_ids: list[str] | None = None) -> StudyContext:
        chunks = self.knowledge.chunks(document_ids)
        citations = [Citation(citation_id=index, document_id=chunk.document_id, document_name=chunk.filename, page=chunk.page, section=chunk.section, chunk_id=chunk.chunk_id) for index, chunk in enumerate(chunks, 1)]
        return StudyContext(chunks=chunks, citations=citations)

    def generate(self, task: str, context: StudyContext, detail: str = 'short') -> dict[str, object]:
        if not context.chunks:
            raise ValueError('There is no indexed knowledge available for this study action.')
        source_text = '\n\n'.join(f'[{index}] {chunk.filename} | page={chunk.page or "unknown"} | section={chunk.section or "unknown"}\n{chunk.text}' for index, chunk in enumerate(context.chunks, 1))
        prompt = f"""You are SnapMind, a local study assistant. Use only the source context below. Never invent facts, questions, answers, options, or citations. Every source number must refer to a source in the context. Return valid JSON only, with no markdown fences. Task: {task}. Detail: {detail}.\n\nSource context:\n{source_text}"""
        try:
            raw = self.backend.generate_structured(self.provider, prompt)
            return self._validate_result(self._validate_sources(self._parse_json(raw), len(context.citations)), task)
        except ProductivityGenerationError:
            raise
        except Exception as exc:
            raise ProductivityGenerationError('The local model could not generate this study material.') from exc

    @staticmethod
    def _parse_json(raw: str) -> dict[str, object]:
        candidate = raw.strip()
        fenced = re.search(r'```(?:json)?\s*(.*?)```', candidate, re.DOTALL | re.IGNORECASE)
        if fenced:
            candidate = fenced.group(1).strip()
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise ProductivityGenerationError('The local model returned invalid structured study data.') from exc
        if not isinstance(parsed, dict):
            raise ProductivityGenerationError('The local model returned an invalid study response.')
        return parsed

    @staticmethod
    def _validate_sources(result: dict[str, object], source_count: int) -> dict[str, object]:
        def walk(value: object) -> None:
            if isinstance(value, dict):
                if 'source_ids' in value:
                    source_ids = value['source_ids']
                    if isinstance(source_ids, list):
                        normalized = [int(item) if isinstance(item, str) and item.isdigit() else item for item in source_ids]
                        value['source_ids'] = normalized
                        source_ids = normalized
                    if not isinstance(source_ids, list) or any(not isinstance(item, int) or item < 1 or item > source_count for item in source_ids):
                        raise ProductivityGenerationError('The local model returned an invalid source reference.')
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        walk(result)
        return result

    @staticmethod
    def _validate_result(result: dict[str, object], task: str) -> dict[str, object]:
        if 'summary' in task and not isinstance(result.get('short_summary'), str):
            raise ProductivityGenerationError('The local model returned no valid summary.')
        expected = 'key_points' if 'Extract important' in task else 'questions' if 'Create up to 5' in task else 'flashcards' if 'flashcards' in task.lower() else ''
        if expected and not isinstance(result.get(expected), list):
            raise ProductivityGenerationError('The local model returned incomplete structured study data.')
        return result
