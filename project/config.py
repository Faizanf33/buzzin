import os

database_name = os.getenv("DATABASE_NAME")
database_username = os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")

database_url = os.getenv("DATABASE_URL")  # or other relevant config var
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

else:
    # set database url (default is sqlite)
    # sqlite:///:memory: (or, sqlite://)
    database_url = "sqlite:///{}.db".format(database_name)

    # mysql://username:password@host:port/database
    # database_url = "mysql://{}:{}@{}:{}/{}".format(
    #     database_username, database_password, host, port, database_name
    # )

    # postgresql://username:password@host:port/database
    # database_url = "postgresql://{}:{}@{}:{}/{}".format(
    #     database_username, database_password, host, port, database_name
    # )


class Config:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = database_url
    # Uncomment the following lines to use a MySQL database
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "pool_pre_ping": True,
    #     "pool_recycle": 280,
    #     "pool_size": 100,
    #     "max_overflow": 0,
    # }
    SECRET_KEY = "app_secret"
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
