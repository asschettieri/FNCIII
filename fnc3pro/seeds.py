# seeds.py
import os
import django
import datetime
from django.utils import timezone
from django.conf import settings

# ✅ Configura il modulo delle impostazioni Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fnc3pro.settings")
django.setup()  # <--- Necessario per usare i modelli

print(f">>> Database attuale: {settings.DATABASES['default']['NAME']}")

# Importa i modelli dal tuo pacchetto/app
from fncapp.models import (
    TipoFondo,
    Modulo,
    CodiceAteco,
    Azienda,
    Dipendente,
    Progetto,
    ProgettoAzienda,
    PianoFormativo,
    PianoModulo,
    Timesheet,
)

def run():
    # 1. Creiamo alcuni Codici Ateco
    ateco1 = CodiceAteco.objects.create(
        codice="62.01",
        descrizione="Produzione di software su commessa"
    )
    print(f"Creato Codice Ateco: {ateco1}")
    ateco2 = CodiceAteco.objects.create(
        codice="70.22",
        descrizione="Consulenza imprenditoriale e altra consulenza amministrativo-gestionale"
    )
    print(f"Creato Codice Ateco: {ateco2}")

    # 2. Creiamo dei Tipi di Fondo
    fondo1 = TipoFondo.objects.create(nome="Fondo Interprofessionale A")
    print(f"Creato Tipo Fondo: {fondo1}")
    fondo2 = TipoFondo.objects.create(nome="Fondo Interprofessionale B")
    print(f"Creato Tipo Fondo: {fondo2}")

    # 3. Creiamo alcune Aziende
    az1 = Azienda.objects.create(
        nome="Azienda Alpha",
        partitaiva="12345678901",
        codiceateco=ateco1,
        email="info@aziendaalpha.it",
        telefono="0123456789",
        cellulare="3391234567",
        indirizzosl="Via Roma, 10 - Milano",
        note="Azienda specializzata in software gestionale",
    )
    print(f"Creata Azienda: {az1}")
    az2 = Azienda.objects.create(
        nome="Beta Solutions",
        partitaiva="98765432109",
        codiceateco=ateco2,
        email="contact@betasolutions.com",
        telefono="055667788",
        cellulare="3461234567",
        indirizzosl="Piazza Verdi, 5 - Roma",
        note="Società di consulenza manageriale",
    )
    print(f"Creata Azienda: {az2}")

    # 4. Creiamo dei Dipendenti associati alle aziende
    dip1 = Dipendente.objects.create(
        nome="Mario",
        cognome="Rossi",
        sesso="M",
        datanascita=datetime.date(1985, 4, 12),
        luogonascita="Milano",
        provincianascita="MI",
        codicefiscale="RSSMRA85D12H501L",
        dataassunzione=datetime.date(2015, 9, 1),
        datacessazione=None,
        tipocontratto="Tempo Indeterminato",
        livellocontratto="Senior Developer",
        oresettimanali=40,
        percparttime=0,
        qualifica="Ingegnere",
        mansione="Sviluppatore",
        note="Ottimo lavoratore",
        email="mario.rossi@aziendaalpha.it",
        telefono="123456789",
        azienda=az1
    )
    print(f"Creato Dipendente: {dip1}")
    dip2 = Dipendente.objects.create(
        nome="Luisa",
        cognome="Bianchi",
        sesso="F",
        datanascita=datetime.date(1990, 11, 25),
        luogonascita="Roma",
        provincianascita="RM",
        codicefiscale="BNCLSA90S65H501M",
        dataassunzione=datetime.date(2018, 3, 15),
        datacessazione=None,
        tipocontratto="Part-Time",
        livellocontratto="Junior Analyst",
        oresettimanali=20,
        percparttime=50,
        qualifica="Analista",
        mansione="Analisi dati",
        note="Specializzata in analisi finanziaria",
        email="luisa.bianchi@betasolutions.com",
        telefono="987654321",
        azienda=az2
    )
    print(f"Creato Dipendente: {dip2}")

    # 5. Creiamo alcuni Progetti
    prj1 = Progetto.objects.create(
        nome="Progetto Alfa",
        data_avvio=datetime.date(2025, 5, 20),
        stato="In Corso",
        descrizione="Implementazione di un nuovo CRM aziendale",
    )
    print(f"Creato Progetto: {prj1}")
    prj2 = Progetto.objects.create(
        nome="Progetto Beta",
        data_avvio=datetime.date(2025, 6, 10),
        stato="Sospeso",
        descrizione="Ricerca e sviluppo su IA generativa",
    )
    print(f"Creato Progetto: {prj2}")

    # Creiamo il 'through' ProgettoAzienda per indicare che "Azienda Alpha" è coinvolta in prj1
    ProgettoAzienda.objects.create(
        progetto=prj1,
        azienda=az1,
        capofila=True
    )
    print(f"Creato ProgettoAzienda per {az1} in {prj1}")
    # Coinvolgiamo Beta Solutions nel Progetto Beta
    ProgettoAzienda.objects.create(
        progetto=prj2,
        azienda=az2,
        capofila=False
    )
    print(f"Creato ProgettoAzienda per {az2} in {prj2}")

    # 6. Creiamo dei Moduli (opzionale, se vuoi specificare i moduli didattici)
    modulo1 = Modulo.objects.create(nome="Introduzione a Python")
    print(f"Creato Modulo: {modulo1}")
    modulo2 = Modulo.objects.create(nome="Data Analysis con Python e Pandas")
    print(f"Creato Modulo: {modulo2}")
    modulo3 = Modulo.objects.create(nome="Introduzione a Machine Learning")
    print(f"Creato Modulo: {modulo3}")

    # 7. Creiamo alcuni Piani Formativi
    pf1 = PianoFormativo.objects.create(
        nome="Piano Formativo Python",
        progetto=prj1,    # associamo al progetto Alfa
        fondo=fondo1,     # associamo un tipo di fondo
        data_inizio=datetime.date(2025, 1, 1),
        data_fine=datetime.date(2025, 2, 1),
        ore_totali=80,
        descrizione="Corso intensivo su Python e Django",
    )
    print(f"Creato Piano Formativo: {pf1}")
    pf2 = PianoFormativo.objects.create(
        nome="Piano Formativo DataScience",
        progetto=prj2,    # associamo al progetto Beta
        fondo=fondo2,
        data_inizio=datetime.date(2025, 3, 1),
        data_fine=datetime.date(2025, 4, 15),
        ore_totali=120,
        descrizione="Introduzione all'analisi dati e machine learning",
    )
    print(f"Creato Piano Formativo: {pf2}")

    # 8. Creiamo la relazione Pianiformativo-Modulo (through PianoModulo)
    PianoModulo.objects.create(
        piano_formativo=pf1,
        modulo=modulo1
    )
    print(f"Creato PianoModulo per {pf1} e {modulo1}")
    PianoModulo.objects.create(
        piano_formativo=pf1,
        modulo=modulo2
    )
    print(f"Creato PianoModulo per {pf1} e {modulo2}")
    PianoModulo.objects.create(
        piano_formativo=pf2,
        modulo=modulo3
    )
    print(f"Creato PianoModulo per {pf2} e {modulo3}")

    # 9. Creiamo dei Timesheet di esempio
    #    (ipotizzando che 'importo_retributivo' e 'importo_contributivo' siano cifre orarie)
    pm1 = PianoModulo.objects.get(piano_formativo=pf1, modulo=modulo1)
    pm2 = PianoModulo.objects.get(piano_formativo=pf1, modulo=modulo2)
    pm3 = PianoModulo.objects.get(piano_formativo=pf2, modulo=modulo3)

    # Mario Rossi (dip1) segue il piano1 (pf1) con i moduli1 e 2
    Timesheet.objects.create(
        dipendente=dip1,
        piano_modulo=pm1,
        ore_previste=40.0,
        ore_effettuate=32.0,
        importo_retributivo=30.0,   # euro/ora
        importo_contributivo=10.0,  # euro/ora
    )
    print(f"Creato Timesheet per {dip1} e {pm1}")
    Timesheet.objects.create(
        dipendente=dip1,
        piano_modulo=pm2,
        ore_previste=40.0,
        ore_effettuate=35.0,
        importo_retributivo=30.0,
        importo_contributivo=10.0,
    )
    print(f"Creato Timesheet per {dip1} e {pm2}")

    # Luisa Bianchi (dip2) segue il piano2 (pf2) con il modulo3
    Timesheet.objects.create(
        dipendente=dip2,
        piano_modulo=pm3,
        ore_previste=50.0,
        ore_effettuate=45.0,
        importo_retributivo=25.0,
        importo_contributivo=8.0,
    )
    print(f"Creato Timesheet per {dip2} e {pm3}")

    print("Dati fittizi inseriti con successo!")

if __name__ == "__main__":
    run()