from statistics import mean
from time import perf_counter

from pydantic import BaseModel, Field

from .ai.backends import InferenceBackend
from .ai.providers import LLMProvider
from .knowledge.service import KnowledgeService


class RetrievalBenchmarkRequest(BaseModel):
    query: str = 'grounded local AI'
    iterations: int = Field(default=10, ge=1, le=100)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalBenchmarkResult(BaseModel):
    workload: str
    query: str
    iterations: int
    top_k: int
    indexed_chunks: int
    warmup_results: int
    average_latency_ms: float
    minimum_latency_ms: float
    maximum_latency_ms: float
    backend: str
    runtime: str
    model: str
    status: str
    limitation: str | None


def run_retrieval(request: RetrievalBenchmarkRequest, knowledge: KnowledgeService, backend: InferenceBackend, provider: LLMProvider) -> RetrievalBenchmarkResult:
    query = request.query.strip()
    if not query:
        raise ValueError('Benchmark query cannot be empty.')
    warmup = knowledge.search(query, request.top_k)
    timings = []
    for _ in range(request.iterations):
        start = perf_counter()
        knowledge.search(query, request.top_k)
        timings.append((perf_counter() - start) * 1000)
    report = backend.report
    return RetrievalBenchmarkResult(
        workload='Local RAG retrieval', query=query, iterations=request.iterations, top_k=request.top_k,
        indexed_chunks=knowledge.store.count(), warmup_results=len(warmup.results),
        average_latency_ms=round(mean(timings), 3), minimum_latency_ms=round(min(timings), 3), maximum_latency_ms=round(max(timings), 3),
        backend=report.backend, runtime=report.runtime, model=provider.model_name, status='measured', limitation=report.limitation,
    )
