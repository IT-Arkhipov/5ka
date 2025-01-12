from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    cookies: dict = Field(default_factory=dict)  # noqa
    location: str = ''
    sap_code: str = ''


settings = Settings()
