import os

class Config:
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class TestingConfig():
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    OPENAI_API_KEY = "this_is_a_fake_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    TESTING = True

class ProductionConfig(Config):
    url = os.environ.get("DATABASE_URL")

    if url is not None and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = url
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")