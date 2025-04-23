from langchain import hub
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_pinecone import PineconeVectorStore

from docu_mentor.types.enums import OpenAIModelEnum
from docu_mentor.core import settings
from docu_mentor.models.response_dtos import DocsRetrievalResponseDTO
from docu_mentor.types.types import ChatHistoryType

embeddings = OpenAIEmbeddings(
    api_key=settings.api.openai_api_key, model=OpenAIModelEnum.TEXT_EMBEDDING_3_SMALL
)


def run_llm(
    query: str,
    chat_history: ChatHistoryType,
    faiss_index: FAISS = None,
) -> DocsRetrievalResponseDTO:
    docsearch_vector_store = PineconeVectorStore(
        pinecone_api_key=settings.api.pinecone_api_key,
        embedding=embeddings,
        index_name=settings.config.index_name,
    )

    chat = ChatOpenAI(
        api_key=settings.api.openai_api_key, model=OpenAIModelEnum.GPT_4O_MINI
    )

    # Load the prompt from LangChain Hub and create a stuff documents chain
    retrieval_qa_chat_prompt = hub.pull(settings.url.retrieval_qa_chat_prompt_url)
    stuff_documents_chain = create_stuff_documents_chain(
        prompt=retrieval_qa_chat_prompt, llm=chat
    )

    # Choose the retriever based on whether FAISS index is provided or not
    retriever = (
        faiss_index.as_retriever()
        if faiss_index
        else docsearch_vector_store.as_retriever()
    )

    # Load the rephrase prompt from LangChain Hub and create a history-aware retriever
    rephrase_prompt = hub.pull(settings.url.rephrase_prompt_url)
    history_aware_retriever = create_history_aware_retriever(
        prompt=rephrase_prompt,
        llm=chat,
        retriever=retriever,
    )

    # Create the retrieval chain using the history-aware retriever and stuff documents chain
    retrieval_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain,
    )

    result = retrieval_chain.invoke(
        input={"input": query, "chat_history": chat_history}
    )

    return DocsRetrievalResponseDTO(**result)


if __name__ == "__main__":
    result = run_llm()
    print(result.model_dump_json(indent=2))
