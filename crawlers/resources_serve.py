from sanic import Sanic

app = Sanic(__name__)

class ResourcesServe(object):
    def serve(self):
        """
        $ python -m crawlers.resources_serve serve
        :return:
        """
        chunk_size = 1024 * 1024 * 8 # Set chunk size to 8KB
        app.static('/id_0198.mp3', '/pi/resources/id_0198.mp3',
                   stream_large_files=chunk_size)

        app.run(host="0.0.0.0", port=8000)

if __name__ == '__main__':
    import fire
    fire.Fire(ResourcesServe)

