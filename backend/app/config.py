from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AlgoForge API"
    environment: str = "development"
    cors_origins: str = "http://localhost:5173"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    judge0_base_url: str = "https://judge0-ce.p.rapidapi.com"
    judge0_rapidapi_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
