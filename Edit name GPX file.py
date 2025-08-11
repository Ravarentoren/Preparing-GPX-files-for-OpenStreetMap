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
