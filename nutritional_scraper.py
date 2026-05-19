#!/usr/bin/env python3
"""
Adaptogen nutritional facts scraper.

Visits individual product URLs and emits a flattened CSV snapshot.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}
REQUEST_DELAY = 2  # seconds between requests

CSV_COLUMNS = [
    "nome",
    "url",
    "porcao",
    "calorias",
    "carboidratos",
    "proteinas",
    "gorduras",
    "gorduras_saturadas",
    "gorduras_trans",
    "fibras",
    "acucares",
    "acucares_adicionados",
    "sodio",
    "data_coleta",
    "categoria",
]


def load_product_urls(filepath: str = "json/produtos_urls.json") -> Dict[str, List[str]]:
    """Load categorized product URLs exported by ``url_collector``."""
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded URLs from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Unable to load URL index: {e}")
        raise


def get_page(url: str) -> Optional[BeautifulSoup]:
    """GET a product page HTML and return Soup, swallowing transient HTTP errors."""
    try:
        logger.info(f"GET {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)
        return BeautifulSoup(response.content, "lxml")
    except requests.RequestException as e:
        logger.error(f"HTTP error for {url}: {e}")
        return None


def extract_product_name(soup: BeautifulSoup) -> str:
    """Best-effort product title from PDP markup."""
    selectors = (
        "h1.product_title",
        "h1.product-title",
        "h1",
        ".product-title",
        ".product_title",
    )

    for sel in selectors:
        node = soup.select_one(sel)
        if node:
            return node.get_text(strip=True)

    return "Name not found"


def clean_numeric_value(value: str) -> float:
    """Parse localized numeric nutrient strings → float; blanks become 0.0."""
    if not value or value.strip() == "":
        return 0

    cleaned = value.strip().replace(",", ".")
    match = re.search(r"[\d.]+", cleaned)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return 0

    return 0


def extract_portion(table) -> str:
    """
    Extract serving/portions text tailored to Adaptogen PDP tables (`Porção:` lines).

    Table copy remains Portuguese on the storefront; regex anchors must match PT wording.
    """
    patterns = [
        r"Porção:\s*(\d+\s*g\s*\([^)]+\))",
        r"Porção:\s*(\d+\s*g)",
        r"Porção:\s*(\d+\s*g\s*\(\d+\s*unidade[s]?\))",
        r"Porção:\s*(.+?)(?:\n|<|$)",
        r"Porção de\s+(.+?)(?:\n|<|$)",
        r"Porção\s+de\s+(.+?)(?:\n|<|$)",
        r"Porção\s+(.+?)(?:\n|<|$)",
    ]

    thead = table.find("thead")
    if thead:
        colspan_th = thead.find("th", {"colspan": True})
        if colspan_th:
            for elem in colspan_th.find_all(["strong", "p"]):
                text = elem.get_text()
                for pattern in patterns:
                    m = re.search(pattern, text, re.IGNORECASE)
                    if m:
                        txt = " ".join(m.group(1).strip().split())
                        return txt

            text_full = colspan_th.get_text()
            for pattern in patterns:
                m = re.search(pattern, text_full, re.IGNORECASE)
                if m:
                    return " ".join(m.group(1).strip().split())

        for th in thead.find_all("th"):
            txt = th.get_text()
            for pattern in patterns:
                m = re.search(pattern, txt, re.IGNORECASE)
                if m:
                    return " ".join(m.group(1).strip().split())

    tbody = table.find("tbody")
    if tbody:
        row0 = tbody.find("tr")
        if row0:
            for cell in row0.find_all(["td", "th"]):
                text = cell.get_text()
                if "porção" in text.lower():
                    for pattern in patterns:
                        m = re.search(pattern, text, re.IGNORECASE)
                        if m:
                            return " ".join(m.group(1).strip().split())

                    if "de" in text.lower():
                        chunks = text.split("de", 1)
                        if len(chunks) > 1:
                            return " ".join(chunks[1].strip().split())

                    stripped = (
                        text.replace("Porção", "")
                        .replace("porção", "")
                        .strip()
                    )
                    stripped = " ".join(stripped.split())
                    if stripped:
                        return stripped

    return ""


def parse_nutritional_table(soup: BeautifulSoup) -> Optional[Dict]:
    """
    Parse the PDP nutrition table housed under ``div.flow``.

    Nutrient labels mirror Brazilian storefront wording; mapping keys intentionally stay Portuguese.
    """
    flow_div = soup.find("div", class_="flow")
    if not flow_div:
        logger.warning("Could not locate div.flow")
        return None

    table = flow_div.find("table")
    if not table:
        logger.warning("No nested <table> under div.flow")
        return None

    data = {
        "porcao": "",
        "calorias": 0,
        "carboidratos": 0,
        "proteinas": 0,
        "gorduras": 0,
        "gorduras_saturadas": 0,
        "gorduras_trans": 0,
        "fibras": 0,
        "acucares": 0,
        "acucares_adicionados": 0,
        "sodio": 0,
    }

    data["porcao"] = extract_portion(table)

    nutrient_mapping = {
        "valor energético": "calorias",
        "carboidratos": "carboidratos",
        "proteínas": "proteinas",
        "gorduras totais": "gorduras",
        "gorduras saturadas": "gorduras_saturadas",
        "gorduras trans": "gorduras_trans",
        "fibras alimentares": "fibras",
        "fibra alimentar": "fibras",
        "açúcares totais": "acucares",
        "açucares totais": "acucares",
        "açúcares adicionados": "acucares_adicionados",
        "açucares adicionados": "acucares_adicionados",
        "sódio": "sodio",
    }

    tbody = table.find("tbody")
    if tbody:
        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 2:
                nutrient_name = cells[0].get_text(strip=True).lower()
                nutrient_value = cells[1].get_text(strip=True)

                for key_sl, csv_key in nutrient_mapping.items():
                    if key_sl in nutrient_name:
                        data[csv_key] = clean_numeric_value(nutrient_value)
                        break

    return data


def scrape_product(url: str, categoria: str) -> Optional[Dict]:
    """Scrape a single PDP into a flattened row dict aligned with CSV_COLUMNS."""
    try:
        soup = get_page(url)
        if not soup:
            return None

        name = extract_product_name(soup)

        nutritional = parse_nutritional_table(soup)
        if not nutritional:
            logger.warning(f"No nutrition table for «{name}» ({url})")
            return None

        payload = {
            "nome": name,
            "url": url,
            "porcao": nutritional["porcao"],
            "calorias": nutritional["calorias"],
            "carboidratos": nutritional["carboidratos"],
            "proteinas": nutritional["proteinas"],
            "gorduras": nutritional["gorduras"],
            "gorduras_saturadas": nutritional["gorduras_saturadas"],
            "gorduras_trans": nutritional["gorduras_trans"],
            "fibras": nutritional["fibras"],
            "acucares": nutritional["acucares"],
            "acucares_adicionados": nutritional["acucares_adicionados"],
            "sodio": nutritional["sodio"],
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categoria": categoria,
        }

        logger.info(f"✓ scraped {name}")
        return payload

    except Exception as e:
        logger.error(f"{url}: {e}")
        return None


def save_to_csv(rows: List[Dict], filepath: str) -> None:
    """Write UTF-8 CSV with header row pulled from CSV_COLUMNS."""
    try:
        with open(filepath, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"CSV written to {filepath}")
    except Exception as e:
        logger.error(f"CSV write failed: {e}")
        raise


def main() -> None:
    """Batch-scrape products referenced inside ``produtos_urls.json``."""
    logger.info("Nutrition scrape starting...")

    try:
        by_category = load_product_urls()
    except Exception:
        logger.error("Aborting — run ``python url_collector.py`` (or CLI option 1) first.")
        return

    aggregated: List[Dict] = []
    total_urls = sum(len(lst) for lst in by_category.values())
    processed = success = failed = 0

    logger.info("\n%s", "=" * 60)
    logger.info("Products queued: %d", total_urls)
    logger.info("%s\n", "=" * 60)

    for category, urls in by_category.items():
        logger.info("\n%s", "=" * 60)
        logger.info("Category: %s", category.upper())
        logger.info("URLs in bucket: %d", len(urls))
        logger.info("%s\n", "=" * 60)

        for u in urls:
            processed += 1
            logger.info("[%d/%d]", processed, total_urls)

            row = scrape_product(u, category)

            if row:
                aggregated.append(row)
                success += 1
            else:
                failed += 1

    if aggregated:
        csv_path = "dados_extraidos/produtos_nutricionais.csv"
        save_to_csv(aggregated, csv_path)

    pct = (success / processed * 100) if processed else 0.0
    logger.info("\n%s", "=" * 60)
    logger.info("RUN SUMMARY")
    logger.info("%s", "=" * 60)
    logger.info("Processed: %d", processed)
    logger.info("Success: %d", success)
    logger.info("Failures: %d", failed)
    logger.info("Success rate: %.1f%%", pct)
    logger.info("%s\n", "=" * 60)
    logger.info("Done.")


if __name__ == "__main__":
    main()
