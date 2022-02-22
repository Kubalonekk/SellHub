from django.shortcuts import render
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from .filters import *
from .decorators import *
from django.template.context_processors import csrf
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.db.models import Count

def index(request):
    marki = Marka.objects.all()

    ogloszenia = Ogloszenie.objects.all().order_by('-data_dodania')
    myFilter = OgloszenieFilter(request.GET, queryset=ogloszenia)
    ogloszenia = myFilter.qs

    
    context = {
        'ogloszenia': ogloszenia,
        'myFilter': myFilter,
        'marki':marki,
    }

    return render(request, 'SellHub/index.html', context)

def ogloszenie(request):
    # * Funkcja używa HTMX do pobarnia wybranej marki a pozniej do dopasywania QS

    marka = request.GET.get('marka')
    ogloszenia = Ogloszenie.objects.all().order_by('-data_dodania')
    myFilter = OgloszenieFilter(request.GET, queryset=ogloszenia)
    if marka == "reset":
        myFilter.form.marka = None
        pass
    else:
        myFilter.form.marka = marka
        myFilter.form.fields['model'].queryset = Model.objects.filter(marka=marka)
    ogloszenia = myFilter.qs

    context = {
        'ogloszenia': ogloszenia,
        'myFilter': myFilter,
    }
    return render(request, 'SellHub/partials/OgloszenieForm.html', context)



def pojedyncze_ogloszenie(request, pk):

    ogloszenie = Ogloszenie.objects.get(pk=pk)
    if request.user.is_authenticated:
        if ogloszenie.ogloszenie_uzytkownika.uzytkownik != request.user:
            ogloszenie.wyswietlenia += 1
            ogloszenie.save()
        if ogloszenie.ulubione.filter(uzytkownik=request.user):
            flaga = True
        else:
            flaga = False
    else:
        flaga = False
        ogloszenie.wyswietlenia += 1
        ogloszenie.save()
    zdjecia_ogloszenie = ZdjecieOgloszenie.objects.filter(
        ogloszenie=ogloszenie,
        zdjecie_glowne=False,
        )

    context = {
        'ogloszenie': ogloszenie,
        'zdjecia_ogloszenie': zdjecia_ogloszenie,
        'flaga': flaga,

    }

    return render(request, 'SellHub/pojedyncze_ogloszenie.html', context)

@dla_niezalogowanych
def rejestracja(request):

    if request.method == 'POST':
        form = NowyUzytkownikForm(request.POST) 
        if form.is_valid():
            nowy_uzytkownik = form.save()
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            numer_telefonu = form.cleaned_data.get('numer_telefonu')
            nowy_profil = ProfilUzytkownika.objects.create(
                uzytkownik=nowy_uzytkownik,
                imie=first_name,
                nazwisko=last_name,
                email=email,
                numer_telefonu=numer_telefonu,
            )
            messages.success(request, 'Konto zalozone pomyslnie. Witaj ' + nowy_uzytkownik.username)
            zalogowany_uzytkownik = authenticate(
                username=nowy_uzytkownik.username,
                password=request.POST['password1'])
            login(request, zalogowany_uzytkownik)
            return redirect('index')
        else:
            messages.warning(request, 'Cos poszlo nie tak')
    else:
        form = NowyUzytkownikForm()

    context = {
        'form': form,
    }

    return render(request, 'SellHub/rejestracja.html', context)

@dla_zalogowanych
def wylogowanie(request):
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano użytkownika')
    return redirect('index')


@dla_zalogowanych
def dodaj_ogloszenie(request):
    # Widok ten pobiera z formularza ID marki po to aby w późniejszym etapie dodawania Ogłoszenia wyświetlić tylko porządane modele

    if request.user.is_authenticated:
        if request.user.uzytkownik.numer_telefonu is None or request.user.uzytkownik.imie is None or request.user.uzytkownik.nazwisko is None:
            messages.warning(request, 'Aby móc dodać ogłoszenie, musisz uzupełnic dane')    
            return redirect('edytuj_profil')
        else:
            pass
    else:
        messages.warning(request, 'Najpierw musisz się zalogować')
        return redirect('login')
    form = MarkaForm()
    if request.method == 'POST':
        form = MarkaForm(request.POST) 
        if form.is_valid():
            marka = form.cleaned_data.get('marka') 
            return redirect('dodaj_ogloszenie2', pk=marka.id)

    context ={
        'form': form,

    }

    return render(request, 'SellHub/dodaj_ogloszenie1.html', context)

@dla_zalogowanych
def dodaj_ogloszenie2(request, pk):
    if request.user.is_authenticated:
        pass
    else:
        messages.warning(request, 'Aby móc dodać ogłoszenie, musisz uzupełnic dane')    
        return redirect('edytuj_profil')

    form = OgloszenieForm()
    marka = Marka.objects.get(id=pk)
    form.fields['model'].queryset = Model.objects.filter(marka=pk)
    if request.method == 'POST':
        form = OgloszenieForm(request.POST)
        zdjecia = request.FILES.getlist('zdjecia')
        glowne = request.FILES.get('glowne')
        if form.is_valid():
            nowe_ogloszenie = form.save(commit=False)
            nowe_ogloszenie.ogloszenie_uzytkownika = request.user.uzytkownik
            nowe_ogloszenie.marka = marka
            nowe_ogloszenie = form.save()
            glowne_zdjecie = ZdjecieOgloszenie.objects.create(
                ogloszenie = nowe_ogloszenie,
                zdjecie = glowne,
                zdjecie_glowne = True,
            )

            for x in zdjecia:
                nowe_zdjecie = ZdjecieOgloszenie.objects.create(
                    ogloszenie = nowe_ogloszenie,
                    zdjecie = x,
                )
            messages.success(request, 'Pomyślnie dodano ogłoszenie')
        else:
            messages.error(request, 'Coś poszło nie tak')

    context ={
        'form': form,
        'marka': marka,

    }

    return render(request, 'SellHub/dodaj_ogloszenie2.html', context)
@dla_zalogowanych
def edytuj_ogloszenie_galeria(request, pk):

    edytowane_ogloszenie = Ogloszenie.objects.get(pk=pk)
    zdjecia_ogloszenie = ZdjecieOgloszenie.objects.filter(ogloszenie=pk).order_by('-zdjecie_glowne')

    if request.method == 'POST':
        zdjecia = request.FILES.getlist('zdjecia')
        for zdjecie in zdjecia:
            nowe_zdjecie = ZdjecieOgloszenie.objects.create(
                ogloszenie=edytowane_ogloszenie,
                zdjecie=zdjecie,
            )
        messages.success(request, 'Pomyślnie dodano zdjęcie/a')

    context = {
        'edytowane_ogloszenie': edytowane_ogloszenie,
        'zdjecia_ogloszenie': zdjecia_ogloszenie,

    }

    return render(request, 'SellHub/edytuj_ogloszenie_galeria.html', context)

@dla_zalogowanych
def usun_zdjecie(request, pk):

    zdjecie_usun = ZdjecieOgloszenie.objects.get(pk=pk)
    ogloszenie = zdjecie_usun.ogloszenie
    zdjecie_usun.delete()
    messages.success(request, 'Pomyślnie usunięto zdjęcie')
    return redirect('edytuj_ogloszenie_galeria', ogloszenie.id)


@dla_zalogowanych
def usun_ogloszenie(request, pk):

    ogloszenie_usun = Ogloszenie.objects.get(pk=pk)
    tytul = ogloszenie_usun.tytul
    messages.success(request, 'Pomyślnie usunięto ogloszenie: ' + tytul )
    ogloszenie_usun.delete()
    return redirect('twoje_ogloszenia')

@dla_zalogowanych
def ustaw_glowne_zdjecie(request, pk):

    ustaw_glowne  = ZdjecieOgloszenie.objects.get(pk=pk)
    ogloszenie = ustaw_glowne.ogloszenie
    if ustaw_glowne.zdjecie_glowne == True:
        messages.warning(request, 'To zdjęcie jest już zdjęciem głównym')
        return redirect('edytuj_ogloszenie_galeria', ogloszenie.id)
    else:
        zdjecia = ZdjecieOgloszenie.objects.filter(ogloszenie=ogloszenie)
        for zdjecie in zdjecia:
            if zdjecie.zdjecie_glowne == True:              
                zdjecie.zdjecie_glowne = False
                zdjecie.save()
            elif zdjecie.id == ustaw_glowne.id:
                zdjecie.zdjecie_glowne = True
                zdjecie.save()
        
        messages.error(request, 'Pomyślnie zmieniono zdjęcie główne')
        return redirect('edytuj_ogloszenie_galeria', ogloszenie.id)


def aktualizuj_ulubione(request, pk):
    ogloszenie = Ogloszenie.objects.get(pk=pk)
    query = ogloszenie.ulubione.all()
    liczba = ogloszenie.ulubione.all().count()
    ogloszenie.ilosc_ulubionych = liczba
    ogloszenie.save()
    pass





@dla_niezalogowanych
def logowanie(request):
    if request.method == 'POST':     
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.uzytkownik.imie:
                messages.success(request, 'Witaj '+ user.uzytkownik.imie)
            else:
                messages.success(request, 'Witaj użytkowniku')
            return redirect('index')
            ...
        else:
            messages.error(request, "Błędny login lub hasło")
        

    context = {

    }

    return render(request, 'SellHub/login.html', context)





@dla_zalogowanych
def edytuj_ogloszenie(request, pk):
    
    edytowane_ogloszenie = Ogloszenie.objects.get(pk=pk)
    if request.user.uzytkownik == edytowane_ogloszenie.ogloszenie_uzytkownika:
        pass
    else:
        messages.warning(request, 'Nie masz dostępu do tej strony')
        return redirect('index')


    form = OgloszenieForm(instance=edytowane_ogloszenie)
    if request.method == 'POST':
        form = OgloszenieForm(request.POST, request.FILES, instance=edytowane_ogloszenie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pomyślnie edytowano ogłoszenie')
            return redirect('index')

    context = {
        'form': form,
        'edytowane_ogloszenie': edytowane_ogloszenie,
    }
    

    return render(request, 'SellHub/edytuj_ogloszenie.html', context)
@dla_zalogowanych
def twoje_ogloszenia(request):

    ogloszenia = Ogloszenie.objects.filter(ogloszenie_uzytkownika = request.user.uzytkownik)


    context = {
        'ogloszenia': ogloszenia,
    }

    return render(request, 'SellHub/twoje_ogloszenia.html', context)

@dla_zalogowanych
def edytuj_profil(request):
   
    profil = request.user.uzytkownik
    form = EdytujProfilUzytkownika(instance=profil)

    if request.method == 'POST':
        form = EdytujProfilUzytkownika(request.POST,instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pomyślnie edytowano profil')
            return redirect('index')


    context = {
        'form': form,

    }

    return render(request, 'SellHub/edytuj_profil.html', context)


def ulubione(request):
    profil_uzytkownika = ProfilUzytkownika.objects.get(uzytkownik = request.user)
    ulubione_ogloszenia = profil_uzytkownika.ulubione_ogloszenia.all()
    context = {
        'ulubione_ogloszenia': ulubione_ogloszenia,

    }
    return render(request, 'SellHub/ulubione.html', context)




# ----------------------------------------------- HTMX ---------------------------------

def usun_z_ulubionych(request, pk):
    # * Widok napisany dla listy Ulubionych ogloszen
    profil_uzytkownika = ProfilUzytkownika.objects.get(uzytkownik = request.user)
    ogloszenie = Ogloszenie.objects.get(pk=pk)
    ogloszenie.ulubione.remove(request.user.uzytkownik)
    aktualizacja = aktualizuj_ulubione(request, pk)
    ulubione_ogloszenia = profil_uzytkownika.ulubione_ogloszenia.all()
    messages.info(request, 'Pomyśnie usunięto ogłoszenie z ulubionych')
    context = {
        'ulubione_ogloszenia': ulubione_ogloszenia,

    }
    return render(request, 'SellHub/partials/ulubione_ogloszenia.html', context) 


def dodaj_lub_usun_ulubione(request, pk):
    #  * widok dodaje lub usuwa Ogloszenie z ulubionych 

    ogloszenie = Ogloszenie.objects.get(pk=pk)
    if ogloszenie.ulubione.filter(uzytkownik=request.user) and ogloszenie.ogloszenie_uzytkownika != request.user.uzytkownik:
        ogloszenie.ulubione.remove(request.user.uzytkownik)
        messages.info(request, 'Pomyśnie usunięto ogłoszenie z ulubionych')
        flaga = False
        
    elif ogloszenie.ogloszenie_uzytkownika == request.user.uzytkownik:
        messages.error(request, 'Nie możesz dodać swojego ogłoszenia do ulubionych')
        flaga = False

    else:
        ogloszenie.ulubione.add(request.user.uzytkownik)
        messages.success(request, 'Pomyśnie dodano ogłoszenie do ulubionych')
        flaga = True

    aktualizacja = aktualizuj_ulubione(request, pk)
    
    ogloszenie = Ogloszenie.objects.get(pk=pk)
    
    context = {
        'ogloszenie': ogloszenie,
        'flaga': flaga,

    }

    return render(request, 'SellHub/partials/dodaj_lub_usun_ulubione.html', context)



def sprawdz_cena(request):
    form = OgloszenieForm(request.GET)    
    return HttpResponse(as_crispy_field(form['cena']))

def sprawdz_moc(request):
    form = OgloszenieForm(request.GET)
    return HttpResponse(as_crispy_field(form['moc_silinka']))

def sprawdz_pojemnosc_silnika(request):
    form = OgloszenieForm(request.GET)
    return HttpResponse(as_crispy_field(form['pojemnosc_silnika']))

def sprawdz_przebieg(request):
    form = OgloszenieForm(request.GET)
    return HttpResponse(as_crispy_field(form['przebieg']))    

def sprawdz_nazwa_uzytkownika(request):
    form = NowyUzytkownikForm(request.GET)
    return HttpResponse(as_crispy_field(form['username']))

