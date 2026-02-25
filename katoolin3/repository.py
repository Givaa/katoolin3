"""APT repository management for Kali Linux sources."""

import os
import subprocess
import sys

from .colors import print_success, print_error, print_info, print_warning

REPO_FILE = "/etc/apt/sources.list.d/katoolin3.list"
REPO_CONTENT = (
    "# Katoolin3 - Kali Linux repositories\n"
    "deb http://http.kali.org/kali kali-rolling main contrib non-free\n"
    "# deb-src http://http.kali.org/kali kali-rolling main contrib non-free\n"
)
GPG_KEY = "ED444FF07D8D0BF6"
KEYSERVER = "keyserver.ubuntu.com"


def check_root():
    """Exit if not running as root."""
    if os.getuid() != 0:
        print_error("This tool requires root privileges. Run with sudo.")
        sys.exit(1)


def is_repo_added():
    """Check if Kali repository file exists."""
    return os.path.exists(REPO_FILE)


def add_repo():
    """Add Kali Linux repository to apt sources."""
    if is_repo_added():
        print_info("Kali repository already added.")
        return True

    try:
        with open(REPO_FILE, "w") as f:
            f.write(REPO_CONTENT)
        print_success("Kali repository added.")
        return True
    except PermissionError:
        print_error("Permission denied. Run as root.")
        return False


def remove_repo():
    """Remove Kali Linux repository from apt sources."""
    if not is_repo_added():
        print_info("No Kali repository to remove.")
        return True

    try:
        os.remove(REPO_FILE)
        print_success("Kali repository removed.")
        return True
    except OSError as e:
        print_error(f"Failed to remove repository: {e}")
        return False


def add_gpg_key():
    """Import the Kali Linux GPG signing key."""
    print_info("Importing Kali GPG key...")
    result = subprocess.run(
        ["apt-key", "adv", "--keyserver", KEYSERVER, "--recv-keys", GPG_KEY],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print_success("GPG key imported.")
        return True
    else:
        print_error(f"Failed to import GPG key: {result.stderr.strip()}")
        return False


def update():
    """Run apt-get update for the Kali repository only."""
    print_info("Updating package lists...")
    result = subprocess.run(
        [
            "apt-get",
            "update",
            "-o", 'Dir::Etc::sourcelist="sources.list.d/katoolin3.list"',
            "-o", 'Dir::Etc::sourceparts="-"',
            "-o", 'APT::Get::List-Cleanup="0"',
        ]
    )
    if result.returncode == 0:
        print_success("Package lists updated.")
    else:
        print_error("Failed to update package lists.")
    return result.returncode == 0


def setup_repo():
    """Full setup: add repo, import key, update. Returns True on success."""
    if not add_repo():
        return False
    if not add_gpg_key():
        return False
    return update()
