from typing import Optional

from pydantic_settings import BaseSettings
import os
import json


class Settings(BaseSettings):
    production_database_url: str
    testing_database_url:str
    superuser:dict
    #don't change this very important for Github Secret variables
    rsa_private_key:str
    rsa_public_key:str

    jwt_algorithm: str
    jwt_exp_minutes: int
    jwt_exp_days: int

    model_config = {
        "env_file": None if os.environ.get("ENVIRONMENT") == "Testing" else ".env",
    }
    def load_runtime_values(self):
        raw = os.getenv("SUPERUSER")
        if raw:
            try:
                self.superuser = json.loads(os.getenv("SUPERUSER"))
            except json.decoder.JSONDecodeError as e:
                raise ValueError(f"Invalid SUPERUSER JSON: {e}")
        self.rsa_private_key = os.getenv("RSA_PRIVATE_KEY")
        self.rsa_public_key = os.getenv("RSA_PUBLIC_KEY")
settings = Settings()
settings.load_runtime_values()