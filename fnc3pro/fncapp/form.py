from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
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


class PsbsrlRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email aziendale",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-light bg-opacity-50 border-light py-2',
            'placeholder': 'Inserisci la tua email aziendale'
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light bg-opacity-50 border-light py-2',
            'placeholder': 'Inserisci una password sicura'
        })
    )

    password2 = forms.CharField(
        label="Conferma Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light bg-opacity-50 border-light py-2',
            'placeholder': 'Conferma la password'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-light bg-opacity-50 border-light py-2',
                'placeholder': 'Inserisci il tuo username'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        domini_ammessi = ["@psbsrl.com", "@psbsrl.it"]  # Lista dei domini consentiti
        if not any(email.endswith(dominio) for dominio in domini_ammessi):
            raise forms.ValidationError(
                "Devi utilizzare un'email aziendale con dominio psbsrl (es. @psbsrl.com o @psbsrl.it)."
            )
        # Controlla se l'email esiste già
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Questa email è già registrata. Per favore usa un'email diversa."
            )
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light bg-opacity-50 border-light py-2',
            'placeholder': 'Inserisci il tuo username o email'
        }),
        label="Username o Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light bg-opacity-50 border-light py-2',
            'placeholder': 'Inserisci la tua password'
        }),
        label="Password"
    )