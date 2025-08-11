# Názvy souborů - Vyčistit GPX soubory - Clean gpx file
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
