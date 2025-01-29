from django import forms
from fncapp.models import *
from django.forms.models import inlineformset_factory

class ProgettoForm(forms.ModelForm):
    class Meta:
        model = Progetto
        fields = ['nome', 'data_avvio', 'stato', 'descrizione', 'aziende']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il nome del progetto'}),
            'data_avvio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'stato': forms.TextInput(attrs={'class': 'form-control'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aziende': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
     
class PianoFormativoForm(forms.ModelForm):
    class Meta:
        model = PianoFormativo
        fields = [
            'denominazione',
            'fondo',
            'processi_innovazione_1',
            'processi_innovazione_2',
            'fabbisogno_formativo',
            'intervento_formativo',
            'informazione_comunicazione',
            'processo_valorizzazione',
            'processo_valorizzazione_options',
            'metodologie_didattiche',
            'moduli',
        ]
        widgets = {
            'fondo': forms.Select(attrs={'class': 'form-select'}),

            'moduli': forms.SelectMultiple(attrs={'class': 'form-control'}),

            'denominazione': forms.TextInput(attrs={'class': 'form-control'}),

            'processi_innovazione_1': forms.SelectMultiple(choices=[
                ('a', 'sistemi tecnologici e digitali'),
                ('b', "introduzione e sviluppo dell'intelligenza artificiale"),
                ('c', 'sostenibilità ed impatto ambientale'),
                ('d', 'economia circolare'),
                ('e', 'transizione ecologica'),
                ('f', 'efficientamento energetico'),
                ('g', 'welfare aziendale e benessere organizzativo')
            ], attrs={
                'class': 'form-control',
                'multiple': True
            }),

            'processi_innovazione_2': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Processi di innovazione cui il piano formativo è di supporto (Max 30 righe, font Arial 11 interlinea singola)'
            }),

            'fabbisogno_formativo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Fabbisogno formativo collegato al processo di innovazione (Max 30 righe, font Arial 11 interlinea singola)'
            }),

            'intervento_formativo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Capacità dell’intervento formativo di produrre i risultati desiderati (Max 30 righe, font Arial 11 interlinea singola)'
            }),

            'informazione_comunicazione': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Modalità di informazione e comunicazione ai lavoratori riguardanti le finalità del piano formativo (Max 20 righe, font Arial 11 interlinea singola)'
            }),

            'processo_valorizzazione': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Processo di valorizzazione del patrimonio di competenze possedute dai lavoratori (Max 30 righe, font Arial 11 interlinea singola)'
            }),

            'processo_valorizzazione_options': forms.SelectMultiple(choices=[
                ('a', 'test di ingresso'),
                ('b', 'griglie di autovalutazione in ingresso'),
                ('c', 'interviste/colloqui'),
                ('d', 'osservazioni pratiche'),
                ('e', 'portfolio (esperienze lavorative pregresse, background educativo, certificazioni e corsi precedentemente seguiti, ecc…)'),
                ('f', 'altro')
            ], attrs={
                'class': 'form-control',
                'multiple': True
            }),

            'metodologie_didattiche': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descrivere le metodologie didattiche utilizzate (Max 30 righe, font Arial 11 interlinea singola)'
            }),
        }
        labels = {
            'denominazione': 'Denominazione Piano',
            'processi_innovazione_1': 'Processi di innovazione secondo le tipologie previste dall’Avviso FNC3',
            'processi_innovazione_2': 'Processi di innovazione cui il piano formativo è di supporto',
            'fabbisogno_formativo': 'Fabbisogno formativo collegato al processo di innovazione',
            'intervento_formativo': 'Capacità dell’intervento formativo di produrre i risultati desiderati',
            'informazione_comunicazione': 'Modalità di informazione e comunicazione ai lavoratori',
            'processo_valorizzazione': 'Processo di valorizzazione del patrimonio di competenze',
            'processo_valorizzazione_options': 'Opzioni per il processo di valorizzazione',
            'metodologie_didattiche': 'Metodologie didattiche',
        }

    def clean_processi_innovazione_1(self):
        data = self.cleaned_data['processi_innovazione_1']
        return ';'.join(data) if isinstance(data, list) else data

    def clean_processo_valorizzazione_options(self):
        data = self.cleaned_data['processo_valorizzazione_options']
        return ';'.join(data) if isinstance(data, list) else data
        
PianoFormativoInlineFormSet = inlineformset_factory(
    Progetto,
    PianoFormativo,
    form=PianoFormativoForm,
    extra=1,
    can_delete=True
)

class TipoFondoForm(forms.ModelForm):
    class Meta:
        model = TipoFondo
        fields = ['nome', 'percentuale_dad', 'percentuale_fad']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il nome'}),
            'percentuale_dad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci la percentuale DAD'}),
            'percentuale_fad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci la percentuale FAD'}),
        }

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = [
            'denominazione', 'risultato_atteso', 'ore', 'ada', 'processo', 'sep',
            'specificita_risultato', 'entrecomp', 'lifecomp', 'qcer', 'livello_di_standard'
        ]
        widgets = {
            'denominazione': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci la denominazione'}),
            'risultato_atteso': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ore': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci il numero di ore'}),
            'ada': forms.TextInput(attrs={'class': 'form-control'}),
            'processo': forms.TextInput(attrs={'class': 'form-control'}),
            'sep': forms.TextInput(attrs={'class': 'form-control'}),
            'specificita_risultato': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'entrecomp': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Inserisci una Competenza e un Descrittore separato da "-". Per aggiungere più righe usa ";" alla fine di ogni riga.'
            }),
            'lifecomp': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Inserisci una Competenza e un Descrittore separato da "-". Per aggiungere più righe usa ";" alla fine di ogni riga.'
            }),
            'qcer': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Inserisci una Competenza e un Descrittore separato da "-". Per aggiungere più righe usa ";" alla fine di ogni riga.'
            }),
            'livello_di_standard': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Inserisci una Competenza e un Descrittore separato da "-". Per aggiungere più righe usa ";" alla fine di ogni riga.'
            }),
        }
