"""ANSI color constants and helpers for terminal output."""


class Colors:
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[33m"
    CYAN = "\033[1;36m"
    RESET = "\033[0m"


def colored(text, color):
    """Wrap text in ANSI color codes."""
    return f"{color}{text}{Colors.RESET}"


def print_error(msg):
    print(colored(f"[!] {msg}", Colors.RED))


def print_success(msg):
    print(colored(f"[+] {msg}", Colors.GREEN))


def print_warning(msg):
    print(colored(f"[W] {msg}", Colors.YELLOW))


def print_info(msg):
    print(colored(f"[*] {msg}", Colors.CYAN))
