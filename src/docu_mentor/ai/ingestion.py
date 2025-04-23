from pinecone import Pinecone
from typing import List, Callable, Dict, Iterator, Any
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


from docu_mentor.core import settings
from docu_mentor.types.enums import OpenAIModelEnum
from docu_mentor.utils import custom_firecrawl_loader


# Create Pinecone client
pinecone = Pinecone(
    api_key=settings.api.pinecone_api_key,
)


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


def ingest_docs(
    raw_documents: List[Document],
    pine_cone_config: Dict[str, Any],
    documents_manipulator: Callable[[List[Document]], List[Document]] = None,
) -> None:
    print(f"Loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=embeddings_config["chunk_size"],
        chunk_overlap=embeddings_config["chunk_overlap"],
    )

    documents = text_splitter.split_documents(documents=raw_documents)

    documents_manipulator(documents) if documents_manipulator else None

    print(f"Going to add {len(documents)} documents to Pinecone")

    batch_store_documents(
        documents=documents,
        updater=lambda documents: PineconeVectorStore.from_documents(
            pinecone_api_key=settings.api.pinecone_api_key,
            documents=documents,
            embedding=embeddings,
            **pine_cone_config,
        ),
    )

    print("Stored and indexed documents successfully")


def ingest_local_docs():
    loader = ReadTheDocsLoader(path=settings.url.langchain_docs_path, encoding="utf-8")

    raw_documents = loader.load()

    ingest_docs(
        raw_documents=raw_documents,
        pine_cone_config={"index_name": settings.config.index_name},
        documents_manipulator=lambda documents: [
            doc.metadata.update(
                {"source": doc.metadata["source"].replace("langchain-docs", "https://")}
            )
            or doc
            for doc in documents
        ],
    )


def ingest_docs_faiss(
    raw_documents: List[Document],
    faiss_index_path: str = None,
    documents_manipulator: Callable[[List[Document]], List[Document]] = None,
) -> None:
    print(f"Loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=embeddings_config["chunk_size"],
        chunk_overlap=embeddings_config["chunk_overlap"],
    )

    documents = text_splitter.split_documents(documents=raw_documents)

    if documents_manipulator:
        documents = documents_manipulator(documents)

    print(f"Going to add {len(documents)} documents to FAISS")

    vectorstore = FAISS.from_documents(documents, embeddings)

    if faiss_index_path:
        vectorstore.save_local(faiss_index_path)

    print(
        f"Stored and indexed {len(documents)} documents in FAISS at '{faiss_index_path}'"
    )

    return vectorstore


def ingest_docs_from_url(
    url: str,
) -> FAISS:
    # 1. Load the documents from the URL
    raw_documents = custom_firecrawl_loader(url=url)

    # 2. Ingest
    return ingest_docs_faiss(
        raw_documents=raw_documents,
    )


if __name__ == "__main__":
    ingest_docs_from_url("https://python.langchain.com/docs")
