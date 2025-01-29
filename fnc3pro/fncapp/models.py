from django.db import models

class TipoFondo(models.Model):
    nome = models.CharField(max_length=255)
    percentuale_dad = models.FloatField(default=0)
    percentuale_fad = models.FloatField(default=0)

    def __str__(self):
        return self.nome
    
class Modulo(models.Model):
    denominazione = models.TextField(blank=True, null=True)
    risultato_atteso = models.TextField(blank=True, null=True)
    ore = models.FloatField(blank=True, null=True)
    ada = models.TextField(blank=True, null=True)
    processo = models.TextField(blank=True, null=True)
    sep = models.TextField(blank=True, null=True)
    specificita_risultato = models.TextField(blank=True, null=True)
    entrecomp = models.TextField(blank=True, null=True)
    lifecomp = models.TextField(blank=True, null=True)
    qcer = models.TextField(blank=True, null=True)
    livello_di_standard = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
class CodiceAteco(models.Model):
    codice = models.CharField(max_length=20)
    descrizione = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.codice
    
class Azienda(models.Model):
    nome = models.CharField(max_length=255)
    partitaiva = models.CharField(max_length=20, blank=True, null=True)
    codiceateco = models.ForeignKey(CodiceAteco, on_delete=models.SET_NULL, null=True, related_name='aziende')
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    cellulare = models.CharField(max_length=30, blank=True, null=True)
    indirizzosl = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nome
    
class Dipendente(models.Model):
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255, blank=True, null=True)
    sesso = models.CharField(max_length=1, blank=True, null=True)
    datanascita = models.DateField(blank=True, null=True)
    luogonascita = models.CharField(max_length=255, blank=True, null=True)
    provincianascita = models.CharField(max_length=255, blank=True, null=True)
    codicefiscale = models.CharField(max_length=16, blank=True, null=True)
    dataassunzione = models.DateField(blank=True, null=True)
    datacessazione = models.DateField(blank=True, null=True)
    tipocontratto = models.CharField(max_length=255, blank=True, null=True)
    livellocontratto = models.CharField(max_length=255, blank=True, null=True)
    oresettimanali = models.FloatField(blank=True, null=True)
    percparttime = models.FloatField(blank=True, null=True)
    qualifica = models.CharField(max_length=255, blank=True, null=True)
    mansione = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE, related_name='dipendenti')
    def __str__(self):
        return self.nome
    
class Progetto(models.Model):
    nome = models.CharField(max_length=255)
    data_avvio = models.DateField(blank=True, null=True)
    stato = models.CharField(max_length=50, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    aziende = models.ManyToManyField(Azienda, through='ProgettoAzienda')
    def __str__(self):
        return self.nome
    
class ProgettoAzienda(models.Model):
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)
    capofila = models.BooleanField(default=False)
    class Meta:
        unique_together = ('progetto', 'azienda')
        
class PianoFormativo(models.Model):
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='piani_formativi')
    fondo = models.ForeignKey(TipoFondo, on_delete=models.SET_NULL, null=True, related_name='piani_formativi')
    moduli = models.ManyToManyField(Modulo, through='PianoModulo')
    denominazione = models.TextField(blank=True, null=True)
    processi_innovazione_1 = models.TextField(blank=True, null=True)
    processi_innovazione_2 = models.TextField(blank=True, null=True)
    fabbisogno_formativo = models.TextField(blank=True, null=True)
    intervento_formativo = models.TextField(blank=True, null=True)
    informazione_comunicazione = models.TextField(blank=True, null=True)
    processo_valorizzazione = models.TextField(blank=True, null=True)
    processo_valorizzazione_options = models.TextField(blank=True, null=True)
    metodologie_didattiche = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
class PianoModulo(models.Model):
    piano_formativo = models.ForeignKey(PianoFormativo, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    ore_in_presenza = models.FloatField(blank=True, null=True)
    ore_on_the_job = models.FloatField(blank=True, null=True)
    fad_sincrona = models.FloatField(blank=True, null=True)
    fad_asincrona = models.FloatField(blank=True, null=True)
    dad = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('piano_formativo', 'modulo')
        
class Timesheet(models.Model):
    dipendente = models.ForeignKey(Dipendente, on_delete=models.CASCADE)
    piano_modulo = models.ForeignKey(PianoModulo, on_delete=models.CASCADE)
    ore_previste = models.FloatField(blank=True, null=True)
    ore_effettuate = models.FloatField(blank=True, null=True)
    importo_retributivo = models.FloatField(blank=True, null=True)
    importo_contributivo = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('dipendente', 'piano_modulo')

class RappresentanteSindacale(models.Model):
    nome_cognome = models.CharField(max_length=100, blank=False, null=False)
    data_nascita = models.DateField(blank=False, null=False)
    luogo_nascita = models.CharField(max_length=100, blank=False, null=False)
    citta_residenza = models.CharField(max_length=100, blank=False, null=False)
    via_residenza = models.CharField(max_length=200, blank=False, null=False)
    numero_civico = models.CharField(max_length=10, blank=False, null=False)
    codice_fiscale = models.CharField(max_length=16, blank=False, null=False)  
    firma = models.TextField(blank=False, null=False) 

    def __str__(self):
        return self.nome_cognome
