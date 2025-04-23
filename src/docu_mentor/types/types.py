from typing import TypedDict, List, Tuple, Literal


class EmbeddingSettingsDict(TypedDict):
    chunk_size: int
    chunk_overlap: int
    batch_size: int
    dimensions: int
    metric: str


ChatHistoryType = List[Tuple[Literal["human", "ai"], str]]
