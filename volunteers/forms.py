from django import forms
from .models import VolunteerProfile, Skill


class VolunteerProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = VolunteerProfile
        fields = ["skills", "interests", "availability_days", "emergency_contact_name", "emergency_contact_phone"]
        widgets = {
            "interests": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "availability_days": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. mon,wed,sat"
            }),
            "emergency_contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_contact_phone": forms.TextInput(attrs={"class": "form-control"}),
        }
