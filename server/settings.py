import os

from decouple import Config, config
from dotenv import load_dotenv

load_dotenv()

DB_TYPE: str = config("DB_TYPE")
DB_NAME: str = config("DB_NAME")
DB_USER: str = config("DB_USER")
DB_PASSWORD: str = config("DB_PASSWORD")
DB_HOST: str = config("DB_HOST")
DB_PORT: int = config("DB_PORT")
SECRET_KEY : str = config("SECRET_KEY")