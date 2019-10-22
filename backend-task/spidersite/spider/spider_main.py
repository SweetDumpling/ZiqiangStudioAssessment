from .html_downloader import HTMLDownloader
from .html_parser import HTMLParser
from .urls_manager import URLsManager


class SpiderMain:

    def __init__(self):
        self.html_parser = HTMLParser()
        self.html_downloader = HTMLDownloader()
        self.urls_manager = URLsManager()

    def craw(self, url, n) -> {}:
        self.urls_manager.addNewURL(url)
        datas = list()
        for i in range(n):
            if not self.urls_manager.hasNewURL():
                break
            new_url = self.urls_manager.getNewURL()
            html = self.html_downloader.download(new_url)
            data, urls = self.html_parser.parse(new_url, html)
            if urls is not None and len(urls) != 0:
                self.urls_manager.addNewURLs(urls)
            if data is not None and len(data) != 0:
                datas.append(data)
        return datas
