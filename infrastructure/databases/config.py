import os
from dotenv import load_dotenv
from pydantic import Field, BaseModel


load_dotenv()


class PostgresConfig(BaseModel):
    host: str = Field(default=os.getenv("POSTGRES_HOST"))
    port: int = Field(default=int(os.getenv("POSTGRES_PORT")))
    user: str = Field(default=os.getenv("POSTGRES_USER"))
    password: str = Field(default=os.getenv("POSTGRES_PASSWORD"))
    database: str = Field(default=os.getenv("POSTGRES_DB"))


class Config:
    env_file = "..env"