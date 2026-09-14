export type ConnectionState = 'loading' | 'connected' | 'error'

export interface HealthResponse {
  status: string
  service: string
  phase: string
}

export interface ModelsResponse {
  status: string
  message: string
  models: string[]
}

export interface HardwareResponse {
  status: string
  message: string
  device: { os: string; processor: string; cpu: Capability; gpu: Capability; npu: Capability }
}
export interface Capability { name: string; status: string; evidence: string; limitation?: string | null }
export interface RuntimeResponse { backend: string; runtime: string; status: string; evidence: string; limitation: string | null; model: string }
export interface MultimodalCapability { name: string; status: string; runtime: string; evidence: string; limitation: string }
export interface MultimodalCapabilities { ocr: MultimodalCapability; image_understanding: MultimodalCapability; speech_to_text: MultimodalCapability }

export interface ConfigResponse {
  status: string
  processing_mode: string
  cloud_features: boolean
}

export type DocumentStatus = 'processing' | 'indexed' | 'failed'
export interface DocumentRecord {
  document_id: string
  filename: string
  file_type: string
  file_size: number
  created_at: string
  page_count: number | null
  processing_status: DocumentStatus
  error_message: string | null
  text_length: number
}
export interface KnowledgeChunk {
  document_id: string
  chunk_id: string
  filename: string
  file_type: string
  page: number | null
  section: string | null
  text: string
  position: number
  relevance: number
}
export interface Citation { citation_id: number; document_id: string; document_name: string; page: number | null; section: string | null; chunk_id: string }
export interface ChatMessage { role: string; content: string; citations: Citation[] }
export interface ChatResponse { session_id: string; answer: string; citations: Citation[]; retrieved_chunks: KnowledgeChunk[]; model: string; status: string; history: ChatMessage[] }
export interface StudyResponse { model: string; status: string; citations: Citation[]; data: Record<string, unknown> }
export interface DashboardSnapshot { document_count: number; indexed_chunk_count: number; recent_documents: DocumentRecord[]; ai: { status: string; model: string }; hardware: { processor: string; cpu_status: string; gpu_status: string; npu_status: string; npu_evidence: string } }
export interface BenchmarkResult { workload: string; query: string; iterations: number; top_k: number; indexed_chunks: number; warmup_results: number; average_latency_ms: number; minimum_latency_ms: number; maximum_latency_ms: number; backend: string; runtime: string; model: string; status: string; limitation: string | null }

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init)
  if (!response.ok) throw new Error(`Backend request failed (${response.status})`)
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<HealthResponse>('/api/health'),
  models: () => request<ModelsResponse>('/api/models'),
  hardware: () => request<HardwareResponse>('/api/hardware'),
  config: () => request<ConfigResponse>('/api/config'),
  runtime: () => request<RuntimeResponse>('/api/runtime'),
  multimodalCapabilities: () => request<MultimodalCapabilities>('/api/multimodal/capabilities'),
  dashboard: () => request<DashboardSnapshot>('/api/dashboard'),
  prepareDemo: () => request<DocumentRecord[]>('/api/demo/prepare', { method: 'POST' }),
  benchmarkRetrieval: (query: string, iterations = 10) => request<BenchmarkResult>('/api/benchmark/retrieval', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, iterations, top_k: 5 }) }),
  documents: () => request<{ documents: DocumentRecord[] }>('/api/documents'),
  uploadDocument: async (file: File) => {
    const body = new FormData()
    body.append('file', file)
    const response = await fetch('/api/documents', { method: 'POST', body })
    if (!response.ok) throw new Error((await response.json()).detail ?? 'Document upload failed.')
    return response.json() as Promise<DocumentRecord>
  },
  deleteDocument: async (documentId: string) => {
    const response = await fetch(`/api/documents/${documentId}`, { method: 'DELETE' })
    if (!response.ok) throw new Error((await response.json()).detail ?? 'Document deletion failed.')
  },
  retryDocument: async (documentId: string) => request<DocumentRecord>(`/api/documents/${documentId}/retry`, { method: 'POST' }),
  searchKnowledge: (query: string, top_k = 5) => request<{ query: string; indexed_chunks: number; results: KnowledgeChunk[] }>('/api/knowledge/search', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, top_k }) }),
  chat: (query: string, session_id: string) => request<ChatResponse>('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, session_id, top_k: 5 }) }),
  study: (kind: 'summary' | 'key-points' | 'quiz' | 'flashcards', detail = 'short') => request<StudyResponse>(`/api/study/${kind}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ detail }) }),
}
