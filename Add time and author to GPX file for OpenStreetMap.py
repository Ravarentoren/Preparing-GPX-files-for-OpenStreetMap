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

