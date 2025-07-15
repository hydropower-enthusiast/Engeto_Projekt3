# Engeto_Projekt3
Cílem projektu 3 je scrapovací skript, který je zaměřen na volby do poslanecké sněmovny z roku 2017 v ČR.
Scrapování má fungovat pro kterýkoliv uzemní celek z tohoto odkazu:

> https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Výsledné data mají být zapsány ve formátu .csv

Ukázka výsledku:

<img width="1639" height="472" alt="obrazek" src="https://github.com/user-attachments/assets/684498ba-41d2-4fd2-a33c-8850e19ffdda" />


## Spouštění Skriptu

### Krok 1 - Příprava pro spuštění skriptu
Nejpvre je nutné vytvořit si virtuální prostředí, aby nedošlo při instalaci potřebných knihoven k přepsání globálních knihoven.

Poté je třeba aktivovat Windows PowerShell.
(Přesný postup pro vytvoření virtuálního prostředí a aktivaci PowerShellu je na následujícím odkazu:)

> https://docs.python.org/3/library/venv.html

Následně je nutné si do vytvořeného prostředí stáhnout soubor requirements.txt a main.py
Poté přes Aktivovaný PowerShell nainstalovat knihovny ze souboru requirements.txt pomocí:

> python -m pip install -r requirements.txt

Pozn. Pokud je soubor requirements.txt uložen jinde, je potřeba zadat celou cestu k souboru.
Po nainstalování knihoven je již skript připraven ke spuštení.

### Krok 2 - Spouštění skriptu
Spuštění skriptu je prováděno v aktivovaném PowerShellu pomocí příkazu

> python nazev_prostredi\main.py "webova_stranka" "nazev_csv.csv"

kde nazev_prostredi, webova_stranka a nazev_csv.csv jsou zavislé dle pojmenování a požadavků uživatele.

Pozn: Je nutné při spouštění dbát na pravidla PowerShellu:
& - je v PowerShellu vyhrazený znak, proto je třeba jej obalit uvozovkami

Příklad:

<img width="1453" height="80" alt="obrazek" src="https://github.com/user-attachments/assets/73d13fef-0a05-4858-a48d-e6500945522b" />


Dále je nutné zadat webovou stránku a název ve správném pořadí. Webová stránka musí odkazovat na jeden z vybraných územních celků.


















