from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ModelCandidate:
    model: str
    version: str
    format: str
    size: str
    quantization: str
    runtime: str
    supported_hardware: str
    intended_workload: str
    licensing: str
    compatibility_status: str
    evidence: str


CANDIDATES = [ModelCandidate(
    model='llama3.2', version='latest', format='Ollama package', size='2.0 GB reported by Ollama',
    quantization='Provider-managed; not independently inspected', runtime='Ollama',
    supported_hardware='Local CPU path verified; GPU/NPU usage unknown', intended_workload='Grounded text generation',
    licensing='Refer to the model license distributed with the Ollama model', compatibility_status='development candidate',
    evidence='Installed locally and used successfully in Phase 4 smoke testing; no Qualcomm AI Hub evidence.',
)]


def catalog() -> list[dict[str, str]]:
    return [asdict(candidate) for candidate in CANDIDATES]
