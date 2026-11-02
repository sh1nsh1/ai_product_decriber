from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseEnv(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Config(BaseEnv):
    deepseek_api_key: str


def get_config() -> Config:
    return Config.model_validate({})
