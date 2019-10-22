class URLsManager:

    def __init__(self):
        self.urls = set()
        self.new_urls = set()

    def addNewURL(self, url):
        if url is None:
            return
        if url not in self.urls:
            self.urls.add(url)
            self.new_urls.add(url)

    def addNewURLs(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.addNewURL(url)

    def hasNewURL(self) -> bool:
        return len(self.new_urls) != 0

    def getNewURL(self) -> str:
        return self.new_urls.pop()
