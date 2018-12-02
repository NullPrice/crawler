from crawler.crawler import Crawler

# TODO: Either environment variables here or CLI args
crawl = Crawler('https://example.org/', './output')
crawl.start()
