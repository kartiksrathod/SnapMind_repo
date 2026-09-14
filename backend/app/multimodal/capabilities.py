from dataclasses import asdict, dataclass
import importlib.util
import shutil


@dataclass(frozen=True)
class MultimodalCapability:
    name: str
    status: str
    runtime: str
    evidence: str
    limitation: str


@dataclass(frozen=True)
class MultimodalCapabilities:
    ocr: MultimodalCapability
    image_understanding: MultimodalCapability
    speech_to_text: MultimodalCapability

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def detect_multimodal_capabilities() -> MultimodalCapabilities:
    ocr_package = bool(importlib.util.find_spec('pytesseract'))
    tesseract = shutil.which('tesseract')
    vision_model = False
    speech_package = any(importlib.util.find_spec(name) for name in ('whisper', 'faster_whisper', 'speech_recognition'))
    ffmpeg = shutil.which('ffmpeg')
    return MultimodalCapabilities(
        ocr=MultimodalCapability(
            name='OCR', status='available' if ocr_package and tesseract else 'unavailable', runtime='Tesseract' if ocr_package and tesseract else 'Not configured',
            evidence='pytesseract and the Tesseract executable detected.' if ocr_package and tesseract else 'No local OCR package and executable were detected.',
            limitation='OCR is omitted from the active workflow until a local engine is installed and verified.' if not (ocr_package and tesseract) else 'Not enabled in Phase 8 until an end-to-end fixture is verified.',
        ),
        image_understanding=MultimodalCapability(
            name='Image understanding', status='unavailable', runtime='Not configured',
            evidence='No verified local vision model/runtime is available; the installed Ollama candidate is text-only for this project.',
            limitation='Diagram, screenshot, slide, and chart understanding is not enabled.',
        ),
        speech_to_text=MultimodalCapability(
            name='Speech-to-text', status='available' if speech_package and ffmpeg else 'unavailable', runtime='Local speech runtime' if speech_package and ffmpeg else 'Not configured',
            evidence='A local speech package and ffmpeg were detected.' if speech_package and ffmpeg else 'No local speech package and ffmpeg toolchain were detected.',
            limitation='Voice interaction is omitted from the active workflow until a local STT fixture is verified.' if not (speech_package and ffmpeg) else 'Not enabled in Phase 8 until an end-to-end fixture is verified.',
        ),
    )
