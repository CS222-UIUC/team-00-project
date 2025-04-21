from django import forms
from .models import UserTextData


class UserTextDataForm(forms.ModelForm):
    class Meta:
        model = UserTextData
        fields = ["name", "text_data"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "text_data": forms.Textarea(attrs={"rows": 10, "cols": 50, "id": "editor"}),
        }
