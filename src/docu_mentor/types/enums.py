from enum import Enum


class EnvironmentEnum(str, Enum):
    production = "production"
    development = "development"


from enum import Enum


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
