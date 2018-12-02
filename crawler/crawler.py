import pathlib
import os
import uuid
import urllib
from .process import Process


class Crawler:
    def __init__(self, domain, output_dir, tags=['a']):
        self.domain = domain
        self.tags = tags
        self.crawl_id = uuid.uuid4()
        self.output_dir = os.path.abspath("{}/{}/".format(
            output_dir, self.crawl_id))
        self.queue = {urllib.parse.urlparse(self.domain)}
        self.processed = set()

    def _create_output_dir(self):
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def _save_crawled_content(self, page):
        output_file = None

        # If raw page content instead of script or content with a suffix
        if page.content:
            if pathlib.Path(page.url_parse.path).suffix == '':
                output_file = self.output_dir + "{}/index.html".format(
                    urllib.parse.quote(page.url_parse.hostname +
                                       page.url_parse.path))
            else:
                output_file = self.output_dir + "{}/{}".format(
                    urllib.parse.quote(page.url_parse.hostname),
                    urllib.parse.quote(page.url_parse.path))
            # import pdb
            # pdb.set_trace()
            # print("Makedir: {}".format(os.path.dirname(output_file)))
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(str(page.content))

    def _process_found_content(self, page):
        """
        Ensure 'found' content has not already been found
        """
        for tag in page.processed_tags:
            if tag not in self.processed and tag not in self.queue:
                self.queue.add(tag)

    def start(self):
        """
        Starts the crawl run
        """
        self._create_output_dir()
        print("Crawl ID: {} Beginning crawl of: {}".format(
            self.crawl_id, self.domain))

        while len(self.queue) != 0:
            # Grab first URL from list
            page = Process(self.queue.pop(), self.tags)
            # Process the URL given
            page.process()
            # Save content to directory based on URL
            self._save_crawled_content(page)
            # Append crawled page onto processed
            self.processed.add(page.url_parse)
            # Append new tags to queue
            self._process_found_content(page)
