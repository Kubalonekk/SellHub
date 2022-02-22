"""public_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('wylogowanie/', views.wylogowanie, name='wylogowanie'),
    path('login/', views.logowanie, name='logowanie'),
    path('dodaj_ogloszenie/', views.dodaj_ogloszenie, name='dodaj_ogloszenie'),
    path('dodaj_ogloszenie2/<int:pk>/', views.dodaj_ogloszenie2, name="dodaj_ogloszenie2"),
    path('twoje_ogloszenia/', views.twoje_ogloszenia, name="twoje_ogloszenia"),
    path('edytuj_profil/', views.edytuj_profil, name="edytuj_profil"),
    path('ogloszenie/<int:pk>/', views.pojedyncze_ogloszenie, name="pojedyncze_ogloszenie"),
    path('edytuj_ogloszenie/<int:pk>/', views.edytuj_ogloszenie, name='edytuj_ogloszenie'),
    path('edytuj_ogloszenie/galeria/<int:pk>/', views.edytuj_ogloszenie_galeria, name='edytuj_ogloszenie_galeria'),
    path('usun_zdjecie/<int:pk>/', views.usun_zdjecie, name='usun_zdjecie'),
    path('usun_ogloszenie/<int:pk>/', views.usun_ogloszenie, name='usun_ogloszenie'),
    path('ustaw_glowne_zdjecie/<int:pk>/', views.ustaw_glowne_zdjecie, name='ustaw_glowne_zdjecie'),
    path('dodaj_lub_usun_ulubione/<int:pk>', views.dodaj_lub_usun_ulubione, name="dodaj_lub_usun_ulubione"),
    path('ulubione/', views.ulubione, name='ulubione'),


]


htmx_urlpatterns = [
    path('sprawdz_cena/', views.sprawdz_cena, name='sprawdz_cena'),
    path('sprawdz_moc/', views.sprawdz_moc, name='sprawdz_moc'),
    path('sprawdz_pojemnosc_silnika/', views.sprawdz_pojemnosc_silnika, name="sprawdz_pojemnosc_silnika"),
    path('sprawdz_przebieg/', views.sprawdz_przebieg, name="sprawdz_przebieg"),
    path('ogloszenie/', views.ogloszenie, name="ogloszenie"),
    path('usun_z_ulubionych/<int:pk>', views.usun_z_ulubionych, name="usun_z_ulubionych"),
    path('sprawdz_nazwa_uzytkownika/', views.sprawdz_nazwa_uzytkownika, name='sprawdz_nazwa_uzytkownika'),



]

urlpatterns += htmx_urlpatterns
