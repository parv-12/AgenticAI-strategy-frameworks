import requests
import json
import hashlib
import logging
from urllib.parse import urljoin, urlparse
import os
from bs4 import BeautifulSoup


try:
    from embedchain.helpers.json_serializable import register_deserializable
    from embedchain.loaders.base_loader import BaseLoader
    from embedchain.utils.misc import clean_string
except ImportError:
    raise ImportError(
        'Webpage requires extra dependencies. Install with `pip install --upgrade "embedchain[dataloaders]"`'
    ) from None


crawler_url = "http://localhost:7002/browseddg"
crawler_output_path = "C:/Users/Dell/Downloads/Strategic_planning_siemens/spider_crawler/spider/out"


def web_crawler(start_url, max_depth=0): #TODO filter content if max depth > 0

    try:
        loader = WebPageLoader()
        crawled_content = loader.crawl_pages(start_url, max_depth)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        WebPageLoader.close_session()

    return crawled_content[start_url]

def get_links(start_url): #TODO filter content if max depth > 0

    try:
        loader = WebPageLoader()
        links = loader.fetch_links(start_url)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        WebPageLoader.close_session()

    return links

def pdf_from_web(start_url, folder_location):
    folder_location = r'D:\UserData\z0049n3z\Patents and research\12. AI for strategy planning\strategic_intelligence\app\utils\pdf_web'
    # if not os.path.exists(folder_location):os.mkdir(folder_location)

    for url in start_url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select("a[href$='.pdf']"):
            filename = os.path.join(folder_location, link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url, link['href'])).content)


@register_deserializable
class WebPageLoader(BaseLoader):
    _session = requests.Session()

    def load_data(self, url):
          headers = {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
          }
          response = self._session.get(url, headers=headers, timeout=30)
          response.raise_for_status()
          data = response.content
          content = self._get_clean_content(data, url)

          meta_data = {"url": url}

          doc_id = hashlib.sha256((content + url).encode()).hexdigest()
          return {
              "doc_id": doc_id,
              "data": [
                  {
                      "content": content,
                      "meta_data": meta_data,
                  }
              ],
          }

    @staticmethod
    def _get_clean_content(html, url) -> str:
        soup = BeautifulSoup(html, "html.parser")
        original_size = len(str(soup.get_text()))

        tags_to_exclude = [
            "nav",
            "aside",
            "form",
            "header",
            "noscript",
            "svg",
            "canvas",
            "footer",
            "script",
            "style",
        ]
        for tag in soup(tags_to_exclude):
            tag.decompose()

        ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
        for id_ in ids_to_exclude:
            tags = soup.find_all(id=id_)
            for tag in tags:
                tag.decompose()

        classes_to_exclude = [
            "elementor-location-header",
            "navbar-header",
            "nav",
            "header-sidebar-wrapper",
            "blog-sidebar-wrapper",
            "related-posts",
        ]
        for class_name in classes_to_exclude:
            tags = soup.find_all(class_=class_name)
            for tag in tags:
                tag.decompose()

        content = soup.get_text()
        content = clean_string(content)

        cleaned_size = len(content)
        if original_size != 0:
            logging.info(
                f"[{url}] Cleaned page size: {cleaned_size} characters, down from {original_size} (shrunk: {original_size-cleaned_size} chars, {round((1-(cleaned_size/original_size)) * 100, 2)}%)"
            )

        return content

    @classmethod
    def fetch_links(cls, url):
        """
        Extract all links from a given URL.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
        response = cls._session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True)]
        return [urljoin(url, link) for link in links]

    @classmethod
    def crawl_pages(cls, start_url, max_depth=3, visited=None, current_depth=0):
        """
        Crawl multiple pages starting from a given URL with a maximum depth.
        """
        crawled_content = {}
        if visited is None:
            visited = set()

        if current_depth > max_depth:
            return

        if start_url not in visited:
            visited.add(start_url)
            try:
                loader = WebPageLoader()
                data = loader.load_data(start_url)
                content = data["data"][0]["content"]
                # print(f"Content from {start_url}:\n{content}\n")
                crawled_content[start_url]=content
            except Exception as e:
                print(f"An error occurred while processing {start_url}: {str(e)}")

            # Fetch links and recursively crawl
            links = cls.fetch_links(start_url)
            for link in links:
              cls.crawl_pages(link, max_depth, visited, current_depth + 1)

        return crawled_content
    

    

    @classmethod
    def close_session(cls):
        cls._session.close()