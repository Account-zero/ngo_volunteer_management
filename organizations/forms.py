from django import forms
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "description", "mission", "logo", "website", "email", "phone", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "mission": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
