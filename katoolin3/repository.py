"""APT repository management for Kali Linux sources."""

import os
import subprocess
import sys

from .colors import print_success, print_error, print_info

REPO_FILE = "/etc/apt/sources.list.d/katoolin3.list"
KEYRING_DIR = "/etc/apt/keyrings"
KEYRING_FILE = "/etc/apt/keyrings/katoolin3.gpg"
REPO_CONTENT = (
    "# Katoolin3 - Kali Linux repositories\n"
    "deb [signed-by=/etc/apt/keyrings/katoolin3.gpg]"
    " http://http.kali.org/kali kali-rolling main contrib non-free\n"
)
KALI_KEY_URL = "https://archive.kali.org/archive-key.asc"
PINNING_FILE = "/etc/apt/preferences.d/katoolin3"
PINNING_CONTENT = (
    "# Katoolin3 - prevent Kali packages from overriding system packages\n"
    "Package: *\n"
    "Pin: release o=Kali\n"
    "Pin-Priority: 50\n"
)


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
        with open(PINNING_FILE, "w") as f:
            f.write(PINNING_CONTENT)
        print_success("Kali repository added (with safe pinning).")
        return True
    except PermissionError:
        print_error("Permission denied. Run as root.")
        return False


def remove_repo():
    """Remove Kali Linux repository and GPG key."""
    removed_any = False

    if is_repo_added():
        try:
            os.remove(REPO_FILE)
            print_success("Kali repository removed.")
            removed_any = True
        except OSError as e:
            print_error(f"Failed to remove repository: {e}")
            return False
    else:
        print_info("No Kali repository to remove.")

    if os.path.exists(KEYRING_FILE):
        try:
            os.remove(KEYRING_FILE)
            print_success("GPG key removed.")
            removed_any = True
        except OSError as e:
            print_error(f"Failed to remove GPG key: {e}")

    if os.path.exists(PINNING_FILE):
        try:
            os.remove(PINNING_FILE)
            print_success("Pinning rules removed.")
            removed_any = True
        except OSError as e:
            print_error(f"Failed to remove pinning file: {e}")

    if not removed_any:
        print_info("Nothing to remove.")

    return True


def add_gpg_key():
    """Import the Kali Linux GPG signing key using modern keyring method."""
    print_info("Importing Kali GPG key...")

    os.makedirs(KEYRING_DIR, exist_ok=True)

    # Download the ASCII-armored key from the official Kali server
    fetch = subprocess.run(
        ["wget", "-qO-", KALI_KEY_URL],
        capture_output=True,
    )
    if fetch.returncode != 0 or not fetch.stdout:
        print_error("Failed to download GPG key from archive.kali.org.")
        return False

    # Convert from ASCII armor to binary .gpg format
    dearmor = subprocess.run(
        ["gpg", "--dearmor"],
        input=fetch.stdout,
        capture_output=True,
    )
    if dearmor.returncode != 0 or not dearmor.stdout:
        print_error("Failed to dearmor GPG key.")
        return False

    try:
        with open(KEYRING_FILE, "wb") as f:
            f.write(dearmor.stdout)
    except OSError as e:
        print_error(f"Failed to write keyring file: {e}")
        return False

    print_success("GPG key imported.")
    return True


def update():
    """Run apt-get update for the Kali repository only."""
    print_info("Updating package lists...")
    result = subprocess.run(
        [
            "apt-get",
            "update",
            "-o", "Dir::Etc::sourcelist=sources.list.d/katoolin3.list",
            "-o", "Dir::Etc::sourceparts=-",
            "-o", "APT::Get::List-Cleanup=0",
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
