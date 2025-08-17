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






