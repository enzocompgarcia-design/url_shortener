from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from app.config import config
from app.database.cassandra.models import LinksTableDb


def create_tables():
    cluster = Cluster(
        [config.CASSANDRA_HOST],
        port=config.CASSANDRA_PORT,
    )

    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS link_shortener
        WITH replication = {
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }
    """)

    session.shutdown()
    cluster.shutdown()

    connection.setup(
        hosts=[config.CASSANDRA_HOST],
        default_keyspace="link_shortener",
        protocol_version=5,
    )

    sync_table(LinksTableDb)


def get_db():
    yield connection
