from django import forms

from .models import Estudiante


class EstudianteForm(forms.ModelForm):
    """Formulario reutilizado por CreateView y UpdateView."""

    class Meta:
        model = Estudiante
        fields = ["nombre", "apellido", "email", "curso", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "apellido": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "curso": forms.Select(attrs={"class": "select"}),
            "activo": forms.CheckboxInput(),
        }
