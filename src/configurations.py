from os import getenv
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


# Base Configurations
class BaseConfig:
    DEBUG = True
    TESTING = False

    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(getenv("JWT_REFRESH_TOKEN_EXPIRES")))

    API_TITLE = "Forum API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/api/v1/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Development Configurations
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{getenv('DATABASE_USERNAME')}:{getenv('DATABASE_PASSWORD')}@{getenv('DATABASE_HOST')}:{getenv('DATABASE_PORT')}/{getenv('DATABASE_NAME')}"


# Staging Configurations
class StagingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


# Production Configurations
class ProductionConfig(BaseConfig):
    DEBUG = False
