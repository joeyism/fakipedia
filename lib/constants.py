import os

MAX_TEXT_LENGTH = os.getenv("MAX_TEXT_LENGTH", 1024)
DEFAULT_MODEL_MEMORY = os.getenv("DEFAULT_MODEL_MEMORY", 200)
DB_URL = os.getenv("DB_URL")
GPT2_NAME = os.getenv('GPT2_NAME', 'gpt2-medium')
ENV = os.getenv("ENV")
