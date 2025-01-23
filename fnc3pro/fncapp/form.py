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
        fields = ['nome', 'data_inizio', 'data_fine', 'ore_totali', 'descrizione', 'fondo', 'moduli']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inizio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fine': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ore_totali': forms.NumberInput(attrs={'class': 'form-control'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fondo': forms.Select(attrs={'class': 'form-select'}),
            'moduli': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
PianoFormativoInlineFormSet = inlineformset_factory(
    Progetto,
    PianoFormativo,
    form=PianoFormativoForm,
    extra=1,
    can_delete=True
)