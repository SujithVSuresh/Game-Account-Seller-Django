import django_filters
from .models import GameAccounts
from django.forms.widgets import TextInput

from . models import *

class PostFilter(django_filters.FilterSet):
    #start_date = DateFilter(field_name="date_created", lookup_expr="gte")
    #end_date = DateFilter(field_name="date_created", lookup_expr="lte")
    #note = CharFilter(field_name='note', lookup_expr='icontains') #for character search
    from_rate = django_filters.NumberFilter(field_name='rate', lookup_expr='gte', label='Greater than or equal to:', widget=TextInput(attrs={'placeholder': 'Enter Amount'}))
    to_rate = django_filters.NumberFilter(field_name='rate', lookup_expr='lte', label='Less than or equal to:', widget=TextInput(attrs={'placeholder': 'Enter Amount'}))
    class Meta:
        model = GameAccounts
        fields = ['rate', ]


      

