from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = ""
    azure_openai_api_version: str = "2024-06-01"

    # Rate-limiting for batch endpoint (requests per second to LLM)
    llm_max_concurrency: int = 5

    model_config = {"env_file": ".env"}


settings = Settings()
