import boto3

from app.common.tls import custom_ca_certs
from app.config import config
from logging import getLogger
from sqlalchemy import create_engine, Engine, URL, text
from sqlalchemy.event import listen

logger = getLogger(__name__)

engine: Engine = None

def get_sql_engine() -> Engine:
    global engine

    if engine is not None:
        return engine
    
    url = URL.create(
        drivername="postgresql+psycopg",
        username=config.postgres_user,
        host=config.postgres_host,
        port=config.postgres_port,
        database=config.postgres_db
    )

    cert = custom_ca_certs.get(config.rds_truststore)

    if cert:
        logger.info("Creating Postgres SQLAlchemy engine with custom TLS cert %s", config.rds_truststore)
        engine = create_engine(
            url,
            connect_args={
                "sslmode": "require",
                "sslrootcert": cert
            }
        )
    else:
        logger.info("Creating Postgres SQLAlchemy engine")
        engine = create_engine(url)

    listen(engine, "do_connect", get_token)

    logger.info("Testing Postgres SQLAlchemy connection to %s", config.postgres_host)
    check_connection(engine)

    return engine


def check_connection(engine: Engine) -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def get_token(dialect, conn_rec, cargs, cparams):
    print(config.aws_region)
    if config.python_env == "development":
        cparams["password"] = config.postgres_password
    else:
        client = boto3.client("rds")

        token = client.generate_db_auth_token(
            Region=config.aws_region,
            DBHostname=config.postgres_host,
            Port=config.postgres_port,
            DBUsername=config.postgres_user
        )

        cparams["password"] = token
