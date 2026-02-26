"""Package installation logic for katoolin3."""

import subprocess

from .categories import CATEGORIES, get_tool_name
from .colors import Colors, colored, print_success, print_error, print_info
from .repository import setup_repo, is_repo_added


def is_installed(package_name):
    """Check if a package is installed via dpkg."""
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Status}", package_name],
            capture_output=True,
            text=True,
        )
        return "install ok installed" in result.stdout
    except FileNotFoundError:
        return False


def show_installed(category_id=None):
    """Show installed tools, optionally filtered by category."""
    if category_id is not None:
        if category_id not in CATEGORIES:
            print_error(f"Invalid category: {category_id}")
            return
        cats = {category_id: CATEGORIES[category_id]}
    else:
        cats = CATEGORIES

    total_installed = 0
    total_tools = 0

    for cat_id, cat in sorted(cats.items()):
        installed = []
        not_installed = []
        for tool in cat["tools"]:
            name = get_tool_name(tool)
            if is_installed(name):
                installed.append(name)
            else:
                not_installed.append(name)

        total_installed += len(installed)
        total_tools += len(cat["tools"])

        marker = colored(
            f"[{len(installed)}/{len(cat['tools'])}]", Colors.GREEN
        )
        print(f"\n  {marker} {cat['name']}")
        if installed:
            for name in installed:
                print(f"    {colored('+', Colors.GREEN)} {name}")
        if not_installed and category_id is not None:
            for name in not_installed:
                print(f"    {colored('-', Colors.RED)} {name}")

    print(
        colored(
            f"\n  Total: {total_installed}/{total_tools} tools installed\n",
            Colors.CYAN,
        )
    )


def _ensure_repo():
    """Ensure Kali repo is added before installing."""
    if not is_repo_added():
        print_info("Setting up Kali repository first...")
        if not setup_repo():
            print_error("Failed to set up repository. Cannot install.")
            return False
    return True


def install_package(package_name):
    """Install a package via apt-get."""
    print_info(f"Installing {package_name}...")
    result = subprocess.run(["apt-get", "install", "-y", package_name])
    if result.returncode == 0:
        print_success(f"{package_name} installed successfully.")
    else:
        print_error(f"Failed to install {package_name}.")
    return result.returncode == 0


def install_tool(tool):
    """Install a single tool."""
    if not _ensure_repo():
        return False
    return install_package(tool)


def install_category(category_id):
    """Install all tools in a category."""
    if category_id not in CATEGORIES:
        print_error(f"Invalid category: {category_id}")
        return

    cat = CATEGORIES[category_id]
    tools = cat["tools"]
    print_info(f"Installing all {len(tools)} tools in '{cat['name']}'...")

    success = 0
    failed = 0
    for tool in tools:
        if install_tool(tool):
            success += 1
        else:
            failed += 1

    print()
    print_info(f"Done. {success} succeeded, {failed} failed.")
