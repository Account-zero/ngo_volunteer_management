from django import forms
from .models import Opportunity, Category
from volunteers.models import Skill


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            "title", "description", "category", "skills_required", "location", "is_remote",
            "start_date", "end_date", "start_time", "end_time", "volunteers_needed", "status",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "skills_required": forms.CheckboxSelectMultiple,
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "is_remote": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "volunteers_needed": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if start and end and end < start:
            raise forms.ValidationError("End date cannot be before start date.")
        return cleaned_data


class OpportunityFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Search opportunities..."}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-select"}))
    is_remote = forms.ChoiceField(
        choices=[("", "Any"), ("1", "Remote"), ("0", "In-person")],
        required=False, widget=forms.Select(attrs={"class": "form-select"}))
