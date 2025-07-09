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

def vyber_atributy_z_radku(tr_tag:"bs4.element.ResultSet"):
    return [tr_tag[3].getText(),tr_tag[4].getText(),tr_tag[7].getText()]

def vyber_atributy_z_radku2(tr_tag:"bs4.element.ResultSet"):
    return [tr_tag[0].getText(),tr_tag[1].getText(),tr_tag[2].getText()]

def vyber_atributy_z_radku3(tr_tag:"bs4.element.ResultSet"):
    return {"Cislo":tr_tag[0].getText(),"název":tr_tag[1].getText()}

def naformatuj_odkaz(cislo,kraj,numnuts):
    return f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={cislo}&xnumnuts={numnuts}"

def scraper(url):
    odp_serveru=get(url)
    odp_serveru.encoding='UTF-8'
    soup=bs(odp_serveru.text,"html.parser")
    return soup
    

def obec(url):
    """
    Scrapeovaci funkce fungujici na urovni konkretni obce.
    Je rozdelena na dve casti, kdy prvni cast scrapne obecnou tabulku
    uvadejici data o poctu Registrovanych, Obalek, a platnych hlasu a 
    druhou cast, ktera scrapne volebni vysledky jednotlivych stran.
    """
    # odp_serveru=get(url)
    # odp_serveru.encoding='UTF-8'
    # soup=bs(odp_serveru.text,"html.parser")
    soup=scraper(url)
    table_tab_top=soup.find("table",{"id":"ps311_t1"})
    vsechny_tr=table_tab_top.find_all("tr") # toto uz je list
    td_ra_radku=[]
    td_ra_radku2=[]
    vysledky=[]    
    for tr in vsechny_tr[2:]:
        td_na_radku=tr.find_all("td")
        data_hrace=vyber_atributy_z_radku(td_na_radku)
        vysledky.append(data_hrace)
    
    vysledky2=[]
    for table in soup.find_all("table",{"class":"table"}):
        try:
            vsechny_tr2=table.find_all("tr")
            for tr2 in vsechny_tr2[2:]:
                td_na_radku2=tr2.find_all("td")
                data_hrace=vyber_atributy_z_radku2(td_na_radku2)
                vysledky2.append(data_hrace)
        except AttributeError:
            pass
    
    return vysledky,vysledky2[1:]

def main_function(url,kraj,numnuts):
    """
    Zajistuje scrapeovani na urovni uzemniho celku. 
    Scrapne cisla vsech jednotlivych obci z uzemniho celku a nazev
    vsech techto obci.
    Nasledne tyto cisla pouzije pro ziskani a vytvoreni url odkazu
    ktere jsou pouzity pro scrapeovani jednotli
    """

    soup2=scraper(url)
    td_ra_radku3=[]
    
    vysledky3=[]
    for table in soup2.find_all("table",{"class":"table"}):
        try:
            vsechny_tr3=table.find_all("tr")
            for tr3 in vsechny_tr3[2:]:
                td_na_radku3=tr3.find_all("td")
                data_hrace=vyber_atributy_z_radku3(td_na_radku3)
                vysledky3.append(data_hrace)
        except AttributeError:
            pass
    
    x={} 
    for each in vysledky3:
        try:
            y=obec(naformatuj_odkaz(each["Cislo"],kraj,numnuts))
    
            x[each["Cislo"]]={"Location":each["název"],
                              "Registered":y[0][0][0],
                              "Envelopes":y[0][0][1],
                              "Valid":y[0][0][2]}
            
            for pskr in range(0,len(y[1])):
                x[each["Cislo"]][y[1][pskr][1]]=y[1][pskr][2]

        except AttributeError:
            pass
    
    return x

def csv_zapisovac(x,file_name):
    """
    zapisovani dat do souboru .csv
    pouziva vygenerovany slovnik hodnot a nazev souboru zadany uzivatelem.
    """    
    hlavicka_helper=list(x.keys())
    hlavicka=list(x[hlavicka_helper[0]].keys())
    hlavicka.insert(0,"Code")
    
    with open(file_name,mode="w",encoding="windows-1250",newline="") as csv_soubor:
        zapisovac=csv.writer(csv_soubor,delimiter=";")
        zapisovac.writerow(hlavicka)
    
        for each in x.keys():
            zapisovac_helper=list(x[each].values())
            zapisovac_helper.insert(0,each)
            zapisovac.writerow(zapisovac_helper)
    
        csv_soubor.close()


def webpage_check():
    """
    Kontrola, zda uzivatel zadal platnou webovou stranku.
    Nejprve scrapne vsechny odkazy z planovane webove stranky, 
    nasledne vytridi dle vyuzitelnosti a vraci list pouzitelnych webovych
    stranek.
    """
    url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    soup=scraper(url)
    
    project_href = [i['href'] for i in soup.find_all('a', href=True)]
    project_href2=[]
    for each in project_href:
        if "xnumnuts" and "ps32" in each or "ps36?" in each:
            each="https://www.volby.cz/pls/ps2017nss/"+each
            project_href2.append(each)

    return project_href2
    

if __name__ == "__main__":
    # url=str(sys.argv[1])
    # file_name=str(sys.argv[2])
    """
    Zakladni funkce kontrolujici, zda byly zadany spravne parametry
    a ve spravnem poradi.
    Pokud ano, spusti script.
    Pokud ne, ukonci jej.
    """
    url="https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105"
    file_name="tentocsv.csv"
    
    if url[-4:]==".csv":
        print("incorrect positioning")
        sys.exit()
    elif url not in webpage_check():
        print("incorrect webpage adress")
        sys.exit()
    else:
        numnuts=url[-4:]
        kraj=url.split("xkraj=",1)[1]
        if kraj[0:2].isdigit():
            kraj=kraj[0:2]
        else:
            kraj=kraj[0:1]
            
        x=main_function(url,kraj,numnuts)
        csv_zapisovac(x,file_name)


 


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    