from gql import Client, gql
import logging
from gql.transport.requests import log as requests_logger
requests_logger.setLevel(logging.WARNING)

class QlConnector(object):
    def __init__(self):
        from gql.transport.requests import RequestsHTTPTransport

        self.transport = RequestsHTTPTransport(
            url="http://127.0.0.1:8080/graphql",
            verify=False,
            retries=3,
        )
        self.client = Client(transport=self.transport, fetch_schema_from_transport=False)
        # self.client.schema

    def execute(self, query: str):
        return self.client.execute(gql(query))


