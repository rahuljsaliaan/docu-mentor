from enum import Enum


class EnvironmentEnum(str, Enum):
    production = "production"
    development = "development"


class OpenAIModelEnum(str, Enum):
    # Chat & Completion Models
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0125 = "gpt-3.5-turbo-0125"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-1106-preview"
    GPT_4_VISION = "gpt-4-vision-preview"
    GPT_4_1 = "gpt-4.1"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O_PRO = "gpt-4o-pro"
    O3 = "o3"
    O4_MINI = "o4-mini"

    # Embedding Models
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


class PineConeModelEnum(str, Enum):
    MULTILINGUAL_E5_LARGE = "multilingual-e5-large"
    LLAMA_TEXT_EMBED_V2 = "llama-text-embed-v2"
    COHERE_RERANK_3_5 = "cohere-rerank-3.5"
    PINECONE_SPARSE_ENGLISH_V0 = "pinecone-sparse-english-v0"


class SessionStateEnum(str, Enum):
    documentation_url = "documentation_url"
    user_prompt_history = "user_prompt_history"
    chat_answer_history = "chat_answer_history"
    chat_history = "chat_history"
    faiss_index = "faiss_index"
    generating_response = "generating_response"


class ComponentsKeyEnum(str, Enum):
    url_input = "url_input"
    chat_prompt = "chat_prompt"
