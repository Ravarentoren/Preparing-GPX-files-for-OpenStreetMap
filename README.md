🛠️🔧 KOMPLETNÍ ZPRACOVÁNÍ GPX SOUBORŮ pro OpenStreetMap ⛓️⚒️
🥷 Autor: Ravarentoren - Gemini ⚙️
📜 Popis: Tento skript sjednocuje všechny předchozí funkce do jednoho, uživatelsky přívětivého nástroje s grafickým rozhraním.

import gpxpy
import gpxpy.gpx
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

# --- KONSTANTY A NASTAVENÍ ---
# Zde si můžete nastavit jméno autora nebo název vašeho projektu.
# Tento údaj se objeví v metadatech výsledného GPX souboru.
AUTOR_TEXT = 'Zde doplňte své jméno či název projektu' 


# --- JÁDRO FUNKCÍ ---

def vycisti_gpx_obsah(gpx_text):
    """
    Funkce pro vyčištění obsahu GPX souboru od tagů <extensions>.
    Pracuje s textovým řetězcem, aby se předešlo chybám při parsování.
    """
    radky_out = []
    preskakuji_blok = False
    for radek in gpx_text.splitlines(True):
        if '<extensions>' in radek:
            preskakuji_blok = True
            continue
        if '</extensions>' in radek:
            preskakuji_blok = False
            continue
        if not preskakuji_blok:
            radky_out.append(radek)
    return "".join(radky_out)

def zpracuj_gpx_objekt(gpx, novy_nazev):
    """
    Aplikuje finální úpravy na gpx objekt: název, autor a časové značky.
    """
    # Nastavení autora a hlavního názvu
    gpx.creator = AUTOR_TEXT
    gpx.name = novy_nazev
    
    # Odstranění názvů z jednotlivých tracků, aby byl jen jeden hlavní
    for track in gpx.tracks:
        track.name = None

    # Doplnění časových značek
    startovni_cas = datetime.now()
    aktualni_cas = startovni_cas
    pocet_bodu = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                point.time = aktualni_cas
                aktualni_cas += timedelta(seconds=1)
                pocet_bodu += 1
                
    print(f"Zpracováno {pocet_bodu} bodů. Autor nastaven na '{AUTOR_TEXT}'. Název nastaven na '{novy_nazev}'.")
    return gpx


# --- HLAVNÍ LOGIKA A UŽIVATELSKÉ ROZHRANÍ ---

def main():
    # Inicializace a skrytí hlavního okna Tkinter
    root = tk.Tk()
    root.withdraw()

    # 1. Výběr režimu (jeden soubor vs. více souborů)
    rezim = simpledialog.askstring("Výběr režimu", "Chcete zpracovat JEDEN soubor nebo VÍCE souborů?\nZadejte 'jeden' nebo 'vice':")
    if rezim is None:
        print("Akce zrušena uživatelem.")
        return
    rezim = rezim.lower().strip()

    # 2. Dotaz na název trasy
    novy_nazev = simpledialog.askstring("Název trasy", "Zadejte název, který bude mít výsledná trasa:")
    if not novy_nazev:
        print("Akce zrušena, nebyl zadán název.")
        return

    # ------------------ REŽIM PRO JEDEN SOUBOR ------------------
    if rezim == 'jeden':
        vstupni_cesta = filedialog.askopenfilename(
            title="Vyberte jeden GPX soubor ke zpracování",
            filetypes=[("GPX soubory", "*.gpx")]
        )
        if not vstupni_cesta:
            print("Akce zrušena, nebyl vybrán soubor.")
            return

        print(f"Zpracovávám soubor: {vstupni_cesta}")
        try:
            # Načtení, vyčištění a parsování
            with open(vstupni_cesta, 'r', encoding='utf-8') as f:
                cisty_obsah = vycisti_gpx_obsah(f.read())
            gpx = gpxpy.parse(cisty_obsah)

            # Finální úpravy
            gpx = zpracuj_gpx_objekt(gpx, novy_nazev)
            
            # Uložení výsledku
            vystupni_cesta = filedialog.asksaveasfilename(
                title="Uložit upravený GPX soubor jako...",
                defaultextension=".gpx",
                initialfile=f"upraveno_{os.path.basename(vstupni_cesta)}",
                filetypes=[("GPX soubory", "*.gpx")]
            )
            if vystupni_cesta:
                with open(vystupni_cesta, 'w', encoding='utf-8') as f:
                    f.write(gpx.to_xml())
                messagebox.showinfo("Hotovo", f"Soubor byl úspěšně zpracován a uložen jako:\n{vystupni_cesta}")

        except Exception as e:
            messagebox.showerror("Chyba", f"Vyskytla se chyba při zpracování souboru:\n{e}")

    # ------------------ REŽIM PRO VÍCE SOUBORŮ ------------------
    elif rezim == 'vice':
        vstupni_cesty = filedialog.askopenfilenames(
            title="Vyberte více GPX souborů ke sloučení a zpracování",
            filetypes=[("GPX soubory", "*.gpx")]
        )
        if not vstupni_cesty:
            print("Akce zrušena, nebyly vybrány soubory.")
            return

        print(f"Nalezeno {len(vstupni_cesty)} souborů ke sloučení.")
        slouceny_gpx = gpxpy.gpx.GPX()

        try:
            # Sloučení a vyčištění všech souborů
            for cesta in sorted(vstupni_cesty):
                print(f"Zpracovávám a přidávám: {os.path.basename(cesta)}")
                with open(cesta, 'r', encoding='utf-8') as f:
                    cisty_obsah = vycisti_gpx_obsah(f.read())
                gpx_k_pridani = gpxpy.parse(cisty_obsah)
                for track in gpx_k_pridani.tracks:
                    slouceny_gpx.tracks.append(track)
            
            # Finální úpravy sloučeného objektu
            slouceny_gpx = zpracuj_gpx_objekt(slouceny_gpx, novy_nazev)
            
            # Uložení výsledku
            vystupni_cesta = filedialog.asksaveasfilename(
                title="Uložit sloučený GPX soubor jako...",
                defaultextension=".gpx",
                initialfile="FINALE_slouceno.gpx",
                filetypes=[("GPX soubory", "*.gpx")]
            )
            if vystupni_cesta:
                with open(vystupni_cesta, 'w', encoding='utf-8') as f:
                    f.write(slouceny_gpx.to_xml())
                messagebox.showinfo("Hotovo", f"Všechny soubory byly úspěšně sloučeny a uloženy jako:\n{vystupni_cesta}")

        except Exception as e:
            messagebox.showerror("Chyba", f"Vyskytla se chyba při zpracování souborů:\n{e}")
            
    else:
        messagebox.showwarning("Neplatná volba", "Zadali jste neplatný režim. Spusťte skript znovu a zadejte 'jeden' nebo 'vice'.")


if __name__ == '__main__':
    main()

----------------

#Sloučit GPX soubory - Merge GPX files
import (delete even with brackets and add name folder containing GPX files)
import gpxpy
import gpxpy.gpx

gpx_files = [f for f in (delete with brackets and write the name folders with GPX files).listdir('.') if f.endswith('.gpx')]
merged_gpx = gpxpy.gpx.GPX()

print(f"Nalezeno {len(gpx_files)} souborů ke sloučení.")

for file_name in sorted(gpx_files):
    try:
        gpx_file = open(file_name, 'r')
        gpx_to_append = gpxpy.parse(gpx_file)
        print(f"Zpracovávám: {file_name}")

        for track in gpx_to_append.tracks:
            merged_gpx.tracks.append(track)
    except Exception as e:
        print(f"Chyba při zpracování souboru {file_name}: {e}")

with open('FINALE_slouceno.gpx', 'w') as f:
    f.write(merged_gpx.to_xml())

print("\nHotovo! Všechny soubory byly sloučeny do 'FINALE_slouceno.gpx'")

----------------------------

#Vyčistit GPX soubory - Clean gpx file
vstupni_soubor = '(delete even with brackets and add input file)'
vystupni_soubor = '(delete even with brackets and add output file)'

print(f"Čistím soubor '{vstupni_soubor}'...")

try:
    # Otevřeme oba soubory najednou
    with open(vstupni_soubor, 'r') as f_in, open(vystupni_soubor, 'w') as f_out:
        # Budeme si pamatovat, zda jsme v bloku, který se má smazat
        preskakuji_blok = False

        for radek in f_in:
            # Pokud narazíme na začátek bloku, zapneme přeskakování
            if '<extensions>' in radek:
                preskakuji_blok = True
                continue

            # Pokud narazíme na konec bloku, vypneme přeskakování
            if '</extensions>' in radek:
                preskakuji_blok = False
                continue

            # Pokud je přeskakování zapnuté, řádek ignorujeme
            if preskakuji_blok:
                continue

            # Pokud jsme se dostali až sem, je to dobrý řádek a zapíšeme ho
            f_out.write(radek)

    print(f"Hotovo! Vyčištěný soubor byl uložen jako '{vystupni_soubor}'.")

except FileNotFoundError:
    print(f"\nCHYBA: Vstupní soubor '{vstupni_soubor}' nebyl nalezen!")
    print("Zkontrolujte, zda jste ve správné složce a že název souboru ve skriptu odpovídá skutečnosti.")

--------------

import xml.etree.ElementTree as ET

# Upravit název GPX souboru - Edit name GPX file
vstupni_soubor = '( delete even with brackets and add the name of the input GPX file)'
vystupni_soubor = '(delete even with brackets and add the output file name)'

# Nový název, který chceme vložit (více řádků pomocí trojitých uvozovek)
novy_nazev_text = """(delete even with brackets and add the desired file name)"""

print(f"Upravuji názvy v souboru '{vstupni_soubor}'...")

try:
    # Zaregistrujeme namespace, aby se zachoval ve výstupu
    ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
    
    tree = ET.parse(vstupni_soubor)
    root = tree.getroot()
    
    # Definujeme namespace pro hledání tagů
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}

    # Najdeme a odstraníme všechny staré <name> tagy uvnitř <trk>
    pocet_smazanych = 0
    for trk in root.findall('gpx:trk', ns):
        name_tag = trk.find('gpx:name', ns)
        if name_tag is not None:
            trk.remove(name_tag)
            pocet_smazanych += 1
    
    print(f"Odstraněno {pocet_smazanych} původních názvů tras.")

    # Vytvoříme nový <name> tag
    novy_name_tag = ET.Element('name')
    novy_name_tag.text = novy_nazev_text
    
    # Najdeme <desc> tag a vložíme náš nový <name> tag hned za něj
    desc_tag = root.find('gpx:desc', ns)
    if desc_tag is not None:
        # Získáme index <desc> tagu a vložíme nový za něj
        desc_index = list(root).index(desc_tag)
        root.insert(desc_index + 1, novy_name_tag)
        print("Nový hlavní název byl úspěšně vložen.")
    else:
        # Pokud by tam <desc> nebyl, vložíme ho na začátek
        root.insert(0, novy_name_tag)

    # Uložíme finální soubor
    tree.write(vystupni_soubor, encoding='UTF-8', xml_declaration=True)
    print(f"\nHotovo! Upravený soubor byl uložen jako '{vystupni_soubor}'.")

except FileNotFoundError:
    print(f"\nCHYBA: Vstupní soubor '{vstupni_soubor}' nebyl nalezen!")
except Exception as e:
    print(f"Vyskytla se nečekaná chyba: {e}")

-----------------

# Doplnit čas a autora do GPX souboru pro OpenStreetMap
# Doplňuje časové značky po sekundách a vkládá autora do metadat.

import gpxpy
import gpxpy.gpx
from datetime import datetime, timedelta

# --- NASTAVENÍ ---
# Zde si můžete nastavit jméno autora nebo název vašeho projektu.
# Tento údaj se objeví v metadatech výsledného GPX souboru.
AUTOR_TEXT = 'Zde doplňte své jméno či název projektu' 
# -----------------

# Získání počátečního času z prvního bodu souboru, pokud existuje.
# Pokud neexistuje, použije se aktuální systémový čas.
startovni_cas = None
try:
    with open(vstupni_soubor, 'r') as f:
        gpx_temp = gpxpy.parse(f)
        if gpx_temp.tracks and gpx_temp.tracks[0].segments and gpx_temp.tracks[0].segments[0].points:
            prvni_bod = gpx_temp.tracks[0].segments[0].points[0]
            if prvni_bod.time:
                startovni_cas = prvni_bod.time.replace(tzinfo=None) # Odstranění časové zóny pro jednodušší manipulaci
                print(f"Nalezen počáteční čas v souboru: {startovni_cas}")

except Exception:
    pass # Pokud se nepodaří čas najít, startovni_cas zůstane None

if startovni_cas is None:
    startovni_cas = datetime.now()
    print(f"Počáteční čas v souboru nenalezen, použije se aktuální čas: {startovni_cas.strftime('%Y-%m-%d %H:%M:%S')}")

aktualni_cas = startovni_cas

try:
    print(f"\nZpracovávám soubor '{vstupni_soubor}'...")
    
    # Otevření a naparsování vstupního souboru
    with open(vstupni_soubor, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Nastavení autora (creator)
    gpx.creator = autor_text
    print(f"Autor nastaven na: '{autor_text}'")

    # Procházení všech bodů a doplňování času
    pocet_bodu = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                point.time = aktualni_cas
                aktualni_cas += timedelta(seconds=1)
                pocet_bodu += 1
    
    print(f"Časová značka byla úspěšně doplněna k {pocet_bodu} bodům.")

    # Uložení upraveného souboru
    with open(vystupni_soubor, 'w') as f:
        f.write(gpx.to_xml())

    print(f"\nHotovo! Upravený soubor byl uložen jako '{vystupni_soubor}'.")

except FileNotFoundError:
    print(f"\nCHYBA: Vstupní soubor '{vstupni_soubor}' nebyl nalezen!")
except Exception as e:
    print(f"Vyskytla se nečekaná chyba: {e}")






