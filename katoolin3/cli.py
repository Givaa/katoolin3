"""Main CLI interface for katoolin3."""

import os
import sys

from .categories import CATEGORIES, get_tool_name, count_all_tools
from .installer import install_tool, install_category
from .repository import (
    check_root,
    is_repo_added,
    setup_repo,
    remove_repo,
)
from .colors import Colors, colored, print_info, print_error, print_warning

VERSION = "3.0"

BANNER = r"""
 {cyan} _  __     _              _ _       ___
 | |/ /__ _| |_ ___   ___ | (_)_ __ |_  )
 | ' // _` | __/ _ \ / _ \| | | '_ \ |_ \
 | . \ (_| | || (_) | (_) | | | | | |__) |
 |_|\_\__,_|\__\___/ \___/|_|_|_| |_|____/{reset}  v{version}

 {green}+ -- -- +=[ Kali Linux Tools Installer
 + -- -- +=[ {tool_count} Tools in {cat_count} Categories{reset}
 {yellow}[W] Remove Kali repos before updating your system.{reset}
"""


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(
        BANNER.format(
            cyan=Colors.CYAN,
            green=Colors.GREEN,
            yellow=Colors.YELLOW,
            reset=Colors.RESET,
            version=VERSION,
            tool_count=count_all_tools(),
            cat_count=len(CATEGORIES),
        )
    )


def show_main_menu():
    print(
        f"""
 1) Manage Kali Repositories
 2) View Categories
 3) Search Tool
 4) Help
 0) Exit
"""
    )


def show_categories():
    print(colored("\n:: Categories:\n", Colors.GREEN))
    for cat_id, cat in sorted(CATEGORIES.items()):
        count = len(cat["tools"])
        print(f"  {cat_id:>2}) {cat['name']:<28} ({count} tools)")
    print()


def show_tools(category_id):
    cat = CATEGORIES[category_id]
    tools = cat["tools"]
    print(colored(f"\n:: {cat['name']}\n", Colors.GREEN))
    for i, tool in enumerate(tools, 1):
        name = get_tool_name(tool)
        if i % 2 == 1:
            print(f"  {i:>3}) {name:<28}", end="")
        else:
            print(f"  {i:>3}) {name}")
    if len(tools) % 2 == 1:
        print()
    print(f"\n    0) Install ALL\n")


def repo_menu():
    """Repository management submenu."""
    while True:
        print(
            f"""
 1) Add Kali repositories & update
 2) Remove Kali repositories
 3) Show repository status
 0) Back
"""
        )
        try:
            choice = input(colored("repo > ", Colors.GREEN)).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if choice == "1":
            setup_repo()
        elif choice == "2":
            remove_repo()
        elif choice == "3":
            status = "added" if is_repo_added() else "not added"
            print_info(f"Kali repository is {status}.")
        elif choice in ("0", "back"):
            break
        else:
            print_error("Invalid option.")


def category_menu(category_id):
    """Tool browsing and installation for a single category."""
    show_tools(category_id)
    cat = CATEGORIES[category_id]
    tools = cat["tools"]

    while True:
        prompt = colored(f"kat ({cat['name']}) > ", Colors.CYAN)
        try:
            choice = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if choice in ("back", "b", ""):
            break
        elif choice == "0":
            install_category(category_id)
        elif choice == "show":
            show_tools(category_id)
        elif choice == "help":
            print(
                "  <number>  Install tool\n"
                "  0         Install all\n"
                "  show      Show tools\n"
                "  back      Return to categories"
            )
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(tools):
                    install_tool(tools[idx - 1])
                else:
                    print_error(f"Number must be 1-{len(tools)}")
            except ValueError:
                print_error("Invalid input.")


def search_menu():
    """Search for a tool across all categories."""
    try:
        query = input(colored("Search tool: ", Colors.CYAN)).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if not query:
        return

    found = False
    for cat_id, cat in sorted(CATEGORIES.items()):
        for tool in cat["tools"]:
            name = get_tool_name(tool)
            if query in name.lower():
                if not found:
                    print(colored(f"\n:: Results for '{query}':\n", Colors.GREEN))
                    found = True
                print(f"  [{cat['name']}] {name}")

    if not found:
        print_error(f"No tool matching '{query}' found.")
    print()


def show_help():
    print(
        """
  Usage: Navigate menus by typing the number of your choice.

  Main menu:
    1          Manage Kali repositories (add/remove)
    2          Browse tool categories
    3          Search for a specific tool
    4          Show this help
    0          Exit

  In category view:
    <number>   Install the tool at that number
    0          Install all tools in the category
    show       Re-display the tool list
    back       Return to previous menu
"""
    )


def main():
    """Main entry point."""
    check_root()
    clear_screen()
    banner()

    while True:
        show_main_menu()
        try:
            choice = input(colored("kat > ", Colors.CYAN)).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            sys.exit(0)

        if choice == "1":
            repo_menu()
        elif choice == "2":
            show_categories()
            try:
                cat_choice = input(
                    colored("Select category (0 to go back): ", Colors.CYAN)
                ).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                continue

            try:
                cat_id = int(cat_choice)
                if cat_id == 0:
                    continue
                if cat_id in CATEGORIES:
                    category_menu(cat_id)
                else:
                    print_error("Invalid category.")
            except ValueError:
                if cat_choice:
                    print_error("Invalid input.")
        elif choice == "3":
            search_menu()
        elif choice == "4":
            show_help()
        elif choice in ("0", "exit", "quit"):
            print("\nBye!")
            sys.exit(0)
        elif choice == "clear":
            clear_screen()
            banner()
        else:
            print_error("Invalid option. Type 4 for help.")
