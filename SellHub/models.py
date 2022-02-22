import re
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class ProfilUzytkownika(models.Model):

    blad = 'Numer telefonu musi zaczynac od +48 i mieć 9 cyfr'

    numer_telefonu_regex = RegexValidator(
        regex = r'^[+](48)\d{9}$',
        message=blad
    )

    uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE, related_name='uzytkownik')
    imie = models.CharField(max_length=100, null=True)
    nazwisko = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    numer_telefonu = models.CharField(validators=[numer_telefonu_regex], max_length=60,
                             null=True,)
    ulubione_ogloszenia = models.ManyToManyField("Ogloszenie", related_name='ulubione', blank=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} login: {self.uzytkownik}"

class Ogloszenie(models.Model):

    NADWOZIE = (
        ('Kabriolet','Kabriolet'),
        ('Sedan','Sedan'),
        ('Coupe','Coupe'),
        ('Hatchback','Kombi'),
        ('SUV','SUV'),
    )

    PALIWO = (
        ('Benzyna','Benzyna'),
        ('Diesel','Diesel'),
        ('LPG','LPG'),
        ('Hybryda','Hybryda'),
    )

    STAN_TECHNICZNY = (
        ('Nieuszkodzony',' Nieuszkodzony'),
        ('Uszkodzony', 'Uszkodzony'),
    )

    SKRZYNIA_BIEGOW = (
        ('Manualna', 'Manualna'),
        ('Automatyczna', 'Automatyczna'),
    )

    NEGOCJACJA = (
        ('Tak', 'Tak'),
        ('Nie', 'Nie'),
    )

    ogloszenie_uzytkownika = models.ForeignKey("ProfilUzytkownika", related_name='ogloszenie_uzytkownik', on_delete=models.CASCADE)
    tytul = models.CharField(max_length=100)
    marka = models.ForeignKey("Marka", related_name="marka_ogloszenie", on_delete=models.CASCADE)
    model = models.ForeignKey("Model", related_name="model_ogloszenie", on_delete=models.CASCADE)
    opis = models.TextField(null=True)
    data_dodania = models.DateTimeField(auto_now_add=True, null=True)
    cena = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    rok_produkcji = models.DateTimeField(null=True)
    moc_silinka = models.DecimalField(max_digits=7, decimal_places=0, null=True)
    negocjacja = models.CharField(max_length=10, choices=NEGOCJACJA, null=True)
    nadwozie = models.CharField(max_length=30, choices=NADWOZIE, null=True)
    paliwo = models.CharField(max_length=30, choices=PALIWO, null=True)
    przebieg = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    stan_techniczny = models.CharField(max_length=15, choices=STAN_TECHNICZNY, null=True)
    skrzynia_biegow = models.CharField(max_length=15, choices=SKRZYNIA_BIEGOW, null=True)
    pojemnosc_silnika = models.DecimalField(max_digits=9, decimal_places=0, null=True,)
    wyswietlenia = models.IntegerField(default=0)
    ilosc_ulubionych = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.tytul}. Użytkownika {self.ogloszenie_uzytkownika.imie} {self.ogloszenie_uzytkownika.nazwisko} {self.ogloszenie_uzytkownika.uzytkownik}"



class ZdjecieOgloszenie(models.Model):
    ogloszenie = models.ForeignKey(Ogloszenie, related_name="zdjecie_ogloszenie", on_delete=models.CASCADE)
    zdjecie = models.ImageField(null=True, blank=True)
    zdjecie_glowne = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.ogloszenie.tytul} {self.ogloszenie.model} {self.ogloszenie.marka} "


class Model(models.Model):
    nazwa = models.CharField(max_length=100)
    marka = models.ForeignKey("Marka", related_name="marka_set", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nazwa}"

class Marka(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nazwa}"


    
    
    

