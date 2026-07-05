from django import forms

from .models import Estudiante


class EstudianteForm(forms.ModelForm):
    """
    Formulario reutilizado tanto en CreateView como en UpdateView.

    Al basarse en ModelForm no se duplica la definición de campos ni la
    validación (por ejemplo, email único ya se valida a partir del modelo).
    """

    class Meta:
        model = Estudiante
        fields = ["nombre", "apellido", "email", "curso", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
