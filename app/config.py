
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# fucking pydantic. it's broken without manually loading .env
load_dotenv()

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        case_sensitive = False
        env_file = '.env'


settings = Settings()