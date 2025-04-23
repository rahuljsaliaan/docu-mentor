from typing import List, Callable, Dict, Iterator, Any
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from docu_mentor.core import settings
from docu_mentor.types.enums import OpenAIModelEnum


# Create embeddings object
embeddings = OpenAIEmbeddings(
    api_key=settings.api.openai_api_key, model=OpenAIModelEnum.TEXT_EMBEDDING_3_SMALL
)

embeddings_config = settings.embedding.config(OpenAIModelEnum.TEXT_EMBEDDING_3_SMALL)


def batch_documents(
    documents: List[Document], batch_size: int
) -> Iterator[List[Document]]:
    for i in range(0, len(documents), batch_size):
        yield documents[i : i + batch_size]


def batch_store_documents(
    documents: List[Document], updater: Callable[[List[Document]], Any]
):
    for batch in batch_documents(
        documents=documents,
        batch_size=embeddings_config["batch_size"],
    ):
        updater(batch)


def ingest_docs():
    loader = ReadTheDocsLoader(path=settings.url.langchain_docs_path, encoding="utf-8")

    raw_documents = loader.load()

    print(f"Loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=embeddings_config["chunk_size"],
        chunk_overlap=embeddings_config["chunk_overlap"],
    )

    documents = text_splitter.split_documents(documents=raw_documents)

    for doc in documents:
        new_url: str = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https://")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} documents to Pinecone")

    batch_store_documents(
        documents=documents,
        updater=lambda documents: PineconeVectorStore.from_documents(
            pinecone_api_key=settings.api.pinecone_api_key,
            documents=documents,
            embedding=embeddings,
            index_name=settings.config.index_name,
        ),
    )

    print("Stored and indexed documents successfully")


if __name__ == "__main__":
    ingest_docs()
