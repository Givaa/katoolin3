# katoolin3

A Python 3 CLI tool that lets you install [Kali Linux](https://www.kali.org/) penetration testing tools on any Debian/Ubuntu-based distribution — without having to install Kali itself.

Kali Linux ships with 400+ security and hacking tools (nmap, aircrack-ng, burpsuite, sqlmap, metasploit, netexec, bloodhound, etc.), but they are normally only available inside a Kali installation. **katoolin3** adds the official Kali repositories to your system and provides an interactive menu to browse, search, and install any of those tools individually or by category.

This is a complete Python 3 rewrite of the original [katoolin](https://github.com/LionSec/katoolin) by LionSec.

## What's new in katoolin3

The original katoolin was a single monolithic Python 2 script (1300+ lines) that is no longer maintained and incompatible with modern systems. katoolin3 is a full rewrite that brings:

- **Python 3 support** — Python 2 reached end-of-life in 2020
- **Modular architecture** — clean separation into categories, installer, repository manager, and CLI
- **Safe repository management** — uses a dedicated file in `/etc/apt/sources.list.d/` instead of appending to `sources.list`
- **Data-driven design** — all 415 tools defined as data, not repeated if/elif chains
- **Proper error handling** — uses `subprocess.run()` with return code checks instead of `os.system()`
- **pip installable** — standard `setup.py` with console script entry point
- **Search functionality** — find any tool across all 15 categories
- **Fixed broken install methods** — the original used dead `wget` URLs and outdated `git clone` commands for ~12 tools; all tools now install cleanly via `apt` from the official Kali repository
- **Updated tool list (2025/2026)** — added modern tools like netexec, bloodhound, evil-winrm, nuclei, ffuf, feroxbuster, ghidra, hashcat, bettercap, and many more; reorganized categories to match current Kali (added Database Assessment, Post Exploitation, Social Engineering)

## Features

- Add/remove Kali Linux repositories safely
- Browse 15 categories with 415 penetration testing tools
- Install individual tools or entire categories at once
- Search tools by name across all categories
- Automatic GPG key import and targeted repository updates

### Tool Categories

| # | Category | Tools |
|---|----------|-------|
| 1 | Information Gathering | nmap, amass, recon-ng, theharvester, masscan, subfinder, sherlock, ... |
| 2 | Vulnerability Analysis | sqlmap, nuclei, nikto, lynis, legion, openvas, ... |
| 3 | Web Application Analysis | burpsuite, ffuf, feroxbuster, gobuster, wpscan, caido, dirsearch, ... |
| 4 | Database Assessment | sqlmap, jsql, dbpwaudit, hexorbase, ... |
| 5 | Password Attacks | john, hashcat, hydra, medusa, crowbar, brutespray, ... |
| 6 | Wireless Attacks | aircrack-ng, airgeddon, kismet, wifite, bully, hcxtools, mdk4, ... |
| 7 | Reverse Engineering | ghidra, apktool, edb-debugger, yara, detect-it-easy, ... |
| 8 | Exploitation Tools | metasploit-framework, armitage, beef-xss, evilginx2, set, ... |
| 9 | Sniffing & Spoofing | bettercap, responder, mitmproxy, mitm6, ettercap, wireshark, ... |
| 10 | Post Exploitation | netexec, bloodhound, evil-winrm, impacket-scripts, mimikatz, ... |
| 11 | Forensics | autopsy, binwalk, volatility, chainsaw, foremost, testdisk, ... |
| 12 | Reporting Tools | dradis, eyewitness, cherrytree, maltego, faraday-cli, ... |
| 13 | Social Engineering | set, beef-xss, maltego, wifiphisher, ... |
| 14 | Stress Testing | slowhttptest, t50, dhcpig, thc-ssl-dos, ... |
| 15 | Hardware Hacking | android-sdk, arduino, apktool, ... |

## Requirements

- Python 3.6+
- Debian/Ubuntu-based Linux distribution (with `apt-get`)
- Root privileges

## Installation

### Option 1: pip install

```bash
git clone https://github.com/Givaa/katoolin3.git
cd katoolin3
sudo pip3 install .
sudo katoolin3
```

### Option 2: Run directly

```bash
git clone https://github.com/Givaa/katoolin3.git
cd katoolin3
sudo python3 -m katoolin3
```

## Usage

### CLI Mode (non-interactive)

Quick commands for scripting and fast installs:

```bash
# Install top essential tools (~50 tools, the best from each category)
sudo katoolin3 --top

# Install ALL 415 tools
sudo katoolin3 --full

# Install a specific category (e.g. 10 = Post Exploitation)
sudo katoolin3 --category 10

# Install a single tool
sudo katoolin3 --install netexec

# List all categories
katoolin3 --list

# Search for a tool
katoolin3 --search nmap

# Manage repositories
sudo katoolin3 --add-repo
sudo katoolin3 --remove-repo
```

### Interactive Mode

Run without arguments to get the interactive menu:

```bash
sudo katoolin3
```

```
Main menu:
  1  Manage Kali repositories (add/remove)
  2  Browse tool categories
  3  Search for a specific tool
  4  Help
  0  Exit

In category view:
  <number>  Install the tool at that number
  0         Install all tools in the category
  show      Re-display the tool list
  back      Return to previous menu
```

## Warning

Before updating your system, **remove all Kali Linux repositories** to avoid package conflicts:

```
kat > 1
repo > 2
```

This is important because Kali packages can override your system's default packages during `apt upgrade`.

## Credits

- Original project: [katoolin](https://github.com/LionSec/katoolin) by LionSec
- Python 3 rewrite: [Givaa](https://github.com/Givaa)
- License: GPLv2
