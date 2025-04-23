from typing import List, Set
from pydantic import BaseModel, ConfigDict, Field
from langchain_core.documents import Document


class DocsRetrievalResponseDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    query: str = Field(
        ..., alias="input", description="The user input that was given to the model."
    )
    result: str = Field(
        ..., alias="answer", description="The final answer of the retrieval chain."
    )
    source_documents: List[Document] = Field(
        ...,
        alias="context",
        description="The list of source documents of the final answer.",
    )

    @classmethod
    def create_sources_string(cls, source_urls: Set[str]):
        if not source_urls:
            return ""

        source_string = "sources:\n"

        for i, source in enumerate(source_urls):
            source_string += f"{i + 1}: {source}\n"

        return source_string

    @property
    def formatted_response(self) -> str:
        metadata = set(doc.metadata["source"] for doc in self.source_documents)
        sources_string = self.create_sources_string(metadata)
        return f"{self.result} \n\n {sources_string}"
