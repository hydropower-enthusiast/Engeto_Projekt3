# Engeto_Projekt3
Cílem projektu 3 je scrapovací skript, který je zaměřen na volby do poslanecké sněmovny z roku 2017 v ČR.
Scrapování má fungovat pro kterýkoliv uzemní celek z tohoto odkazu:
> https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Výsledné data mají být zapsány ve formátu .csv

## Spouštění Skriptu

### Krok 1 - Příprava pro spuštění skriptu
Nejpvre je nutné vytvořit si virtuální prostředí, aby nedošlo při instalaci potřebných knihoven k přepsání globálních knihoven
Poté je třeba aktivovat Windows PowerShell.
Následně je nutné si do vytvořeného prostředí stáhnout soubor requirements.txt a main.py
Poté přes Aktivovaný PowerShell nainstalovat knihovny pomocí:

> python -m pip install -r requirements.txt

Pozn. Pokud je soubor requirements.txt uložen jinde, je potřeba zadat celou cestu k souboru.
Po nainstalování knihoven je již skript připraven ke spuštení.

### Krok 2 - Spouštění skriptu
Spuštění skriptu je prováděno v PowerShellu pomocí příkazu

> python nazev_prostredi\main.py "webova_stranka" "nazev_csv.csv"

Je nutné při spouštění dbát na pravidla PowerShellu:
& - je v PowerShellu vyhrazený znak, proto je třeba jej obalit uvozovkami

Příklad:
![spusteni konecneho skriptu2](https://github.com/user-attachments/assets/fed8b0d7-16f8-4ce7-855d-12aa8fdb116e)

Dále je nutné zadat webovou stránku a název ve správném pořadí. Webová stránka musí odkazovat na jeden z vybraných územních celků.

## Skript

Skládá se z následujících funkcí:
### vyber_atributy_z_radku
### scraper
### zisk_hodnot
### list_of_webpages
### main_function
### csv_zapisovac
### basic_function

















