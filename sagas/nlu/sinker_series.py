from typing import Text, Any, Dict, List, Union
import logging
logger = logging.getLogger(__name__)

class SeriesStore(object):
    def __init__(self):
        from influxdb import InfluxDBClient
        self.client = InfluxDBClient('localhost', 8086, 'root', '', 'events')

    def all_db(self):
        return self.client.get_list_database()

    def post(self, measurement:Text, tags:Dict[Text,Any], fields:Dict[Text,Any]):
        json_body = [
            {
                "measurement": measurement,
                "tags": tags,
                # "time": "2017-03-12T22:00:00Z",
                "fields": fields
            }
        ]
        self.client.write_points(json_body)

series_store=SeriesStore()

class SeriesCli(object):
    def measurements(self):
        client=series_store.client
        result = client.query("show measurements;")
        print("Result: {0}".format(result))

    def events(self, provider):
        """
        $ python -m sagas.nlu.sinker_series events 'events'
        :param provider:
        :return:
        """
        qs = f"select * from {provider};"
        client = series_store.client
        result = client.query(qs)
        print("Result: {0}".format(result))

if __name__ == '__main__':
    import fire
    fire.Fire(SeriesCli)

