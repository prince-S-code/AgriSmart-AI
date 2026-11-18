from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AgriSmart AI"
    app_env: str = "development"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_days: int = 14
    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    mongodb_db: str = "agrismart"
    cors_origins: str = "http://localhost:5173"
    upload_dir: str = "uploads"
    max_upload_mb: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


settings = Settings()
