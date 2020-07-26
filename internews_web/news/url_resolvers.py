from urllib.parse import urlparse, urljoin


class UrlParser:

    def __init__(self, url: str):
        self.url_data = urlparse(url)

    @classmethod
    def apply_netloc_policy(cls, raw_netloc: str):
        return raw_netloc.replace("www.", "")

    @classmethod
    def join_urls(cls, url1: str, url2: str):
        return urljoin(url1, url2)

    @classmethod
    def url_is_absolute(cls, url):
        return "https:" in url or "http:" in url

    def get_netloc(self):
        return self.apply_netloc_policy(self.url_data.netloc)

    def get_relative_url(self):
        return self.url_data.path

    def get_base_url(self):
        return f"{self.url_data.scheme}://{self.get_netloc()}"

