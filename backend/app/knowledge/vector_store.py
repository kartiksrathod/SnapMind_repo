import json
import sqlite3
from pathlib import Path

from .models import KnowledgeChunk


class SQLiteVectorStore:
    """Small persistent local vector store using SQLite and cosine-ready vectors."""

    def __init__(self, database_path: Path, dimensions: int) -> None:
        self.database_path = database_path
        self.dimensions = dimensions
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute('''CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY, document_id TEXT NOT NULL, filename TEXT NOT NULL,
                file_type TEXT NOT NULL, page INTEGER, section TEXT, text TEXT NOT NULL,
                position INTEGER NOT NULL, vector TEXT NOT NULL)''')
            connection.execute('CREATE INDEX IF NOT EXISTS idx_chunks_document ON chunks(document_id)')

    def replace_document(self, document_id: str, filename: str, file_type: str, chunks: list[KnowledgeChunk], vectors: list[list[float]]) -> None:
        with self._connect() as connection:
            connection.execute('DELETE FROM chunks WHERE document_id = ?', (document_id,))
            connection.executemany('INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [
                (chunk.chunk_id, chunk.document_id, filename, file_type, chunk.page, chunk.section, chunk.text, chunk.position, json.dumps(vector))
                for chunk, vector in zip(chunks, vectors)
            ])

    def delete_document(self, document_id: str) -> None:
        with self._connect() as connection:
            connection.execute('DELETE FROM chunks WHERE document_id = ?', (document_id,))

    def count(self, document_id: str | None = None) -> int:
        with self._connect() as connection:
            query = 'SELECT COUNT(*) FROM chunks'
            parameters: tuple[str, ...] = ()
            if document_id:
                query += ' WHERE document_id = ?'
                parameters = (document_id,)
            return int(connection.execute(query, parameters).fetchone()[0])

    def chunks(self, document_ids: list[str] | None = None) -> list[KnowledgeChunk]:
        query = 'SELECT chunk_id, document_id, filename, file_type, page, section, text, position FROM chunks'
        parameters: list[str] = []
        if document_ids:
            placeholders = ','.join('?' for _ in document_ids)
            query += f' WHERE document_id IN ({placeholders})'
            parameters.extend(document_ids)
        query += ' ORDER BY document_id, position'
        with self._connect() as connection:
            return [KnowledgeChunk(document_id=row[1], chunk_id=row[0], filename=row[2], file_type=row[3], page=row[4], section=row[5], text=row[6], position=row[7], relevance=1, ) for row in connection.execute(query, parameters)]

    def search(self, vector: list[float], top_k: int, document_ids: list[str] | None = None) -> list[tuple[KnowledgeChunk, float]]:
        query = 'SELECT chunk_id, document_id, filename, file_type, page, section, text, position, vector FROM chunks'
        parameters: list[str] = []
        if document_ids:
            placeholders = ','.join('?' for _ in document_ids)
            query += f' WHERE document_id IN ({placeholders})'
            parameters.extend(document_ids)
        scored: list[tuple[KnowledgeChunk, float]] = []
        with self._connect() as connection:
            for row in connection.execute(query, parameters):
                candidate = json.loads(row[8])
                score = sum(left * right for left, right in zip(vector, candidate))
                if score >= 0.08:
                    scored.append((KnowledgeChunk(document_id=row[1], chunk_id=row[0], filename=row[2], file_type=row[3], page=row[4], section=row[5], text=row[6], position=row[7], relevance=max(0.0, min(1.0, score))), score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.execute('PRAGMA journal_mode=WAL')
        return connection
