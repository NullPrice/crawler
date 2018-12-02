from crawler.crawler import Crawler
import os
import json

url = os.getenv('CRAWLER_TARGET_URL')
output_path = os.getenv('CRAWLER_OUTPUT_PATH')
tags = json.loads(os.getenv('CRAWLER_TARGET_TAGS', '["a", "img", "script"]'))
if not url:
    raise NameError('CRAWLER_TARGET_URL env var not set')
if not output_path:
    raise NameError('CRAWLER_OUTPUT_PATH env var not set')
crawl = Crawler(url, output_path, tags)
crawl.start()
