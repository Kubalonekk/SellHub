import django_filters
from django_filters import DateFilter

from .models import *

class OgloszenieFilter(django_filters.FilterSet):
    cena__gt = django_filters.NumberFilter(field_name='cena', lookup_expr='gt', label="Cena od")
    cena__lt = django_filters.NumberFilter(field_name='cena', lookup_expr='lt', label="Cena do")
    rok_produkcji__gt = django_filters.NumberFilter(field_name='rok_produkcji', lookup_expr='gt', label="Rok produkcji od")
    rok_produkcji__lt = django_filters.NumberFilter(field_name='rok_produkcji', lookup_expr='lt', label="Rok produkcji do")
    
    class Meta:   
        model = Ogloszenie
        fields = ('marka', 'model','nadwozie', 'paliwo','stan_techniczny','paliwo','skrzynia_biegow',)

