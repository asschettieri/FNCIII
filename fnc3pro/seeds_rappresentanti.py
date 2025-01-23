# seeds_rappresentanti.py
import os
import django
import datetime

# ✅ Configura il modulo delle impostazioni Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fnc3pro.settings")
django.setup()

# Importa il modello richiesto
from fncapp.models import RappresentanteSindacale

def run():
    rappresentanti = [
        {
            "nome_cognome": "STEFANO POPOLO",
            "luogo_nascita": "NAPOLI",
            "data_nascita": datetime.date(1993, 7, 6),
            "citta_residenza": "NAPOLI",
            "via_residenza": "LE CAMPI FLEGREI",
            "numero_civico": "31 BIS",
            "codice_fiscale": "PPLSFN93L06F839B",
            "firma": "N/A",
        },
        {
            "nome_cognome": "GIOVANNA BRANCACCIO",
            "luogo_nascita": "NAPOLI",
            "data_nascita": datetime.date(1960, 4, 21),
            "citta_residenza": "NAPOLI",
            "via_residenza": "LE CAMPI FLEGREI",
            "numero_civico": "80",
            "codice_fiscale": "BRNGNN60D61F839W",
            "firma": "N/A",
        },
        {
            "nome_cognome": "ARMANDO COPPOLA",
            "luogo_nascita": "NAPOLI",
            "data_nascita": datetime.date(1977, 5, 13),
            "citta_residenza": "NAPOLI",
            "via_residenza": "ENNIO",
            "numero_civico": "18",
            "codice_fiscale": "CPPRND77E13F839W",
            "firma": "N/A",
        },
        {
            "nome_cognome": "FIORINDA CALIENDO",
            "luogo_nascita": "NAPOLI",
            "data_nascita": datetime.date(1975, 5, 2),
            "citta_residenza": "MARIGLIANO",
            "via_residenza": "SETTEMBRINI",
            "numero_civico": "12",
            "codice_fiscale": "CLNFND75E42F839W",
            "firma": "N/A",
        },
    ]

    for rappresentante_data in rappresentanti:
        try:
            rappresentante, created = RappresentanteSindacale.objects.get_or_create(
                codice_fiscale=rappresentante_data["codice_fiscale"],
                defaults={
                    "nome_cognome": rappresentante_data["nome_cognome"],
                    "luogo_nascita": rappresentante_data["luogo_nascita"],
                    "data_nascita": rappresentante_data["data_nascita"],
                    "citta_residenza": rappresentante_data["citta_residenza"],
                    "via_residenza": rappresentante_data["via_residenza"],
                    "numero_civico": rappresentante_data["numero_civico"],
                    "firma": rappresentante_data["firma"],
                },
            )

            if created:
                print(f"✅ Rappresentante {rappresentante.nome_cognome} aggiunto con successo.")
            else:
                print(f"⚠️ Rappresentante con CF {rappresentante.codice_fiscale} esiste già. Nessuna modifica effettuata.")

        except Exception as e:
            print(f"❌ Errore durante l'elaborazione di {rappresentante_data['nome_cognome']}: {e}")

    print("Dati dei rappresentanti sindacali importati con successo!")

if __name__ == "__main__":
    run()
