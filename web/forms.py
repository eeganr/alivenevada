from web.models import Place
from django.forms import ModelForm

class MapForm(ModelForm):
    class Meta:
        model = Place
        fields = ("location", "address", "image")