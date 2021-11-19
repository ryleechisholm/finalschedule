import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class MessageFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['user']