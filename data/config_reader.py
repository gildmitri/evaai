from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMINS: list[int]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
