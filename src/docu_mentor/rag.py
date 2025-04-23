from langchain import hub
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_pinecone import PineconeVectorStore

from docu_mentor.types.enums import OpenAIModelEnum
from docu_mentor.core import settings
from docu_mentor.models.response_dtos import DocsRetrievalResponseDTO

embeddings = OpenAIEmbeddings(
    api_key=settings.api.openai_api_key, model=OpenAIModelEnum.TEXT_EMBEDDING_3_SMALL
)


def run_llm(query: str) -> DocsRetrievalResponseDTO:
    docsearch_vector_store = PineconeVectorStore(
        pinecone_api_key=settings.api.pinecone_api_key,
        embedding=embeddings,
        index_name=settings.config.index_name,
    )

    chat = ChatOpenAI(
        api_key=settings.api.openai_api_key, model=OpenAIModelEnum.GPT_4O_MINI
    )

    retrieval_qa_chat_prompt = hub.pull(settings.url.retrieval_qa_chat_prompt_url)

    stuff_documents_chain = create_stuff_documents_chain(
        llm=chat, prompt=retrieval_qa_chat_prompt
    )

    retrieval_chain = create_retrieval_chain(
        retriever=docsearch_vector_store.as_retriever(),
        combine_docs_chain=stuff_documents_chain,
    )

    result = retrieval_chain.invoke(input={"input": query})

    return DocsRetrievalResponseDTO(**result)


if __name__ == "__main__":
    result = run_llm()
    print(result.model_dump_json(indent=2))
