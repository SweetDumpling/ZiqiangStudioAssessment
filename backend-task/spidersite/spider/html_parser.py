from bs4 import BeautifulSoup
import re
from datetime import date
import urllib.parse as urlparse


class HTMLParser:
    def _getListURL(self, url, html) -> str:
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        divs = soup.find_all('div', class_='cont_nav')
        try:
            for div in divs:
                if re.search(r'学术动态', div.find('h3').get_text()) is None:
                    continue
                lecture_list_link = div.find(
                    'a', href=re.compile(r'newListLogic.shtml.+'))
                lecture_list_url = lecture_list_link['href']
                lecture_list_url = urlparse.urljoin(url, lecture_list_url)
                return lecture_list_url
        except:
            pass
        return None

    def _getAllListPages(self, url, html) -> {}:
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        try:
            text = soup.find('td', text=re.compile(r'共.+')).get_text()
            num = int(re.search(r'共1/(\d*)页', text).group(1))
            return {url + '&pageNumber=' + str(i) for i in range(1, num+1)}
        except:
            return None

    def _getLectureURLs(self, url, html) -> {}:
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        links = soup.find_all('a', href=re.compile(r'newsDetails_zw.shtml.+'))
        lecture_urls = set()
        for link in links:
            if re.search(r'讲座', link.get_text()) is not None:
                lecture_urls.add(urlparse.urljoin(url, link['href']))
        return lecture_urls

    def _getLectureDetails(self, url, html) -> {}:
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        text = re.sub(r'<[^<>]>', '', soup.get_text())
        text = re.sub(r'\xa0', '', text)
        try:
            page_title = soup.find_all('h3')[1].get_text()
        except:
            page_title = '未识别'
        try:
            title = re.search(r'(题目|主题)(：|:)(\r|\n)*([^\r\n]*)', text).group(4)
        except:
            title = '未识别'
        try:
            speaker = re.search(
                r'(报 ?告 ?人|演 ?讲 ?者|主 ?讲 ?人)(：|:)(\r|\n)*([^\r\n]*)', text).group(4)
        except:
            speaker = '未识别'
        try:
            temp = re.search(r'发布时间：\[(\d+)-(\d+)-(\d+)\]', text)
            announce_date = date(int(temp.group(1)), int(
                temp.group(2)), int(temp.group(3)))
        except:
            announce_date = date(1, 1, 1)
        try:
            time = re.search(
                r'(?<!发布)时间(：|:)(\r|\n)*([^\r\n]*)', text).group(3)
        except:
            time = '未识别'
        try:
            room = re.search(r'地点(：|:)(\r|\n)*([^\r\n]*)', text).group(3)
        except:
            room = '未识别'
        return {'url': url, 'page title': page_title, 'title': title, 'speaker': speaker,
                'time': time, 'room': room, 'announce date': announce_date}

    def parse(self, url, html) -> ():
        if url is None or html is None:
            return None
        elif re.search(r'newsDetails_zw.shtml', url) is not None:
            data = self._getLectureDetails(url, html)
            return (data, None)
        elif re.search(r'newListLogic.shtml.+&pageNumber', url) is not None:
            lecture_urls = self._getLectureURLs(url, html)
            return (None, lecture_urls)
        elif re.search(r'newListLogic.shtml', url) is not None:
            all_list_urls = self._getAllListPages(url, html)
            return (None, all_list_urls)
        elif re.search(r'index.shtml', url) is not None:
            list_url = self._getListURL(url, html)
            return (None, {list_url})
        else:
            return None
