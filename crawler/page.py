import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Page:
    """
    Process a URL and validate / parse content
    """

    def __init__(self, url, tags):
        self.url = url
        self.tags = tags
        self.response_url = None
        self.response = None
        self.content = None
        self.soup = None
        self.processed_tags = set()
        self._reference_set = {'a': 'href'}

    def _get_url(self, timeout=10):
        try:
            self.response = requests.get(self.url.geturl(), timeout=timeout)
        except requests.exceptions.MissingSchema:
            # Crawler couldn't process a URL because of a missing schema
            self.response = requests.get(
                "https:{}".format(self.url.geturl()), timeout=timeout)

        if self.response.ok:
            if self.response.encoding:
                self.content = self.response.text
                self.soup = BeautifulSoup(self.response.text, "html.parser")
            else:
                # Assume binary content
                self.content = self.response.content
            self.response_url = urlparse(self.response.url)
            print("Crawled page: {}".format(self.url.geturl()))
        else:
            # TODO: May want to crawl response content other than 200
            self.response_url = urlparse(self.response.url)
            print("Response {} -- Failed to crawl page: {}".format(
                self.response.status_code, self.url.geturl()))

    def _parse_tags(self):
        """
        Parse our contents tags and filter what we don't care about
        """
        for target_tag in self.tags:
            attribute = self._reference_set.get(target_tag, 'src')
            found = self.soup.find_all(target_tag)
            for tag in found:
                # For each of the tag types we care about
                if tag.get(attribute):
                    parsed_tag = urlparse(tag.get(attribute))
                    if parsed_tag.hostname == self.response_url.hostname:
                        # Tag references / sources from current domain
                        self.processed_tags.add(parsed_tag)
                    elif parsed_tag.hostname is None:
                        # Tag is pointing to current domain
                        if not tag.get(attribute).startswith('/'):
                            corrected_url = urlparse(
                                "{}://{}/{}".format(self.response_url.scheme,
                                                    self.response_url.hostname,
                                                    tag.get(attribute)))
                            self.processed_tags.add(corrected_url)
                        else:
                            corrected_url = urlparse(
                                "{}://{}{}".format(self.response_url.scheme,
                                                   self.response_url.hostname,
                                                   tag.get(attribute)))
                            self.processed_tags.add(corrected_url)

    def process(self):
        self._get_url()
        if self.content and self.response.encoding:
            self._parse_tags()
