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


