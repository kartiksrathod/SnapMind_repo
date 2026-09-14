from dataclasses import dataclass
import re

from ..documents.parsers import ParsedSegment


@dataclass
class TextChunk:
    text: str
    page: int | None
    section: str | None
    position: int


class TextCleaner:
    def clean(self, text: str) -> str:
        text = text.replace('\x00', ' ')
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return '\n'.join(line.strip() for line in text.splitlines()).strip()


class TextChunker:
    def __init__(self, chunk_size: int = 700, overlap: int = 100) -> None:
        if overlap >= chunk_size:
            raise ValueError('Chunk overlap must be smaller than chunk size.')
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, segments: list[ParsedSegment]) -> list[TextChunk]:
        chunks: list[TextChunk] = []
        position = 0
        for segment in segments:
            text = TextCleaner().clean(segment.text)
            if not text:
                continue
            section = segment.section
            start = 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                if end < len(text):
                    boundary = max(text.rfind('\n', start, end), text.rfind(' ', start, end))
                    if boundary > start + self.chunk_size // 2:
                        end = boundary
                chunk_text = text[start:end].strip()
                if chunk_text:
                    chunks.append(TextChunk(chunk_text, segment.page, section, position))
                    position += 1
                if end >= len(text):
                    break
                start = max(end - self.overlap, start + 1)
        return chunks
