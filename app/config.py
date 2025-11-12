from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_expires_in: str
    jwt_algorithm: str = "HS256"
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()