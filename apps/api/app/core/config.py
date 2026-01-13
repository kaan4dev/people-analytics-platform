from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env", extra = "ignore")

    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "people"
    DB_USER: str = "people"
    DB_PASSWORD: str = "people"

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()