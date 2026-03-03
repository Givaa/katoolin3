# katoolin3

Installa i tool di [Kali Linux](https://www.kali.org/) su qualsiasi sistema Debian/Ubuntu — senza installare Kali.

Kali Linux include 400+ tool per penetration testing (nmap, aircrack-ng, burpsuite, sqlmap, metasploit, netexec, bloodhound, ecc.), normalmente disponibili solo all'interno di Kali. **katoolin3** aggiunge i repository ufficiali Kali al tuo sistema e offre un menu interattivo per sfogliare, cercare e installare i tool singolarmente o per categoria.

---

## Avvio rapido

```bash
git clone https://github.com/Givaa/katoolin3.git
cd katoolin3
./katoolin3.sh
```

Nient'altro. Non serve installare nulla.

---

## Requisiti

- Python 3.6+
- Linux basato su Debian/Ubuntu (con `apt-get`)
- Privilegi di root (gestiti automaticamente dallo script)

---

## Utilizzo

### Menu interattivo

```bash
./katoolin3.sh
```

```
  1  Gestisci repository Kali (aggiungi/rimuovi)
  2  Sfoglia le categorie di tool
  3  Cerca un tool
  4  Tool installati
  5  Aiuto
  0  Esci
```

Nella vista categoria:
```
  <numero>  Installa il tool corrispondente
  0         Installa tutti i tool della categoria
  show      Mostra di nuovo la lista
  back      Torna al menu precedente
```

### Modalità CLI (non interattiva)

```bash
# Installa i tool essenziali (~50 tool, i migliori per categoria)
./katoolin3.sh --top

# Installa TUTTI i 415 tool
./katoolin3.sh --full

# Installa una categoria specifica (es. 10 = Post Exploitation)
./katoolin3.sh --category 10

# Installa un singolo tool
./katoolin3.sh --install netexec

# Elenca tutte le categorie
./katoolin3.sh --list

# Cerca un tool
./katoolin3.sh --search nmap

# Mostra i tool installati (tutte le categorie o una specifica)
./katoolin3.sh --status
./katoolin3.sh --status 10

# Gestisci i repository manualmente
./katoolin3.sh --add-repo
./katoolin3.sh --remove-repo
```

---

## Categorie di tool

| # | Categoria | Esempi |
|---|-----------|--------|
| 1 | Information Gathering | nmap, amass, recon-ng, masscan, subfinder, sherlock |
| 2 | Vulnerability Analysis | sqlmap, nuclei, nikto, lynis, openvas |
| 3 | Web Application Analysis | burpsuite, ffuf, feroxbuster, gobuster, wpscan |
| 4 | Database Assessment | sqlmap, jsql, dbpwaudit, hexorbase |
| 5 | Password Attacks | john, hashcat, hydra, medusa, crowbar |
| 6 | Wireless Attacks | aircrack-ng, airgeddon, kismet, wifite, hcxtools |
| 7 | Reverse Engineering | ghidra, apktool, edb-debugger, yara |
| 8 | Exploitation Tools | metasploit-framework, beef-xss, evilginx2, set |
| 9 | Sniffing & Spoofing | bettercap, responder, mitmproxy, ettercap, wireshark |
| 10 | Post Exploitation | netexec, bloodhound, evil-winrm, impacket-scripts |
| 11 | Forensics | autopsy, binwalk, volatility, chainsaw, testdisk |
| 12 | Reporting Tools | dradis, eyewitness, cherrytree, faraday-cli |
| 13 | Social Engineering | set, beef-xss, maltego, wifiphisher |
| 14 | Stress Testing | slowhttptest, t50, dhcpig, thc-ssl-dos |
| 15 | Hardware Hacking | android-sdk, arduino, apktool |

---

## Sicurezza e conflitti di pacchetti

katoolin3 applica automaticamente una regola di **apt pinning** quando aggiunge i repository Kali. Questo assegna ai pacchetti Kali una priorità bassa (50), in modo che:

- Non sovrascrivano mai pacchetti di sistema Ubuntu/Debian durante `apt upgrade`
- Vengano installati **solo se esplicitamente richiesti** (es. `apt install nmap`)

### Prima di `apt upgrade`

Nonostante il pinning, è comunque consigliato rimuovere i repository Kali prima di aggiornare il sistema:

```bash
./katoolin3.sh --remove-repo
```

oppure dal menu interattivo: `1` → `2`. Poi riaggiungerli dopo:

```bash
./katoolin3.sh --add-repo
```

### Se si verificano conflitti

In caso di errore dpkg durante l'installazione di un tool:

```bash
sudo dpkg --configure -a
sudo apt-get install -f
```

---

## Credits

- Progetto originale: [katoolin](https://github.com/LionSec/katoolin) by **LionSec**
- Fork e riscrittura in Python 3: **[Givaa](https://github.com/Givaa)**
- Licenza: GPLv2
