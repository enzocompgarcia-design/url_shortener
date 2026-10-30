from datetime import UTC, datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class LinksTableDb(Model):
    __keyspace__ = "link_shortener"

    short_link = columns.Text(primary_key=True)
    long_link = columns.Text(required=True)
    created_at = columns.DateTime(default=lambda: datetime.now(UTC))
