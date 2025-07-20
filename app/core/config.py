from pydantic_settings import BaseSettings
import os




class Settings(BaseSettings):
    database_url: str
    #don't change this very important for Github Secret variables
    rsa_private_key:str = os.getenv("RSA_PRIVATE_KEY")
    rsa_public_key:str = os.getenv("RSA_PUBLIC_KEY")

    jwt_algorithm: str
    jwt_exp_minutes: int
    jwt_exp_days: int

    class Config:
        env_file = None if os.environ.get("ENVIRONMENT") == "Testing" else ".env"

settings = Settings()
