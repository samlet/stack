class ResourcesDownloader(object):
    def download(self):
        """
        $ python -m crawlers.resources_downloader download
        :return:
        """
        import requests

        # url = "https://www.book2.nl/book2/ID/SOUND/0003.mp3"
        url="https://www.book2.nl/book2/ID/SOUND/0198.mp3"
        r = requests.get(url, allow_redirects=True)
        open('/pi/resources/id_0198.mp3', 'wb').write(r.content)

if __name__ == '__main__':
    import fire
    fire.Fire(ResourcesDownloader)

