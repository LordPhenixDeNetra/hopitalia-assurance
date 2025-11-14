from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hopitalia Assurance API"
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    # API base prefix and version managed separately
    API_BASE_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    # Final prefix; if empty, will be composed from base + version
    API_PREFIX: str = ""
    DATABASE_URL: str = "postgresql+psycopg://netra:Passer123@postgresql-netra.alwaysdata.net:5432/hopitalia"
    DB_ECHO: bool = False
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    def model_post_init(self, __context: dict[str, object]) -> None:
        # Compose API_PREFIX if not explicitly provided
        if not self.API_PREFIX:
            self.API_PREFIX = f"{self.API_BASE_PREFIX}/{self.API_VERSION}"


settings = Settings()