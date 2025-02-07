import os
from dotenv import load_dotenv

load_dotenv()

class Config:  # Base config class for all environments

    SECRET_KEY = os.environ.get("SECRET_KEY")

    BGG_API_ENDPOINT = "https://www.boardgamegeek.com/xmlapi2/"
    BGG_API_DELAY = 1  # Currently unsure of the rate limit, so I'm keeping it at 1 for now because I know this works with low traffic

    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    ENV = "production"

class TestingConfig(Config):
    TESTING = True
    ENV = "testing"

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": ProductionConfig
}
