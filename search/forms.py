from django.forms import ModelForm, CharField
from search.models import SearchText


class SearchForm(ModelForm):
    class Meta:
        model = SearchText
        fields = ("search_item",)
