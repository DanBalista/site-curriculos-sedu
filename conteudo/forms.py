from django import forms
from .models import Banner, Conteudo
from .widgets import CategoriaPicker


class BannerAdminForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'categoria': CategoriaPicker(include_home=True),
        }


class ConteudoAdminForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = '__all__'
        widgets = {
            'categoria': CategoriaPicker(include_home=False),
        }
