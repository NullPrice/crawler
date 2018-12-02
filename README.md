# Crawler

This is a python crawler using requests for fetching content and Beautiful Soup for parsing.

## Requirements
- Python 3.7

## Usage

### Environment variables

- `CRAWLER_TARGET_URL` - The target url that you want to crawl
    - Example: `https://example.org`
- `CRAWLER_OUTPUT_PATH` - Output path for url content
    - Example: `/home/user/crawler-output`
- `CRAWLER_TARGET_TAGS` - A JSON list of tags in the found content that you want the crawler to parse and save
    -  Example: `["a", "img", "script"]`
    -  Limitation: Only tags with a `src` attribute will be successfully crawled. `a` tags will also work

### Via Docker (Recommended)

Build the docker image:

```bash
docker build -t crawler .
```

Run a container from the image with env vars you want (Make sure to volume the output somewhere):

```bash
docker run --rm -e CRAWLER_TARGET_URL='https://www.example.org' -e CRAWLER_OUTPUT_PATH='/output' -e CRAWLER_TARGET_TAGS='["a", "img", "script"]' -v $(pwd)/output:/output crawler
```


### Locally

Make sure you are using Python 3.7

pip install dependencies:

```bash
pip install -r requirements.txt
```

Run the crawler with your configured env vars:

```bash
 CRAWLER_TARGET_URL='https://www.example.org' CRAWLER_OUTPUT_PATH='/output' CRAWLER_TARGET_TAGS='["a", "img", "script"]' python main.py
```

## Limitations and bugs

- Crawler will only pull content from the domain you specify, this in intentional
- There is no depth control, so if you crawl a very large site on some specific file systems it will not be able to build the output directory nessessary to store all of its contents
- Redirects are handled silently, which means that if it does find some content and it has to redirect to grab it, you will not be aware of that from the crawl output
- Only `a, script, img` tags have been tested to work. Your millage will vary with other tags
- Single threaded
