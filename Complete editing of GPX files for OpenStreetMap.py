# KOMPLETNÍ ZPRACOVÁNÍ GPX SOUBORŮ pro OpenStreetMap 
# Autor: Ravarentoren - Gemini
# Popis: Tento skript sjednocuje všechny předchozí funkce do jednoho
#              uživatelsky přívětivého nástroje s grafickým rozhraním.

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
