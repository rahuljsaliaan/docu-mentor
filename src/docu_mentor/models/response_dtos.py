from typing import List
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
