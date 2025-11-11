# AGV Email Agent / Agent pro psaní mailů o AGV

[English](#english) | [Čeština](#čeština)

---

## English

### Overview

This is an email agent for analyzing AGV (Automated Guided Vehicle) data and automatically generating email reports. The agent can:

- Load and analyze AGV event data from JSON files
- Generate detailed HTML email reports
- Support both Czech and English languages
- Preview emails before sending (dry-run mode)
- Send reports to single or multiple recipients

### Features

- **Data Analysis**: Automatically analyzes AGV events, counts issues, identifies active problems
- **Smart Reporting**: Generates professional HTML email reports with statistics and tables
- **Bilingual Support**: Reports can be generated in English or Czech
- **Safe Testing**: Dry-run mode allows you to preview emails without sending them
- **Flexible Configuration**: Supports custom SMTP settings via configuration file

### Installation

1. Clone this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

#### Basic Usage (Dry Run - No Actual Email Sent)

```bash
python email_agent.py cerven.json admin@example.com cs
```

Arguments:
- `cerven.json` - JSON file with AGV data
- `admin@example.com` - recipient email address
- `cs` - language (cs = Czech, en = English)

#### Using in Your Python Code

```python
from email_agent import EmailAgent

# Create agent
agent = EmailAgent()

# Generate and send report
agent.generate_and_send_report(
    json_file='cerven.json',
    recipient='manager@example.com',
    language='cs',
    dry_run=True  # Set to False to actually send
)
```

### Configuration

1. Copy `config_example.json` to `config.json`
2. Edit with your SMTP settings:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "use_tls": true
}
```

**Note**: For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

3. Use the configuration:

```python
import json
from email_agent import EmailAgent

with open('config.json', 'r') as f:
    config = json.load(f)

agent = EmailAgent(config)
```

### Examples

See `example_usage.py` for detailed examples:

```bash
python example_usage.py
```

Examples include:
- Basic usage
- Custom configuration
- Custom analysis
- Multiple recipients

### Data Format

The agent expects JSON data with AGV events in the following format:

```json
[
  {
    "TimeStamp": "2025-06-16 10:53:53Z",
    "Title": "Protectionfield rear triggered",
    "ComponentID": "vehicle_1",
    "Cleared": false,
    "UUID": "d112d445-1501-439a-9712-477e005dfaf3",
    "Position": 792,
    "ComponentName": "AGV1"
  }
]
```

### Email Report Contents

The generated email reports include:

- **Summary Statistics**: Total events, cleared events, active issues
- **Date Range**: Period covered by the report
- **Top Issues**: 10 most common problems
- **Components**: List of all AGV components involved
- **Active Issues**: Detailed list of unresolved problems

---

## Čeština

### Přehled

Toto je agent pro analýzu dat AGV (Automated Guided Vehicle) a automatické generování emailových zpráv. Agent umí:

- Načítat a analyzovat data o událostech AGV z JSON souborů
- Generovat podrobné HTML emailové zprávy
- Podporovat češtinu i angličtinu
- Zobrazit náhled emailu před odesláním (dry-run režim)
- Odesílat zprávy jednomu nebo více příjemcům

### Funkce

- **Analýza dat**: Automaticky analyzuje události AGV, počítá problémy, identifikuje aktivní potíže
- **Chytré reportování**: Generuje profesionální HTML emailové zprávy se statistikami a tabulkami
- **Dvojjazyčná podpora**: Zprávy lze generovat v angličtině nebo češtině
- **Bezpečné testování**: Režim dry-run umožňuje náhled emailů bez jejich odeslání
- **Flexibilní konfigurace**: Podporuje vlastní nastavení SMTP přes konfigurační soubor

### Instalace

1. Naklonujte tento repozitář
2. Nainstalujte potřebné závislosti:
```bash
pip install -r requirements.txt
```

### Rychlý start

#### Základní použití (Dry Run - email se skutečně neodešle)

```bash
python email_agent.py cerven.json admin@example.com cs
```

Argumenty:
- `cerven.json` - JSON soubor s daty AGV
- `admin@example.com` - emailová adresa příjemce
- `cs` - jazyk (cs = čeština, en = angličtina)

#### Použití ve vašem Python kódu

```python
from email_agent import EmailAgent

# Vytvoření agenta
agent = EmailAgent()

# Generování a odeslání zprávy
agent.generate_and_send_report(
    json_file='cerven.json',
    recipient='manager@example.com',
    language='cs',
    dry_run=True  # Nastavte na False pro skutečné odeslání
)
```

### Konfigurace

1. Zkopírujte `config_example.json` na `config.json`
2. Upravte s vašimi SMTP nastaveními:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "vas-email@gmail.com",
  "sender_password": "vase-heslo-aplikace",
  "use_tls": true
}
```

**Poznámka**: Pro Gmail musíte použít [Heslo aplikace](https://support.google.com/accounts/answer/185833), ne vaše běžné heslo.

3. Použití konfigurace:

```python
import json
from email_agent import EmailAgent

with open('config.json', 'r') as f:
    config = json.load(f)

agent = EmailAgent(config)
```

### Příklady

Podívejte se na `example_usage.py` pro podrobné příklady:

```bash
python example_usage.py
```

Příklady zahrnují:
- Základní použití
- Vlastní konfigurace
- Vlastní analýza
- Více příjemců

### Formát dat

Agent očekává JSON data s událostmi AGV v následujícím formátu:

```json
[
  {
    "TimeStamp": "2025-06-16 10:53:53Z",
    "Title": "Protectionfield rear triggered",
    "ComponentID": "vehicle_1",
    "Cleared": false,
    "UUID": "d112d445-1501-439a-9712-477e005dfaf3",
    "Position": 792,
    "ComponentName": "AGV1"
  }
]
```

### Obsah emailové zprávy

Generované emailové zprávy obsahují:

- **Souhrnné statistiky**: Celkový počet událostí, vyřešené události, aktivní problémy
- **Časové období**: Období pokryté zprávou
- **Hlavní problémy**: 10 nejčastějších problémů
- **Komponenty**: Seznam všech zapojených komponent AGV
- **Aktivní problémy**: Podrobný seznam nevyřešených problémů

### Jak na to - Krok za krokem

Chcete-li sestavit agenta na psaní mailů:

1. **Nainstalujte závislosti**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Vyzkoušejte příklady** (bez skutečného odesílání):
   ```bash
   python example_usage.py
   ```

3. **Nastavte SMTP** v `config.json` (zkopírujte z `config_example.json`)

4. **Spusťte agenta**:
   ```bash
   # Pro náhled:
   python email_agent.py cerven.json vas-email@example.com cs
   
   # Pro skutečné odeslání upravte kód a nastavte dry_run=False
   ```

5. **Přizpůsobte podle potřeby** - upravte `email_agent.py` pro vaše specifické požadavky

## License

MIT License
