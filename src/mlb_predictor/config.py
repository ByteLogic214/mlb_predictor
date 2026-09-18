from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mlb_base_url: str = "https://statsapi.mlb.com/api/v1"
    savant_base_url: str = "https://baseballsavant.mlb.com"
    odds_base_url: str = "https://api.the-odds-api.com/v4"
    odds_api_key: str = ""
    database_path: str = "data/mlb.sqlite"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
