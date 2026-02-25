"""Main CLI interface for katoolin3."""

import argparse
import os
import sys

from .categories import (
    CATEGORIES,
    TOP_TOOLS,
    get_tool_name,
    get_top_tools,
    count_all_tools,
)
from .installer import install_tool, install_category
from .repository import (
    check_root,
    is_repo_added,
    setup_repo,
    remove_repo,
)
from .colors import Colors, colored, print_info, print_error, print_success

VERSION = "3.1"

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


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog="katoolin3",
        description="Install Kali Linux tools on Debian/Ubuntu.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--top",
        action="store_true",
        help="Install top essential tools from every category (~50 tools)",
    )
    group.add_argument(
        "--full",
        action="store_true",
        help="Install ALL tools from every category",
    )
    group.add_argument(
        "--category", "-c",
        type=int,
        metavar="N",
        help="Install all tools from category N",
    )
    group.add_argument(
        "--install", "-i",
        metavar="TOOL",
        help="Install a single tool by name",
    )
    group.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all categories",
    )
    group.add_argument(
        "--search", "-s",
        metavar="QUERY",
        help="Search for a tool by name",
    )
    group.add_argument(
        "--add-repo",
        action="store_true",
        help="Add Kali repositories and import GPG key",
    )
    group.add_argument(
        "--remove-repo",
        action="store_true",
        help="Remove Kali repositories",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# CLI (non-interactive) commands
# ---------------------------------------------------------------------------

def cli_list():
    """Print categories and tool counts."""
    print(colored("\n:: Categories:\n", Colors.GREEN))
    for cat_id, cat in sorted(CATEGORIES.items()):
        count = len(cat["tools"])
        print(f"  {cat_id:>2}) {cat['name']:<28} ({count} tools)")
    print(f"\n  Total: {count_all_tools()} tools")
    top = get_top_tools()
    print(f"  Top tools (--top): {len(top)} tools\n")


def cli_search(query):
    """Search for a tool across all categories."""
    query = query.lower()
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
    else:
        print()


def cli_install_top():
    """Install top essential tools."""
    tools = get_top_tools()
    print_info(f"Installing {len(tools)} top tools across all categories...\n")

    for cat_id, cat in sorted(CATEGORIES.items()):
        cat_tools = TOP_TOOLS.get(cat_id, [])
        if cat_tools:
            print(colored(f"\n:: {cat['name']}", Colors.GREEN))
            for tool in cat_tools:
                install_tool(tool)

    print()
    print_success(f"Top tools installation complete.")


def cli_install_full():
    """Install all tools from every category."""
    print_info(f"Installing ALL {count_all_tools()} tools...\n")
    for cat_id in sorted(CATEGORIES.keys()):
        install_category(cat_id)
    print()
    print_success("Full installation complete.")


def cli_install_category(cat_id):
    """Install all tools from a specific category."""
    if cat_id not in CATEGORIES:
        print_error(f"Invalid category {cat_id}. Use --list to see available categories.")
        sys.exit(1)
    install_category(cat_id)


# ---------------------------------------------------------------------------
# Interactive menu (unchanged)
# ---------------------------------------------------------------------------

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

  CLI mode (non-interactive):
    katoolin3 --top              Install top essential tools
    katoolin3 --full             Install all tools
    katoolin3 --category N       Install category N
    katoolin3 --install TOOL     Install a single tool
    katoolin3 --list             List categories
    katoolin3 --search QUERY     Search for a tool
    katoolin3 --add-repo         Add Kali repositories
    katoolin3 --remove-repo      Remove Kali repositories
"""
    )


def interactive_menu():
    """Run the interactive menu."""
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


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    """Main entry point — CLI mode if args given, interactive otherwise."""
    args = parse_args()

    # Non-interactive commands that don't need root
    if args.list:
        cli_list()
        return
    if args.search:
        cli_search(args.search)
        return

    # Everything else needs root
    check_root()

    if args.add_repo:
        setup_repo()
    elif args.remove_repo:
        remove_repo()
    elif args.top:
        cli_install_top()
    elif args.full:
        cli_install_full()
    elif args.category is not None:
        cli_install_category(args.category)
    elif args.install:
        install_tool(args.install)
    else:
        # No CLI flags → interactive menu
        interactive_menu()
