#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adaptogen Scraper — terminal CLI

Interactive interface for collecting and extracting Adaptogen nutritional data.

Author: Sidnei Almeida (github.com/sidnei-almeida)
"""

import os
import sys
import time
import glob
from datetime import datetime
# ============================================================================
# ANSI COLORS FOR TERMINAL OUTPUT
# ============================================================================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'

# ============================================================================
# UTILITIES
# ============================================================================
def clear_screen():
    """Clear the terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Print the application banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║              Adaptogen Scraper — v1.0                        ║
║                                                              ║
║        Nutritional data extraction from Adaptogen            ║
║                                                              ║
║  Product URL collection                                       ║
║  Nutritional facts table parsing                             ║
║  Export to JSON & CSV                                         ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def print_progress_bar(message: str, duration_sec: float = 2.0):
    """Display an animated terminal progress bar."""
    print(f"\n{Colors.YELLOW}Waiting — {message}...{Colors.RESET}")
    bar_len = 40
    for i in range(bar_len + 1):
        progress = i / bar_len
        bar = "█" * i + "░" * (bar_len - i)
        pct = int(progress * 100)
        print(f"\r{Colors.GREEN}[{bar}] {pct}%{Colors.RESET}", end="", flush=True)
        time.sleep(duration_sec / bar_len)
    print()

def print_main_menu():
    """Print the main menu."""
    menu = f"""
{Colors.BLUE}{Colors.BOLD}══════════════════ MAIN MENU ══════════════════{Colors.RESET}

{Colors.GREEN}Primary actions:{Colors.RESET}
  {Colors.YELLOW}1.{Colors.RESET} Collect product URLs — all categories
  {Colors.YELLOW}2.{Colors.RESET} Extract nutritional tables — per product pages
  {Colors.YELLOW}3.{Colors.RESET} Full pipeline — collection + extraction

{Colors.GREEN}Data management:{Colors.RESET}
  {Colors.YELLOW}4.{Colors.RESET} List generated files — JSON & CSV artifacts
  {Colors.YELLOW}5.{Colors.RESET} Delete data files — clears json/ and dados_extraidos/

{Colors.GREEN}Info:{Colors.RESET}
  {Colors.YELLOW}6.{Colors.RESET} About — version, tech stack, output layout
  {Colors.YELLOW}7.{Colors.RESET} Quit

{Colors.BLUE}══════════════════════════════════════════════════════════{Colors.RESET}
"""
    print(menu)

def prompt_choice() -> str:
    """Read user's menu selection."""
    try:
        choice = input(f"{Colors.MAGENTA}Enter option (1-7): {Colors.RESET}").strip()
        return choice
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted.{Colors.RESET}")
        sys.exit(0)

# ============================================================================
# Adaptogen scraper workflows
# ============================================================================

def collect_urls():
    """Run URL collection."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}COLLECT PRODUCT URLS{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 60}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}Categories:{Colors.RESET}")
    print(f"   Pre-workout: {Colors.YELLOW}https://adaptogen.com.br/pre-treino{Colors.RESET}")
    print(f"   Protein snacks: {Colors.YELLOW}https://adaptogen.com.br/proteinas/snacks-proteicos/{Colors.RESET}")
    print(f"   Proteins (paginated): {Colors.YELLOW}https://adaptogen.com.br/proteinas/{Colors.RESET}")
    print(f"   Creatine: {Colors.YELLOW}https://adaptogen.com.br/creatina/{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}Output:{Colors.RESET} {Colors.YELLOW}json/produtos_urls.json{Colors.RESET}")
    
    reply = input(f"\n{Colors.MAGENTA}Start collection? (y/N): {Colors.RESET}").lower()
    
    if reply in {"y", "yes", "s", "sim"}:
        try:
            print_progress_bar("Starting URL crawl", 1.5)
            
            print(f"\n{Colors.GREEN}Running...{Colors.RESET}\n")
            print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}")
            
            import url_collector
            url_collector.main()
            
            print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}")
            print(f"\n{Colors.GREEN}URL collection finished.{Colors.RESET}")
            
        except Exception as e:
            print(f"\n{Colors.RED}Error during collection: {e}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")

def extract_nutrition():
    """Run nutritional scraping."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}EXTRACT NUTRITIONAL TABLES{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 60}{Colors.RESET}")
    
    if not os.path.exists("json/produtos_urls.json"):
        print(f"\n{Colors.RED}Missing json/produtos_urls.json.{Colors.RESET}")
        print(f"{Colors.YELLOW}Run option 1 (Collect URLs) first.{Colors.RESET}")
        return
    
    print(f"\n{Colors.YELLOW}Note:{Colors.RESET}")
    print(f"   This may take {Colors.RED}several minutes{Colors.RESET}.")
    print(f"   Each product page is fetched individually.")
    print(f"   A 2-second delay is applied between HTTP requests.")
    
    print(f"\n{Colors.GREEN}Input:{Colors.RESET} {Colors.YELLOW}json/produtos_urls.json{Colors.RESET}")
    print(f"{Colors.GREEN}Output:{Colors.RESET} {Colors.YELLOW}dados_extraidos/produtos_nutricionais.csv{Colors.RESET}")
    
    reply = input(f"\n{Colors.MAGENTA}Start extraction? (y/N): {Colors.RESET}").lower()
    
    if reply in {"y", "yes", "s", "sim"}:
        try:
            print_progress_bar("Preparing extraction", 1.5)
            
            print(f"\n{Colors.GREEN}Running...{Colors.RESET}\n")
            print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}")
            
            import nutritional_scraper
            nutritional_scraper.main()
            
            print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}")
            print(f"\n{Colors.GREEN}Extraction finished.{Colors.RESET}")
            
        except Exception as e:
            print(f"\n{Colors.RED}Error during extraction: {e}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")

def run_full_pipeline():
    """Run URL collection followed by nutritional extraction."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}FULL PIPELINE{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 60}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}Steps:{Colors.RESET}")
    print(f"   1) Collect product URLs")
    print(f"   2) Extract nutritional facts")
    
    print(f"\n{Colors.YELLOW}This process can take a long time.{Colors.RESET}")
    
    reply = input(f"\n{Colors.MAGENTA}Run full pipeline? (y/N): {Colors.RESET}").lower()
    
    if reply in {"y", "yes", "s", "sim"}:
        try:
            start = time.time()
            
            print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}STEP 1 / 2 — URL COLLECTION{Colors.RESET}")
            print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")
            
            import url_collector
            url_collector.main()
            
            print(f"\n{Colors.GREEN}Step 1 complete.{Colors.RESET}")
            time.sleep(2)
            
            print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}STEP 2 / 2 — NUTRITIONAL EXTRACTION{Colors.RESET}")
            print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")
            
            import nutritional_scraper
            nutritional_scraper.main()
            
            elapsed = time.time() - start
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}PIPELINE COMPLETE{Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
            print(f"\n{Colors.CYAN}Total time:{Colors.RESET} {Colors.YELLOW}{elapsed / 60:.1f} minutes{Colors.RESET}")
            print(f"{Colors.CYAN}Outputs:{Colors.RESET}")
            print(f"   {Colors.GREEN}json/produtos_urls.json{Colors.RESET}")
            print(f"   {Colors.GREEN}dados_extraidos/produtos_nutricionais.csv{Colors.RESET}")
            
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")

def list_generated_files():
    """List generated JSON and CSV artifacts."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}GENERATED FILES{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 60}{Colors.RESET}")
    
    count = 0
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}JSON:{Colors.RESET}")
    folder_json = "json"
    
    if os.path.exists(folder_json):
        json_files = glob.glob(f"{folder_json}/*.json")
        
        if json_files:
            for i, path in enumerate(sorted(json_files, reverse=True), 1):
                base = os.path.basename(path)
                size = os.path.getsize(path)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                
                if size < 1024:
                    size_s = f"{size} B"
                elif size < 1024 * 1024:
                    size_s = f"{size / 1024:.1f} KB"
                else:
                    size_s = f"{size / (1024 * 1024):.1f} MB"
                
                print(f"\n{Colors.YELLOW}{i:2d}.{Colors.RESET} {Colors.WHITE}{base}{Colors.RESET}")
                print(f"     {mtime.strftime('%Y-%m-%d %H:%M:%S')}  ({size_s})")
                count += 1
        else:
            print(f"   {Colors.YELLOW}No JSON files found.{Colors.RESET}")
    else:
        print(f"   {Colors.YELLOW}Folder json/ not found.{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}CSV:{Colors.RESET}")
    folder_csv = "dados_extraidos"
    
    if os.path.exists(folder_csv):
        csv_files = glob.glob(f"{folder_csv}/*.csv")
        
        if csv_files:
            for i, path in enumerate(sorted(csv_files, reverse=True), 1):
                base = os.path.basename(path)
                size = os.path.getsize(path)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                
                if size < 1024:
                    size_s = f"{size} B"
                elif size < 1024 * 1024:
                    size_s = f"{size / 1024:.1f} KB"
                else:
                    size_s = f"{size / (1024 * 1024):.1f} MB"
                
                print(f"\n{Colors.YELLOW}{i:2d}.{Colors.RESET} {Colors.WHITE}{base}{Colors.RESET}")
                print(f"     {mtime.strftime('%Y-%m-%d %H:%M:%S')}  ({size_s})")
                count += 1
        else:
            print(f"   {Colors.YELLOW}No CSV files found.{Colors.RESET}")
    else:
        print(f"   {Colors.YELLOW}Folder dados_extraidos/ not found.{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}{'-' * 60}{Colors.RESET}")
    print(f"{Colors.GREEN}Total entries: {count}{Colors.RESET}")

def wipe_generated_files():
    """Delete generated JSON and CSV files."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}DELETE GENERATED FILES{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 60}{Colors.RESET}")
    
    json_paths = glob.glob("json/*.json") if os.path.exists("json") else []
    csv_paths = glob.glob("dados_extraidos/*.csv") if os.path.exists("dados_extraidos") else []
    total = len(json_paths) + len(csv_paths)
    
    if total == 0:
        print(f"\n{Colors.GREEN}Nothing to delete.{Colors.RESET}")
        return
    
    print(f"\n{Colors.YELLOW}Warning:{Colors.RESET}")
    print(f"   {Colors.RED}{total} file(s){Colors.RESET} will be permanently removed:")
    print(f"     • {len(json_paths)} JSON")
    print(f"     • {len(csv_paths)} CSV")
    print(f"   This action {Colors.RED}cannot be undone.{Colors.RESET}")
    
    confirm = input(f"\n{Colors.MAGENTA}Type CONFIRM to proceed: {Colors.RESET}")
    
    if confirm == "CONFIRM":
        try:
            removed = 0
            for p in json_paths + csv_paths:
                os.remove(p)
                removed += 1
                print(f"{Colors.YELLOW}Removed: {os.path.basename(p)}{Colors.RESET}")
            
            print(f"\n{Colors.GREEN}{removed} file(s) deleted.{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Error while deleting: {e}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")

def print_about():
    """Show project information."""
    about = f"""
{Colors.CYAN}{Colors.BOLD}ABOUT — ADAPTOGEN SCRAPER{Colors.RESET}
{Colors.BLUE}{'-' * 60}{Colors.RESET}

{Colors.GREEN}Purpose:{Colors.RESET}
   Collect and export nutritional facts from Adaptogen products
   (adaptogen.com.br) for spreadsheet-style analysis.

{Colors.GREEN}Features:{Colors.RESET}
   • Four storefront categories scraped for product links
   • Automatic pagination on the Protein category listing
   • Structured parsing of the nutrition table block (`div.flow` → `table`)
   • Outputs JSON URL index + flattened CSV metric rows
   • Missing numeric cells normalized to zero
   • Per-row collection timestamp (`data_coleta`)

{Colors.GREEN}Stack:{Colors.RESET}
   • Python (see local interpreter version)
   • requests — HTTP
   • BeautifulSoup — HTML parsing
   • lxml — fast backend for BeautifulSoup

{Colors.GREEN}Outputs:{Colors.RESET}
   • json/produtos_urls.json — category buckets of absolute URLs
   • dados_extraidos/produtos_nutricionais.csv — macros + metadata columns

{Colors.GREEN}Behavior:{Colors.RESET}
   • Browser-like request headers (User-Agent, Accept-*)
   • 2-second delay between requests (`REQUEST_DELAY`)

{Colors.GREEN}Author:{Colors.RESET}
   Sidnei Almeida — https://github.com/sidnei-almeida
   Version 1.0 — {datetime.now().strftime('%B %Y')}

{Colors.BLUE}{'-' * 60}{Colors.RESET}
"""
    print(about)

def wait_for_continue():
    """Pause until Enter is pressed."""
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

# ============================================================================
# Entry point
# ============================================================================
def main():
    """Run the interactive menu loop."""
    try:
        while True:
            clear_screen()
            print_banner()
            print_main_menu()
            
            choice = prompt_choice()
            
            if choice == "1":
                collect_urls()
                wait_for_continue()
                
            elif choice == "2":
                extract_nutrition()
                wait_for_continue()
                
            elif choice == "3":
                run_full_pipeline()
                wait_for_continue()
                
            elif choice == "4":
                list_generated_files()
                wait_for_continue()
                
            elif choice == "5":
                wipe_generated_files()
                wait_for_continue()
                
            elif choice == "6":
                print_about()
                wait_for_continue()
                
            elif choice == "7":
                print(f"\n{Colors.GREEN}Thanks for using Adaptogen Scraper.{Colors.RESET}")
                print(f"{Colors.CYAN}Goodbye.{Colors.RESET}\n")
                break
                
            else:
                print(f"\n{Colors.RED}Invalid option — choose 1-7.{Colors.RESET}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopped by user. Goodbye.{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
