from typing import TypedDict


class EmbeddingSettingsDict(TypedDict):
    chunk_size: int
    chunk_overlap: int
    batch_size: int
