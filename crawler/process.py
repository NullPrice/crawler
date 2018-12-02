import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Process:
    """
    Process a URL and validate / parse content
    """

    def __init__(self, url, tags):
        self.url = url
        self.tags = tags
        self.url_parse = None
        self.response = None
        self.content = None
        self.soup = None
        self.processed_tags = set()
        self._reference_set = {'a': 'href'}

    def _get_url(self, timeout=10):
        print("Url object: {}".format(self.url))
        print("Getting url: {}".format(self.url.geturl()))
        try:
            self.response = requests.get(self.url.geturl(), timeout=timeout)
        except requests.exceptions.MissingSchema:
            # Crawler couldn't process a URL because of a missing schema
            self.response = requests.get(
                "https:{}".format(self.url.geturl()), timeout=timeout)

        if self.response.ok:
            # Always default to UTF-8 for page content
            # TODO: Decode won't work for binary content
            # Encoding will be empty if binary content
            self.content = self.response.content.decode('utf-8')
            self.soup = BeautifulSoup(self.response.content, "html.parser")
            self.url_parse = urlparse(self.response.url)
            print("Crawled page: {}".format(self.url.geturl()))
        else:
            # TODO: May want to crawl responses other than 200
            self.url_parse = urlparse(self.response.url)
            print("Response {} -- Failed to crawl page: {}".format(
                self.response.status_code, self.url.geturl()))

    def _parse_tags(self):
        """
        Parse our contents tags and filter what we don't care about
        """
        for tag in self.tags:
            attribute = self._reference_set.get(tag, 'src')
            found = self.soup.find_all(tag)
            for tag in found:
                if tag.get(attribute):
                    if urlparse(tag.get(
                            attribute)).hostname == self.url_parse.hostname:
                        if (urlparse(tag.get(attribute)).path == ''):
                            # Handle edgecase with trailing forward slash
                            parsed_url = urlparse(tag.get(attribute) + "/")
                            self.processed_tags.add(parsed_url)
                        else:
                            self.processed_tags.add(
                                urlparse(tag.get(attribute)))

    def process(self):
        self._get_url()
        if self.content:
            self._parse_tags()
