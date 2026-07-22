from django import forms
from .models import HourLog


class HourLogForm(forms.ModelForm):
    class Meta:
        model = HourLog
        fields = ["opportunity", "date", "hours", "description"]
        widgets = {
            "opportunity": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.25", "min": "0.25"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, volunteer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if volunteer is not None:
            from applications.models import Application
            approved_opportunity_ids = Application.objects.filter(
                volunteer=volunteer, status="approved"
            ).values_list("opportunity_id", flat=True)
            self.fields["opportunity"].queryset = self.fields["opportunity"].queryset.filter(
                id__in=approved_opportunity_ids
            )
