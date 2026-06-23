# Rychlý průvodce - Jak na to (Quick Guide)

## Co je to agent na psaní mailů?

Agent na psaní mailů je Python program, který:
1. Načte data o událostech AGV (Automated Guided Vehicle)
2. Analyzuje problémy a statistiky
3. Vytvoří profesionální HTML emailovou zprávu
4. Odešle zprávu na zadané emailové adresy

## Jak začít - 3 jednoduché kroky

### 1. Vyzkoušejte ukázku (bez odesílání emailu)

```bash
python3 demo.py
```

Tento příkaz ukáže kompletní demonstraci všech funkcí.

### 2. Vyzkoušejte různé příklady

```bash
python3 example_usage.py
```

Uvidíte 4 různé příklady použití agenta.

### 3. Spusťte vlastní analýzu

```bash
python3 email_agent.py cerven.json vas-email@example.com cs
```

- `cerven.json` = váš soubor s daty AGV
- `vas-email@example.com` = email příjemce
- `cs` = jazyk zprávy (cs = čeština, en = angličtina)

## Jak odeslat skutečné emaily

### Krok 1: Zkopírujte konfigurační soubor

```bash
cp config_example.json config.json
```

### Krok 2: Upravte config.json se svými SMTP údaji

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "vas-email@gmail.com",
  "sender_password": "vase-heslo-aplikace",
  "use_tls": true
}
```

**Důležité pro Gmail:** Musíte použít [Heslo aplikace](https://support.google.com/accounts/answer/185833), ne vaše běžné heslo.

### Krok 3: Upravte kód pro odesílání

V souboru `email_agent.py` nebo ve vašem vlastním skriptu změňte:

```python
dry_run=True   # Pouze náhled
```

na:

```python
dry_run=False  # Skutečné odesílání
```

## Příklad použití ve vašem kódu

```python
from email_agent import EmailAgent
import json

# Načíst konfiguraci
with open('config.json', 'r') as f:
    config = json.load(f)

# Vytvořit agenta
agent = EmailAgent(config)

# Vygenerovat a odeslat zprávu
agent.generate_and_send_report(
    json_file='cerven.json',
    recipient='manager@firma.cz',
    language='cs',
    dry_run=False  # Změňte na False pro skutečné odeslání
)
```

## Co obsahuje emailová zpráva?

Automaticky vygenerovaná zpráva obsahuje:

📊 **Souhrnné statistiky**
- Celkový počet událostí
- Vyřešené události
- Aktivní problémy

📅 **Časové období**
- Začátek a konec sledovaného období

🔝 **Top 10 nejčastějších problémů**
- Seřazené podle počtu výskytů

⚙️ **Zapojené komponenty**
- Seznam všech AGV komponent

⚠️ **Aktivní problémy**
- Detailní seznam nevyřešených problémů

## Další možnosti

### Odeslat více příjemcům

```python
recipients = [
    'manager@firma.cz',
    'technik@firma.cz',
    'supervisor@firma.cz'
]

for recipient in recipients:
    agent.generate_and_send_report(
        json_file='cerven.json',
        recipient=recipient,
        language='cs',
        dry_run=False
    )
```

### Vlastní analýza

```python
# Načíst data
data = agent.load_agv_data('cerven.json')

# Analyzovat
analysis = agent.analyze_data(data)

# Zobrazit statistiky
print(f"Celkem událostí: {analysis['total_events']}")
print(f"Aktivní problémy: {analysis['not_cleared_events']}")

# Vygenerovat zprávu
body = agent.generate_email_body(analysis, language='cs')
```

## Časté problémy a řešení

### Email se neodešle

1. Zkontrolujte SMTP údaje v `config.json`
2. Pro Gmail použijte "Heslo aplikace", ne běžné heslo
3. Zkontrolujte, zda je povolen "Méně zabezpečený přístup"
4. Zkuste jiný SMTP server

### Chyba při načítání dat

1. Zkontrolujte, zda soubor JSON existuje
2. Ověřte formát JSON souboru
3. Zkontrolujte cestu k souboru

### Email vypadá špatně

1. Některé emailové klienty nepodporují HTML
2. Zkuste otevřít v jiném emailovém klientu
3. Použijte `generate_samples.py` pro vytvoření HTML náhledu

## Potřebujete pomoc?

1. Přečtěte si kompletní dokumentaci v `README.md`
2. Podívejte se na příklady v `example_usage.py`
3. Spusťte `demo.py` pro kompletní ukázku
4. Kontaktujte správce repozitáře

## Automatizace

Pro pravidelné odesílání zpráv můžete použít:

### Linux/Mac (cron)

```bash
# Upravit crontab
crontab -e

# Přidat řádek pro denní zprávu v 8:00
0 8 * * * cd /cesta/k/amr && python3 email_agent.py cerven.json admin@firma.cz cs
```

### Windows (Task Scheduler)

Vytvořte novou úlohu v Plánovači úloh, která spustí váš Python skript.

---

**Gratulujeme!** Nyní máte funkčního agenta na psaní mailů pro analýzu AGV dat! 🎉
