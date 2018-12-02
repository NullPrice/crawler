from crawler.crawler import Crawler
import os
import json

url = os.environ.get('CRAWLER_TARGET_URL')
output_path = os.environ.get('CRAWLER_OUTPUT_PATH')
tags = json.loads(
    os.environ.get('CRAWLER_TARGET_TAGS', '["a", "img", "script"]'))
crawl = Crawler(url, output_path, tags)
crawl.start()
