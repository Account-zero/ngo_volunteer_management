from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "Tell the organization why you'd like to volunteer for this opportunity (optional)"
            }),
        }
