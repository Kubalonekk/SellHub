from cProfile import label
from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField, ModelForm
from django.core.validators import RegexValidator
from .models import *
from datetime import datetime
from django.urls import reverse_lazy


blad = 'Numer telefonu musi zaczynac od +48 i mieć 9 cyfr'

numer_telefonu_regex = RegexValidator(
         regex = r'^[+](48)\d{9}$',
         message=blad
     )




class NowyUzytkownikForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')


        widgets = {
        'username' : forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Nazwa użytkownika',
                                            'hx-get': reverse_lazy('sprawdz_nazwa_uzytkownika'),
                                            'hx-trigger': 'keyup changed delay:0.2s',
                                            'hx-target': '#div_id_username',  #Jak zbadamy formularz , jest to automatycznie tworzony div przez crispy form
                                            }),
        }
    
class MarkaForm(forms.Form):
    marka = ModelChoiceField(queryset=Marka.objects.all(),)


class EdytujProfilUzytkownika(forms.ModelForm):
    class Meta:
        model = ProfilUzytkownika

        exclude = ('uzytkownik', 'ulubione_ogloszenia')


        


# class ZdjecieOgloszenieForm(forms.ModelForm):

#     class Meta:
#         model = ZdjecieOgloszenie

#         fields = ['zdjecie',]

    

class OgloszenieForm(forms.ModelForm):
    class Meta:
        model= Ogloszenie
        
        
        exclude = ('ogloszenie_uzytkownika','marka',)

        labels = {
            'tytul': 'Podaj tytuł ogłoszenia',
            'negocjacja': 'Do negocjacji',
            'tytul': 'Podaj tytuł ogłoszenia',
        }


        widgets = {
            'tytul' : forms.TextInput(attrs={'class': 'form-control',}),
            'model' : forms.Select(attrs={'class': 'form-control',}),
            'cena' : forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Podaj cene w złotówkach',
                                            'hx-get': reverse_lazy('sprawdz_cena'),
                                            'hx-trigger': 'keyup changed delay:0.2s',
                                            'hx-target': '#div_id_cena',  #Jak zbadamy formularz , jest to automatycznie tworzony div przez crispy form
                                            }),
            'opis' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dokładnie opisz auto',}),
            'rok_produkcji': forms.DateInput(attrs={'class': 'form-control',
                                                     'type': 'date',
                                                     'max': datetime.now().date(),
                                                      }),
            'moc_silinka' : forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'km',
                                            'hx-get': reverse_lazy('sprawdz_moc'),
                                            'hx-trigger': 'keyup changed delay:0.2s',
                                            'hx-target': '#div_id_moc_silinka',
                                            }),
            'negocjacja' : forms.Select(attrs={'class': 'form-control',}),
            'pojemnosc_silnika' : forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'cm³',
                                                        'hx-get': reverse_lazy('sprawdz_pojemnosc_silnika'),
                                                        'hx-trigger': 'keyup changed delay:0.2s',
                                                        'hx-target': '#div_id_pojemnosc_silnika',
                                                        }),
            'nadwozie' : forms.Select(attrs={'class': 'form-control',}),
            'paliwo' : forms.Select(attrs={'class': 'form-control',}),
            'skrzynia_biegow' : forms.Select(attrs={'class': 'form-control',}),
            'stan_techniczny' : forms.Select(attrs={'class': 'form-control',}),
            'przebieg' : forms.TextInput(attrs={'class': 'form-control',
                                                'hx-get': reverse_lazy('sprawdz_przebieg'),
                                                'hx-trigger': 'keyup changed delay:0.2s',
                                                'hx-target': '#div_id_przebieg',
                                                }),

        }


    #  **Funkcja musi zaczynac sie od clean_ a pozniej nazwa pola

    def clean_cena(self):
        cena = self.cleaned_data['cena']
        if cena > 10000000:
            raise forms.ValidationError("Cena musi być mniejsza niż: 10.000.000" )
        return cena


    def clean_moc_silinka(self):
        moc_silinka = self.cleaned_data['moc_silinka']
        if moc_silinka > 1000:
            raise forms.ValidationError('Moc silnika musi być mniejsza niż 1000')
        return moc_silinka

    def clean_pojemnosc_silnika(self):
        pojemnosc_silnika = self.cleaned_data['pojemnosc_silnika']
        if pojemnosc_silnika > 10000:
            raise forms.ValidationError('Pojemność silnika musi być mniejsza niż 10000')
        return pojemnosc_silnika

    def clean_przebieg(self):
        przebieg = self.cleaned_data['przebieg']
        if przebieg > 10000000:
            raise forms.ValidationError('Przebieg musi być mniejsza niż 10.000.000')
        return przebieg

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Nazwa użytkownika zajęta')
        return username













  
    







