# -*- coding: utf-8 -*-
"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Přemysl Harazin
email: harazinpremysl@gmail.com
"""

from requests import get
from bs4 import BeautifulSoup as bs
import csv
import sys

def vyber_atributy_z_radku(
    td_tag : "bs4.element.ResultSet", 
    a : str, 
    b : int, 
    c : str, 
    d : int, 
    e : str, 
    f : int,
) -> dict:
    
    """
    Funkce ktera vytvori a vraci slovnik hledanych dat.
    """
    
    return {a:td_tag[b].getText(), c:td_tag[d].getText(), e:td_tag[f].getText()}

def naformatuj_odkaz(
    cislo : str, 
    kraj : str, 
    numnuts : str,
) -> str:
    """
    Funkce formatujici odkaz kazde stranky, ktera ma byt scrapovana.
    Neplati pro Zahranici, jelikoz to je jinak strukturovano.
    """
    return (f"""https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}"""
            f"""&xobec={cislo}&xnumnuts={numnuts}""")

def scraper(
    url : str,
):
    """
    Funkce zajistujici scrapovani dat. Vyuziva knihoven requests a bs4.
    
    :param - str
    """
    odp_serveru = get(url)
    odp_serveru.encoding='UTF-8'
    soup = bs(odp_serveru.text, "html.parser")
    return soup

def zisk_hodnot(
    soup : "bs4.BeautifulSoup", 
    my_tag : str, 
    my_att : str, 
    a : str, 
    b : int, 
    c : str, 
    d : int, 
    e : str, 
    f : int, 
    g : int,
    h : int or NoneType,
    i : int or NoneType,
) -> list:
    
    vysledky = []
    for table in soup.find_all(my_tag, my_att, limit = i):
        vsechny_tr = table.find_all("tr")
        for tr in vsechny_tr[g:h]:
            td_na_radku = tr.find_all("td")
            hodnoty_atributu = vyber_atributy_z_radku(td_na_radku, a, b, c, d, e, f)
            vysledky.append(hodnoty_atributu)
  
    return vysledky  

def obec(
    url : str
) -> list:
    
    """
    Scrapeovaci funkce fungujici na urovni konkretni obce.
    Je rozdelena na dve casti, kdy prvni cast scrapne obecnou tabulku
    uvadejici data o poctu Registrovanych, Obalek, a platnych hlasu a 
    druhou cast, ktera scrapne volebni vysledky jednotlivych stran.
    Obe casti jsou v jedne funkci, jelikoz data jsou na stejne strance a 
    tedy je nutne jen jednou scrapovat.
    """
    
    # Scrapnuti url pomoci soup
    soup = scraper(url)

    my_tag = "table"
    my_att = {"id":"ps311_t1"}
    a = "registrovanych"
    b = 3
    c = "obalky"
    d = 4
    e = "platnych"
    f = 7
    # Range 1
    g = 2
    # Range 2
    h = None
    # limit for find_all
    i = None 
    vysledky = zisk_hodnot(soup, my_tag, my_att, a, b, c, d, e, f, g, h, i)
    
    my_tag = "table"
    my_att = {"class":"table"}
    a = "poradi"
    b = 0
    c = "nazev_strany"
    d = 1
    e = "pocet_hlasu"
    f = 2
    # Range 1
    g = 2
    # Range 2
    h = None
    # limit for find_all
    i = None
    vysledky2 = zisk_hodnot(soup, my_tag, my_att, a, b, c, d, e, f, g, h, i)
    
    return vysledky, vysledky2[1:]
    
def main_function(
    url : str,
    kraj : str,
    numnuts : str,
) -> dict:
    
    """
    Zajistuje scrapeovani na urovni uzemniho celku. 
    Scrapne cisla vsech jednotlivych obci z uzemniho celku a nazev
    vsech techto obci.
    Nasledne tyto cisla pouzije pro ziskani a vytvoreni url odkazu
    ktere jsou pouzity pro scrapeovani konkretnich volebnich dat
    jednotlivych obci. Tyto data nasledne zapisuje do slovniku.
    """

    soup=scraper(url)
    my_tag = "table"
    my_att = {"class":"table"}
    a = "Cislo"
    b = 0
    c = "název"
    d = 1
    e = "empty"
    f = 2
    # Range 1
    g = 2
    # Range 2
    h = None
    # limit for find_all
    i = None
    vysledky = zisk_hodnot(soup, my_tag, my_att, a, b, c, d, e, f, g, h, i)
  
    slovnik_konecnych_dat = {} 
    for each in vysledky:
        try:
            y = obec(naformatuj_odkaz(each["Cislo"], kraj, numnuts))
            slovnik_konecnych_dat[each["Cislo"]] = {"Location":each["název"],
                              "Registered":y[0][0]["registrovanych"],
                              "Envelopes":y[0][0]["obalky"],
                              "Valid":y[0][0]["platnych"]}

            for pskr in range(0,len(y[1])):
                slovnik_konecnych_dat[each["Cislo"]][y[1][pskr]["nazev_strany"]] = y[1][pskr]["pocet_hlasu"]

        except IndexError:
            pass
    
    return slovnik_konecnych_dat

def webpage_check_obecne(
    soup : "bs4.BeautifulSoup", 
    a : str, 
    b : str, 
    c : str
) -> list:
    
    """
    Kontrola, zda uzivatel zadal platnou webovou stranku.
    Nejprve scrapne vsechny odkazy ze zadane webove stranky, 
    nasledne vytridi dle vyuzitelnosti a vraci list pouzitelnych webovych
    stranek.
    """
   
    # Vyhledani vsech linku/odkazu
    project_href = [i['href'] for i in soup.find_all('a', href=True)]
    project_href2 = []
    # Cyklus ktery ze vsech linku vybere vsechny dovolene linky.
    for each in project_href:
        if a and b in each or c in each:
            each="https://www.volby.cz/pls/ps2017nss/"+each
            project_href2.append(each)
    # Returnuje list vsech dovolenych linku.
    return project_href2


def exceptional_case_zahranici(
    url : str,
) -> dict:
    
    """
    Specificka funkce definovana pouze pro zahranici, jelikoz toto ma jako
    jedine rozdilny zapis webove stranky.
    Proto jsou rovnez nektere casti zprogramovany rozdilne a je vyuzito
    rozdilnych principu a postupu. Take zde neni tolik dbano na 
    rozdeleni do jednotlivych mensich funkci a spise je zde snaha o komplexni
    pristup.
    """
    
    soup = scraper(url)
    
    w = "xjazyk=CZ&xkraj=2&xobec=999997"
    x = "xokrsek"
    y = "intentionally empty"
    
    project_zahranici = webpage_check_obecne(soup,w,x,y)

    my_tag = "table"
    my_att = {"class":"table"}
    a = "Okrsek"
    b = -1
    c = "název"
    d = -2
    e = "empty"
    f = -1
    # Range 1
    g = 1
    # Range 2
    h = None
    # limit for find_all
    i = None
    vysledky = zisk_hodnot(soup, my_tag, my_att, a, b, c, d, e, f, g, h, i)

    slovnik_konecnych_dat = {} 
    for i in range(0, len(vysledky)):
            each = vysledky[i]

            url = project_zahranici[i]
            soup = scraper(url)
            
            my_tag = "table"
            my_att = {"class":"table"}
            a = "registrovanych"
            b = 0
            c = "obalky"
            d = 3
            e = "platnych"
            f = 4
            # Range 1
            g = 1
            # Range 2
            h = 2
            # limit for find_all
            i = 1
            
            vysledkyy = zisk_hodnot(soup, my_tag, my_att, a, b, c, d, e, f, g, h, i)
            
            my_tag = "table"
            my_att = {"class":"table"}
            a = "poradi"
            b = 0
            c = "nazev_strany"
            d = 1
            e = "pocet_hlasu"
            f = 2
            # Range 1
            g = 2
            # Range 2
            h = None
            # limit for find_all
            i = None            
            vysledky2 = zisk_hodnot(soup, my_tag, my_att, a, b, c, d, e, f, g, h, i)

            # Pozn: try/except - Index Error zde není řešen, jelikož 
            # Zahraničí pro zadaný rok má v tabulkách všechny řádky obsazené.
            y=[vysledkyy,vysledky2]            
            slovnik_konecnych_dat[each["Okrsek"]] = {"Location":each["název"],
                              "Registered":y[0][0]["registrovanych"],
                              "Envelopes":y[0][0]["obalky"],
                              "Valid":y[0][0]["platnych"]}

            for pskr in range(0,len(y[1])):
                slovnik_konecnych_dat[each["Okrsek"]][y[1][pskr]["nazev_strany"]] = y[1][pskr]["pocet_hlasu"]

    return slovnik_konecnych_dat

def csv_zapisovac(
    slovnik_konecnych_dat : dict,
    file_name : str,
):
    
    """
    zapisovani dat do souboru .csv
    pouziva vygenerovany slovnik hodnot a nazev souboru zadany uzivatelem.
    """    
    
    hlavicka_helper = list(slovnik_konecnych_dat.keys())
    hlavicka = list(slovnik_konecnych_dat[hlavicka_helper[0]].keys())
    hlavicka.insert(0, "Code")
    
    with open(file_name, mode="w", encoding="windows-1250", newline="") as csv_soubor:
        zapisovac = csv.writer(csv_soubor, delimiter=";")
        zapisovac.writerow(hlavicka)
    
        for each in slovnik_konecnych_dat.keys():
            zapisovac_helper = list(slovnik_konecnych_dat[each].values())
            zapisovac_helper.insert(0, each)
            zapisovac.writerow(zapisovac_helper)
    
        csv_soubor.close()


def basic_function(url, file_name):

    """
    Zakladni funkce kontrolujici, zda byly zadany spravne parametry
    a ve spravnem poradi.
    Pokud ano, spusti script.
    Pokud ne, ukonci jej.
    """

    # Fixni url obsahujici seznamy na jednotlive uzemni celky
    fixni_url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    soup = scraper(fixni_url)
    # Povolene odkazy na uzemni celky obsahuji vzdy nasledujici stringy
    w = "xnumnuts"
    x = "ps32"
    y = "ps36?"  
    
    # Kontrola, zda uzivatel neprohodil argumenty pri spousteni skriptu
    if url[-4:] == ".csv":
        print("incorrect positioning")
        sys.exit()
    # Kontrola, zda uzivatel zadal spravny odkaz na uzemni celek.
    elif url not in webpage_check_obecne(soup, w, x, y):
        print("incorrect webpage adress")
        sys.exit()
    # Uzemni celek Zahranici ma jako jediny odlisnou webovou strukturu
    # a proto ma sve vlastni reseni.
    elif url == "https://www.volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
        slovnik_konecnych_dat = exceptional_case_zahranici(url)

    # Vsechny ostatni uzemni celky jsou zpracovavany trochu jinym zpusobem, 
    # finalni vygenerovany slovnik ma vsak v obou pripadech stejnou strukturu.
    else:
        numnuts = url[-4:]
        kraj = url.split("xkraj=", 1)[1]
        if kraj[0:2].isdigit():
            kraj = kraj[0:2]
        else:
            kraj = kraj[0:1]
            
        slovnik_konecnych_dat = main_function(url, kraj, numnuts)
    
    csv_zapisovac(slovnik_konecnych_dat, file_name)
    print("end")


if __name__ == "__main__":
    print("beginning")    
    url = str(sys.argv[1])
    file_name = str(sys.argv[2])
    basic_function(url, file_name)