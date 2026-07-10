from django import forms

from .models import Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nombre", "codigo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "codigo": forms.TextInput(attrs={"class": "input"}),
        }
