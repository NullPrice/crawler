import pathlib
import os
import uuid
import urllib
from .page import Page


class Crawler:
    def __init__(self, domain, output_dir, tags):
        self.domain = domain
        self.tags = tags
        self.crawl_id = uuid.uuid4()
        self.output_dir = os.path.abspath("{}/{}/".format(
            output_dir, self.crawl_id))
        self.queue = {urllib.parse.urlparse(self.domain)}
        self.processed = set()

    def _create_output_dir(self):
        """
        Creates our crawl output directory
        """
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def _save_crawled_content(self, page):
        """
        Takes the found content and writes it into the output directory
        """
        output_file = None

        if page.content:
            if pathlib.Path(page.response_url.path).suffix == '':
                # If raw page content instead of a suffixed specific file
                output_file = self.output_dir + "/{}/index.html".format(
                    page.response_url.hostname + page.response_url.path)
            else:
                output_file = self.output_dir + "/{}/{}".format(
                    page.response_url.hostname, page.response_url.path)

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "wb") as f:
                f.write(page.response.content)

    def _process_found_content(self, page):
        """
        Ensure 'found' content has not already been found
        """
        found_tag_count = len(page.processed_tags)
        tag_count = 0
        for tag in page.processed_tags:
            if tag not in self.processed and tag not in self.queue:
                self.queue.add(tag)
                tag_count += 1
        print("Added {} URLs to the queue out of {} found URLs".format(
            tag_count, found_tag_count))

    def _process_crawled_page(self, page):
        """
        Handle adding page to processed
        """
        self.processed.add(page.response_url)
        if page.url.geturl() != page.response_url.geturl():
            # A redirect occured so mark the original as processed too
            self.processed.add(page.url)

    def start(self):
        """
        Starts the crawl run
        """
        self._create_output_dir()
        print("Crawl ID: {} Beginning crawl of: {}".format(
            self.crawl_id, self.domain))
        print("Crawling tags: " + ", ".join(self.tags))

        while self.queue:
            print("URLs to crawl: {}".format(len(self.queue)))
            # Grab first URL from list
            page = Page(self.queue.pop(), self.tags)
            # Process the URL given
            page.process()
            # Save content to directory based on URL
            self._save_crawled_content(page)
            # Append crawled page onto processed
            self._process_crawled_page(page)
            # Append new tags to queue
            self._process_found_content(page)

        print("Crawl ID: {} Finished!. Crawled {} URLs".format(
            self.crawl_id, len(self.processed)))
