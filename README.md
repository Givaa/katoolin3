# katoolin3

A Python 3 CLI tool that lets you install [Kali Linux](https://www.kali.org/) penetration testing tools on any Debian/Ubuntu-based distribution — without having to install Kali itself.

Kali Linux ships with 300+ security and hacking tools (nmap, aircrack-ng, burpsuite, sqlmap, metasploit, etc.), but they are normally only available inside a Kali installation. **katoolin3** adds the official Kali repositories to your system and provides an interactive menu to browse, search, and install any of those tools individually or by category.

This is a complete Python 3 rewrite of the original [katoolin](https://github.com/LionSec/katoolin) by LionSec.

## What's new in katoolin3

The original katoolin was a single monolithic Python 2 script (1300+ lines) that is no longer maintained and incompatible with modern systems. katoolin3 is a full rewrite that brings:

- **Python 3 support** — Python 2 reached end-of-life in 2020
- **Modular architecture** — clean separation into categories, installer, repository manager, and CLI
- **Safe repository management** — uses a dedicated file in `/etc/apt/sources.list.d/` instead of appending to `sources.list`
- **Data-driven design** — all 338 tools defined as data, not repeated if/elif chains
- **Proper error handling** — uses `subprocess.run()` with return code checks instead of `os.system()`
- **pip installable** — standard `setup.py` with console script entry point
- **Search functionality** — find any tool across all 14 categories
- **Fixed broken install methods** — the original used dead `wget` URLs and outdated `git clone` commands for ~12 tools; all 338 tools now install cleanly via `apt` from the official Kali repository

## Features

- Add/remove Kali Linux repositories safely
- Browse 14 categories with 338 penetration testing tools
- Install individual tools or entire categories at once
- Search tools by name across all categories
- Automatic GPG key import and targeted repository updates

### Tool Categories

| # | Category | Tools |
|---|----------|-------|
| 1 | Information Gathering | nmap, wireshark, recon-ng, theharvester, masscan, ... |
| 2 | Vulnerability Analysis | sqlmap, openvas, lynis, yersinia, ... |
| 3 | Wireless Attacks | aircrack-ng, kismet, wifite, reaver, bully, ... |
| 4 | Web Applications | burpsuite, wpscan, zaproxy, dirb, gobuster, w3af, ... |
| 5 | Sniffing & Spoofing | mitmproxy, responder, sslstrip, wireshark, ... |
| 6 | Maintaining Access | weevely, powersploit, nishang, cryptcat, ... |
| 7 | Reporting Tools | dradis, keepnote, magictree, pipal, ... |
| 8 | Exploitation Tools | armitage, beef-xss, metasploit (via armitage), set, ... |
| 9 | Forensics Tools | binwalk, volatility, foremost, cuckoo, ... |
| 10 | Stress Testing | slowhttptest, t50, dhcpig, thc-ssl-dos, ... |
| 11 | Password Attacks | john, hydra, hashcat, crunch, ncrack, ... |
| 12 | Reverse Engineering | apktool, edb-debugger, yara, valgrind, ... |
| 13 | Hardware Hacking | android-sdk, arduino, sakis3g, ... |
| 14 | Extra | Kali metapackages, squid3 |

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
