<!-- Repository: https://github.com/sidnei-almeida/adaptogen_scraper -->
<p align="center">
  <img src="images/logo.png" alt="Adaptogen Scraper — CLI banner" width="520" />
</p>

<h1 align="center">adaptogen-scraper</h1>

<p align="center">
  <strong>Terminal CLI to harvest Adaptogen storefront URLs (adaptogen.com.br) and scrape structured nutrition panels into JSON + CSV.</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" /></a>
  <img src="https://img.shields.io/badge/requests-HTTP-0071C5?style=flat-square" alt="requests" />
  <img src="https://img.shields.io/badge/BeautifulSoup4-parse-FFD43B?style=flat-square&logo=python&logoColor=black" alt="BeautifulSoup4" />
  <img src="https://img.shields.io/badge/lxml-parser-4479A1?style=flat-square" alt="lxml" />
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#gallery">Gallery</a> ·
  <a href="#features">Features</a> ·
  <a href="#requirements">Requirements</a> ·
  <a href="#installation--quick-start">Quick start</a> ·
  <a href="#cli-reference">CLI</a> ·
  <a href="#data-pipeline">Data</a> ·
  <a href="#project-layout">Layout</a> ·
  <a href="#troubleshooting">Troubleshooting</a> ·
  <a href="#author">Author</a> ·
  <a href="#license">License</a>
</p>

---

## Overview

**adaptogen-scraper** automates a two-phase workflow: crawl **listing pages** back into product PDP links, then open each PDP and parse the **`div.flow` nutrition table**. Numbers are normalized, missing cells become `0`, and everything lands in CSV for spreadsheet analytics.

| Stage | Output |
|-------|--------|
| **URL crawl** | [`json/produtos_urls.json`](json/produtos_urls.json) with arrays per storefront bucket (pre-workout `pre-treino`, snacks, paginated proteins, creatine `creatinas`). |
| **Nutrition scrape** | [`dados_extraidos/produtos_nutricionais.csv`](dados_extraidos/produtos_nutricionais.csv) with servings, macros, timestamp, Brazilian category slug. |
| **Operator UX** | English [`main.py`](main.py) TUI wraps both stages, inventories artifacts, offers destructive cleanup behind `CONFIRM`. |

Scripts send **desktop-style headers** and honor a **2 s stall** (`REQUEST_DELAY` in [`url_collector.py`](url_collector.py) / [`nutritional_scraper.py`](nutritional_scraper.py)). This codebase is intentionally **tutorial / hobby** material—follow the site's terms of service plus any applicable scraping law before running it broadly.

---

## Gallery

### CLI banner (`images/logo.png`)

<p align="center">
  <img src="images/logo.png" alt="Adaptogen Scraper ASCII banner screenshot" width="780" />
</p>

<p align="center">
  <em><strong>Figure 1.</strong> Title card showing version headline and headline capabilities.</em>
</p>

### Full interactive menu (`images/software.png`)

<p align="center">
  <img src="images/software.png" alt="Adaptogen Scraper numbered menu screenshot" width="780" />
</p>

<p align="center">
  <em><strong>Figure 2.</strong> Root menu spanning collect / extract / full run / bookkeeping options.</em>
</p>

> **Note:** If you refresh the screenshots, re-record after switching the CLI to English so marketing assets mirror the codebase.

---

## Features

| Area | Details |
|------|---------|
| **Colored CLI** | [`main.py`](main.py) centralizes confirmations, pacing bars, ASCII panels. |
| **Pagination** | Proteins scrape walks `sf_paged` until WooCommerce emits the localized empty headline `Nenhum produto encontrado`. |
| **Robust PDP parsing** | Regex + XPath-style BeautifulSoup probing for servings text & Portuguese nutrient captions that match storefront copy. |
| **Dual ergonomics** | Drive everything through the CLI **or** run [`url_collector.py`](url_collector.py) + [`nutritional_scraper.py`](nutritional_scraper.py) headlessly. |
| **Template artifact** | [`template_main.py`](template_main.py) clones the stylistic scaffolding for unrelated CLIs. |

---

## Requirements

| Component | Notes |
|-----------|-------|
| **Python** | 3.10+ recommended (stdlib + typing friendly). |
| **Packages** | `requests`, `beautifulsoup4`, `lxml` pinned under [`requirements.txt`](requirements.txt). |
| **Network** | Reliable HTTPS egress to https://adaptogen.com.br |

> **Operational caveat:** storefront HTML drift means selectors occasionally need patching—coordinate issues with reproducible PDP URLs + HTML excerpts.

---

## Installation & quick start

```bash
git clone https://github.com/sidnei-almeida/adaptogen_scraper.git
cd adaptogen_scraper

python -m venv venv
source venv/bin/activate  # Linux / macOS
# .\venv\Scripts\activate on Windows PowerShell

pip install -r requirements.txt

python main.py
```

For a turnkey run, choose **Option 3 — Full pipeline**.

---

## CLI reference

### Interactive entrypoint

```bash
python main.py
```

| Hotkey | Behavior |
|--------|----------|
| **1** | Crawl storefront categories → populate `json/produtos_urls.json` |
| **2** | Read each stored URL → `dados_extraidos/produtos_nutricionais.csv` |
| **3** | Chain **1** then **2** |
| **4** | Summarize timestamps + weights for artifacts |
| **5** | Erase JSON / CSV payloads after typing **`CONFIRM`** |
| **6** | Credits + stack rundown |
| **7** | Exit |

### Scripted / cron usage

Equivalent to Menu **3**:

```bash
python url_collector.py
python nutritional_scraper.py
```

---

## Data pipeline

### URL index (`json/produtos_urls.json`)

Portuguese storefront keys intentionally mirror Adaptogen taxonomy:

```json
{
  "pre-treino": ["https://..."],
  "snacks": ["https://..."],
  "proteinas": ["https://..."],
  "creatinas": ["https://..."]
}
```

### Nutrition CSV (`dados_extraidos/produtos_nutricionais.csv`)

Columns originate from [`nutritional_scraper.CSV_COLUMNS`](nutritional_scraper.py):

| Column | Meaning |
|--------|---------|
| `nome`, `url` | Title pulled from PDP + canonical link |
| `porcao` | Localized servings string when detected |
| `calorias` … `sodio` | Float metrics; blanks coerced to zero |
| `data_coleta` | ISO-ish timestamp stamped per row scrape |
| `categoria` | Source bucket reused from JSON key |

---

## Project layout

```
.
├── main.py                   # Interactive English CLI
├── url_collector.py          # Listing → JSON crawler
├── nutritional_scraper.py    # PDP → CSV scraper
├── template_main.py          # Reusable menu skeleton
├── json/
│   └── produtos_urls.json    # Produced by crawler
├── dados_extraidos/
│   └── produtos_nutricionais.csv  # Produced by PDP pass
├── images/
│   ├── logo.png             # Banner capture
│   └── software.png         # Whole-menu screenshot
├── requirements.txt
└── README.md
```

Artifacts directories may be absent until the first successful run—the writers create files as paths resolve.

---

## Troubleshooting

| Symptom | Checks |
|---------|--------|
| Option **2** can't find URLs | Confirm **1** or `url_collector.py` finished; verify `json/produtos_urls.json`. |
| Zero URLs inside a bucket | Inspect HTML for WooCommerce markup drift (`woocommerce-LoopProduct-link` fallbacks still fail). |
| Logs show missing nutrition panels | PDP may relocate markup outside `div.flow`; adjust [`parse_nutritional_table`](nutritional_scraper.py). |
| HTTP slowdowns | Keep delay; investigate `429`, TLS inspection, corp proxies. |

---

## Author

| | |
| --- | --- |
| **Maintainer** | [Sidnei Almeida](https://github.com/sidnei-almeida) ([@sidnei-almeida](https://github.com/sidnei-almeida)) |
| **Repository** | [github.com/sidnei-almeida/adaptogen_scraper](https://github.com/sidnei-almeida/adaptogen_scraper) |
| **LinkedIn** | [linkedin.com/in/saaelmeida93](https://www.linkedin.com/in/saaelmeida93/) |

---

## Contributing

Issues & PRs welcome—please attach PDP HTML excerpts, storefront headlines, failing URLs, interpreter version, plus `beautifulsoup4`/`lxml` releases when reporting parser drift.

---

## License

Distributed as **community / educational OSS**. There is no packaged `LICENSE` file yet—add one (MIT, etc.) whenever you formalize redistribution terms.

---

<p align="center">
  <sub>Unaffiliated hobby project—not endorsed by Adaptogen®, WooCommerce®, or scraped trademarks.</sub>
</p>
