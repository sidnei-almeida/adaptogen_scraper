#!/usr/bin/env python3
"""
Adaptogen URL collector.

Fetches product page URLs across Adaptogen storefront categories.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

BASE_URL = "https://adaptogen.com.br"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}
REQUEST_DELAY = 2  # seconds between consecutive HTTP requests


def get_page(url: str) -> BeautifulSoup:
    """
    Fetch a URL and return a BeautifulSoup document.

    Raises:
        requests.RequestException: on transport or HTTP failure.
    """
    try:
        logger.info(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)
        return BeautifulSoup(response.content, "lxml")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        raise


def extract_product_urls(soup: BeautifulSoup, base_url: str = BASE_URL) -> List[str]:
    """
    Extract absolute product URLs from a listing/category page HTML.
    """
    urls = []

    links = soup.find_all("a", class_="woocommerce-LoopProduct-link")

    if not links:
        links = soup.find_all("a", href=True)
        links = [link for link in links if "/produto/" in link.get("href", "")]

    for link in links:
        href = link.get("href")
        if href:
            if href.startswith("http"):
                urls.append(href)
            elif href.startswith("/"):
                urls.append(f"{base_url}{href}")
            else:
                urls.append(f"{base_url}/{href}")

    seen = set()
    unique: List[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)

    return unique


def scrape_pre_workout() -> List[str]:
    """Collect URLs from the Pre-workout category."""
    logger.info("Crawling pre-workout category...")
    url = f"{BASE_URL}/pre-treino"

    try:
        soup = get_page(url)
        urls = extract_product_urls(soup)
        logger.info(f"{len(urls)} pre-workout products found")
        return urls
    except Exception as e:
        logger.error(f"Pre-workout scrape failed: {e}")
        return []


def scrape_snacks() -> List[str]:
    """Collect URLs from protein snacks listing."""
    logger.info("Crawling protein snacks...")
    url = f"{BASE_URL}/proteinas/snacks-proteicos/"

    try:
        soup = get_page(url)
        urls = extract_product_urls(soup)
        logger.info(f"{len(urls)} snack products found")
        return urls
    except Exception as e:
        logger.error(f"Snacks scrape failed: {e}")
        return []


def scrape_creatine() -> List[str]:
    """Collect URLs from the creatine category."""
    logger.info("Crawling creatine...")
    url = f"{BASE_URL}/creatina/"

    try:
        soup = get_page(url)
        urls = extract_product_urls(soup)
        logger.info(f"{len(urls)} creatine products found")
        return urls
    except Exception as e:
        logger.error(f"Creatine scrape failed: {e}")
        return []


def scrape_proteins() -> List[str]:
    """
    Paginate `/proteinas/` with `sf_paged` query param until WooCommerce stops.

    Pagination ends when Portuguese empty-state headline appears (Brazilian storefront copy).
    """
    logger.info("Crawling proteins (paginated)...")
    collected: List[str] = []
    page = 1

    while True:
        url = f"{BASE_URL}/proteinas/?sf_paged={page}"

        try:
            soup = get_page(url)

            empty = soup.find("h3", string="Nenhum produto encontrado")
            if empty:
                logger.info(f"Reached end of pagination at page={page}")
                break

            page_urls = extract_product_urls(soup)

            if not page_urls:
                logger.info(f"No products on page {page}; assuming end of pagination")
                break

            collected.extend(page_urls)
            logger.info(f"Page {page}: {len(page_urls)} products")
            page += 1

        except Exception as e:
            logger.error(f"Protein pagination failed at page={page}: {e}")
            break

    unique = list(set(collected))
    logger.info(f"Total protein products collected (deduped): {len(unique)}")
    return unique


def save_to_json(data: Dict[str, List[str]], filepath: str) -> None:
    """Persist category → URL arrays to UTF-8 JSON."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Wrote JSON to {filepath}")
    except Exception as e:
        logger.error(f"JSON write failed: {e}")
        raise


def main() -> None:
    """Orchestrate all category crawls."""
    logger.info("Starting Adaptogen product URL crawl...")

    product_urls = {
        "pre-treino": scrape_pre_workout(),
        "snacks": scrape_snacks(),
        "proteinas": scrape_proteins(),
        "creatinas": scrape_creatine(),
    }

    grand_total = sum(len(u) for u in product_urls.values())
    logger.info(f"\n{'=' * 50}")
    logger.info("CRAWL SUMMARY")
    logger.info(f"{'=' * 50}")
    for category, urls in product_urls.items():
        logger.info(f"{category}: {len(urls)} URLs")
    logger.info(f"Total: {grand_total}")
    logger.info(f"{'=' * 50}\n")

    out = "json/produtos_urls.json"
    save_to_json(product_urls, out)
    logger.info("URL crawl finished successfully.")


if __name__ == "__main__":
    main()
