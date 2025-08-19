from django import forms
from .models import rwmat

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = rwmat
        fields = ["name", "quantity", "unit"]
        labels = {
            "name": "نام ماده",
            "quantity": "مقدار",
            "unit": "واحد",
        }
