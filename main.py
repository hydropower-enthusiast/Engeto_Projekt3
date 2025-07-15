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

def scraper(
    url : str,
):
    """
    Funkce zajistujici scrapovani dat. Vyuziva knihoven requests a bs4.
    
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
            hodnoty_atributu = vyber_atributy_z_radku(td_na_radku, a, 
                                                      b, c, d, e, f)
            vysledky.append(hodnoty_atributu)
  
    return vysledky  

def list_of_webpages(
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
   
    # Vyhledani vsech linku/odkazu na dane strance
    link_list = [i['href'] for i in soup.find_all('a', href=True)]
    list_dovolenych_stranek = []
    # Cyklus ktery ze vsech linku vybere vsechny dovolene linky.
    for each in link_list:
        if a and b in each or c in each:
            each="https://www.volby.cz/pls/ps2017nss/"+each
            list_dovolenych_stranek.append(each)
    # Returnuje list vsech dovolenych linku.
    return list_dovolenych_stranek

def main_function(
    url : str,
    zahranici : bool,
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
    y = "xvyber"
    
    seznam_url = list_of_webpages(soup,w,x,y)

    my_tag = "table"
    my_att = {"class":"table"}
    
    if zahranici: 
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

    else:
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
    
    okrsek_obec = a
    vysledky_uz_celek = zisk_hodnot(soup, my_tag, my_att, 
                                    a, b, c, d, e, f, g, h, i)

    slovnik_konecnych_dat = {} 
    for i in range(0, len(vysledky_uz_celek)):
            each = vysledky_uz_celek[i]

            url = seznam_url[i]
            soup = scraper(url)
            
            if zahranici:
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

            else:
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
            
            vysledky_region_1 = zisk_hodnot(soup, my_tag, my_att, 
                                    a, b, c, d, e, f, g, h, i)
            
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
            vysledky_region_2 = zisk_hodnot(soup, my_tag, my_att, 
                                    a, b, c, d, e, f, g, h, i)
            if not zahranici:
                vysledky_region_2 = vysledky_region_2[1:]

            # Pozn: try/except - Index Error je řešen, jelikož 
            # ne všechny územní celky mají v tabulkách na webové stránce
            # všechny řádky obsazené. 
            try:
                y=[vysledky_region_1, vysledky_region_2]            
                slovnik_konecnych_dat[each[okrsek_obec]] = {"Location":each["název"],
                                  "Registered":y[0][0]["registrovanych"],
                                  "Envelopes":y[0][0]["obalky"],
                                  "Valid":y[0][0]["platnych"]}
    
                for iterator in range(0,len(y[1])):
                    (slovnik_konecnych_dat[each[okrsek_obec]][y[1][iterator]
                        ["nazev_strany"]]) = y[1][iterator]["pocet_hlasu"]

            except IndexError:
                pass

    return slovnik_konecnych_dat

def csv_zapisovac(
    slovnik_konecnych_dat : dict,
    file_name : str,
):
    
    """
    zapisovani dat do souboru .csv
    pouziva slovnik konecnych dat a nazev souboru zadany uzivatelem.
    Je pouzit delimiter ; a encoding windows-1250, jelikož obsahuje 
    českou abecedu. 
    Mezera mezi tisíci a stovkami není řešena, dá se řešit snadno v excelu.
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
    elif url not in list_of_webpages(soup, w, x, y):
        print("incorrect webpage adress")
        sys.exit()
    # Uzemni celek Zahranici ma jako jediny odlisnou webovou strukturu
    # a proto ma sve vlastni reseni.
    elif url == "https://www.volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
        slovnik_konecnych_dat = main_function(url, zahranici = True)

    # Vsechny ostatni uzemni celky jsou zpracovavany trochu jinym zpusobem, 
    # finalni vygenerovany slovnik ma vsak v obou pripadech stejnou strukturu.
    else:
        slovnik_konecnych_dat = main_function(url, zahranici = False)
    
    csv_zapisovac(slovnik_konecnych_dat, file_name)
    print("end")


if __name__ == "__main__":
    print("beginning")    
    url = str(sys.argv[1])
    file_name = str(sys.argv[2])
    basic_function(url, file_name)