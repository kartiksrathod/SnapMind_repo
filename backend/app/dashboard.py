from pydantic import BaseModel

from .ai.providers import LLMProvider
from .documents.storage import DocumentStorage
from .hardware.capabilities import detect_hardware
from .knowledge.service import KnowledgeService


class DashboardSnapshot(BaseModel):
    document_count: int
    indexed_chunk_count: int
    recent_documents: list[dict[str, object]]
    ai: dict[str, object]
    hardware: dict[str, object]


def snapshot(documents: DocumentStorage, knowledge: KnowledgeService, provider: LLMProvider) -> DashboardSnapshot:
    records = documents.list_documents()
    hardware = detect_hardware()
    return DashboardSnapshot(
        document_count=len(records),
        indexed_chunk_count=knowledge.store.count(),
        recent_documents=[record.model_dump(mode='json') for record in records[:5]],
        ai={'status': 'ready' if provider.is_available() else 'unavailable', 'model': provider.model_name},
        hardware={'processor': hardware.processor, 'cpu_status': hardware.cpu.status, 'gpu_status': hardware.gpu.status, 'npu_status': hardware.npu.status, 'npu_evidence': hardware.npu.evidence},
    )
