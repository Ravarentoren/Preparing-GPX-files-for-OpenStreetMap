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

