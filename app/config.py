from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Vestibular Flashcards API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    FRONTEND_URL: str = "http://localhost:5173"

    DATABASE_URL: str = "sqlite:///./vestibular.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()