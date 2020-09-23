from .models import Endereco

import django_filters

class EnderecoFilter(django_filters.FilterSet):
    cidade = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Endereco
        fields = ['__all__']