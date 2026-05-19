#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universal CLI shell template — colored terminal menus for Python tooling.

USAGE:
  1. Copy into a new repo.
  2. Rename placeholders (`PROJECT_NAME`, `FUNC_*`, folders, etc.).
  3. Wire real logic under each stub handler.
"""

import os
import sys
import time
import glob
from datetime import datetime

# ----------------------------------------------------------------------------
# ANSI colors
# ----------------------------------------------------------------------------
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                       PROJECT_NAME v1.0                      ║
║                   ONE_LINE_SUMMARY_HERE                      ║
║                                                              ║
║  Capability bullet 1                                         ║
║  Capability bullet 2                                         ║
║  Capability bullet 3                                         ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)


def print_progress_bar(message: str, duration_sec: float = 2.0):
    print(f"\n{Colors.YELLOW}Working — {message}...{Colors.RESET}")
    bar_len = 40
    for i in range(bar_len + 1):
        pct = int((i / bar_len) * 100)
        bar = "█" * i + "░" * (bar_len - i)
        print(f"\r{Colors.GREEN}[{bar}] {pct}%{Colors.RESET}", end="", flush=True)
        time.sleep(duration_sec / bar_len)
    print()


def print_main_menu():
    menu = f"""
{Colors.BLUE}{Colors.BOLD}════════════════ MAIN MENU ════════════════{Colors.RESET}

{Colors.GREEN}Primary actions:{Colors.RESET}
  {Colors.YELLOW}1.{Colors.RESET} FUNC_1 — describe action
  {Colors.YELLOW}2.{Colors.RESET} FUNC_2 — describe action
  {Colors.YELLOW}3.{Colors.RESET} FUNC_3 — describe action

{Colors.GREEN}Data:{Colors.RESET}
  {Colors.YELLOW}4.{Colors.RESET} List artifacts
  {Colors.YELLOW}5.{Colors.RESET} Delete artifact directory

{Colors.GREEN}Info:{Colors.RESET}
  {Colors.YELLOW}6.{Colors.RESET} About
  {Colors.YELLOW}7.{Colors.RESET} Quit

{Colors.BLUE}═══════════════════════════════════════════════════════{Colors.RESET}
"""
    print(menu)


def prompt_choice() -> str:
    try:
        return input(f"{Colors.MAGENTA}Pick an option (1-7): {Colors.RESET}").strip()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted.{Colors.RESET}")
        sys.exit(0)


# ----------------------------------------------------------------------------
# Customize these handlers per project.
# ----------------------------------------------------------------------------
def route_action_one():
    print(f"\n{Colors.CYAN}{Colors.BOLD}ACTION ONE{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 62}{Colors.RESET}")
    print(f"\n{Colors.GREEN}Settings:{Colors.RESET}")
    print(f"   Param A: {Colors.YELLOW}<value>{Colors.RESET}")
    print(f"   Param B: {Colors.YELLOW}<value>{Colors.RESET}")

    if input(f"\n{Colors.MAGENTA}Continue? (y/N): {Colors.RESET}").lower() in {
        "y",
        "yes",
    }:
        try:
            print_progress_bar("Running action #1", 2.0)
            print(f"{Colors.GREEN}✓ stub finished{Colors.RESET}")
        except Exception as exc:
            print(f"{Colors.RED}Error: {exc}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")


def route_action_two():
    print(f"\n{Colors.CYAN}{Colors.BOLD}ACTION TWO{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 62}{Colors.RESET}")
    print(f"\n{Colors.YELLOW} Heads-up: customize duration / warnings here.{Colors.RESET}")

    if input(f"\n{Colors.MAGENTA}Continue? (y/N): {Colors.RESET}").lower() in {
        "y",
        "yes",
    }:
        try:
            print_progress_bar("Executing action #2", 1.5)
            print(f"{Colors.GREEN}✓ stub finished{Colors.RESET}")
        except Exception as exc:
            print(f"{Colors.RED}Error: {exc}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")


def route_action_three():
    print(f"\n{Colors.CYAN}{Colors.BOLD}ACTION THREE{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 62}{Colors.RESET}")
    param = input(f"\n{Colors.MAGENTA}Provide free-form input: {Colors.RESET}").strip()

    if not param:
        print(f"{Colors.RED}Input required.{Colors.RESET}")
        return

    try:
        print_progress_bar(f"Processing `{param}`", 1.0)
        print(f"{Colors.GREEN}✓ stub finished{Colors.RESET}")
    except Exception as exc:
        print(f"{Colors.RED}Error: {exc}{Colors.RESET}")


def list_artifacts(directory: str = "OUTPUT_FOLDER", glob_pattern: str = "*.csv"):
    print(f"\n{Colors.CYAN}{Colors.BOLD}ARTIFACTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 62}{Colors.RESET}")

    if not os.path.exists(directory):
        print(f"{Colors.YELLOW}Folder `{directory}` missing.{Colors.RESET}")
        return

    matches = glob.glob(os.path.join(directory, glob_pattern))
    if not matches:
        print(f"{Colors.YELLOW}No `{glob_pattern}` files.{Colors.RESET}")
        return

    print(f"\n{Colors.GREEN}{len(matches)} file(s){Colors.RESET}\n")
    for idx, path in enumerate(sorted(matches, reverse=True), 1):
        size = os.path.getsize(path)
        stamp = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")

        pretty = (
            f"{size} B"
            if size < 1024
            else (
                f"{size / 1024:.1f} KB"
                if size < 1024 ** 2
                else f"{size / (1024 ** 2):.1f} MB"
            )
        )

        print(f"{Colors.YELLOW}{idx:2}.{Colors.RESET} {Colors.WHITE}{os.path.basename(path)}{Colors.RESET}")
        print(f"      {stamp} — {pretty}\n")


def wipe_artifacts(directory: str = "OUTPUT_FOLDER", glob_pattern: str = "*.csv"):
    print(f"\n{Colors.CYAN}{Colors.BOLD}DELETE ARTIFACTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 62}{Colors.RESET}")

    if not os.path.exists(directory):
        print(f"{Colors.YELLOW}`{directory}` not found.{Colors.RESET}")
        return

    files = glob.glob(os.path.join(directory, glob_pattern))
    if not files:
        print(f"{Colors.GREEN}Nothing matched `{glob_pattern}`.{Colors.RESET}")
        return

    print(f"{Colors.RED}{len(files)} file(s){Colors.RESET} will be erased permanently.")
    if input(f"{Colors.MAGENTA}Type CONFIRM to proceed: {Colors.RESET}") == "CONFIRM":
        for path in files:
            os.remove(path)
        print(f"{Colors.GREEN}Deleted {len(files)} file(s).{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Canceled.{Colors.RESET}")


def print_about():
    about = f"""
{Colors.CYAN}{Colors.BOLD}ABOUT{Colors.RESET}
{Colors.BLUE}{'-' * 62}{Colors.RESET}

Replace this prose with concise project specifics:
  • Audience / guarantees
  • Stack & dependencies
  • Output schemas / formats
  • Operational caveats / rate limiting

 Maintainer + version placeholders.

{Colors.BLUE}{'-' * 62}{Colors.RESET}
"""
    print(about)


def wait_for_continue():
    input(f"\n{Colors.CYAN}Press Enter...{Colors.RESET}")


# ----------------------------------------------------------------------------
def main():
    """Dispatch loop."""
    try:
        while True:
            clear_screen()
            print_banner()
            print_main_menu()

            choice = prompt_choice()

            if choice == "1":
                route_action_one()
            elif choice == "2":
                route_action_two()
            elif choice == "3":
                route_action_three()
            elif choice == "4":
                list_artifacts()
            elif choice == "5":
                wipe_artifacts()
            elif choice == "6":
                print_about()
            elif choice == "7":
                print(f"\n{Colors.GREEN}Goodbye.{Colors.RESET}\n")
                break
            else:
                print(f"{Colors.RED}Invalid choice (1-7).{Colors.RESET}")
                time.sleep(2)
                wait_for_continue()
                continue

            wait_for_continue()

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Stopped.{Colors.RESET}\n")


if __name__ == "__main__":
    main()
