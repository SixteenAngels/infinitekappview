from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, case_sensitive=True)

    DATABASE_URL: str = "sqlite:///./infinitek.db"
    MQTT_BROKER: str = "broker.hivemq.com"
    MQTT_PORT: int = 1883
    JWT_SECRET: str = "changeme"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    API_PREFIX: str = "/api"


settings = Settings()
