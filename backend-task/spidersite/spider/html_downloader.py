import urllib.request as urllib2


class HTMLDownloader:
    def download(self, url) -> str:
        if url is None:
            return None
        request = urllib2.Request(url)
        request.add_header('user-agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request)
        if response.getcode() != 200:
            return None
        return response.read()
