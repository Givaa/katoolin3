"""Package installation logic for katoolin3."""

import subprocess

from .categories import CATEGORIES
from .colors import print_success, print_error, print_info
from .repository import setup_repo, is_repo_added


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
