from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

BOOTSTRAP_INPUT = "form-control"


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = BOOTSTRAP_INPUT


class VolunteerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = BOOTSTRAP_INPUT

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.VOLUNTEER
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data.get("phone", "")
        if commit:
            user.save()
        return user


class OrganizationSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Contact first name")
    last_name = forms.CharField(max_length=150, required=True, label="Contact last name")
    email = forms.EmailField(required=True)
    organization_name = forms.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = BOOTSTRAP_INPUT

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.ORG_ADMIN
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "date_of_birth", "address", "bio", "profile_picture"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "last_name": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "email": forms.EmailInput(attrs={"class": BOOTSTRAP_INPUT}),
            "phone": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "date_of_birth": forms.DateInput(attrs={"class": BOOTSTRAP_INPUT, "type": "date"}),
            "address": forms.Textarea(attrs={"class": BOOTSTRAP_INPUT, "rows": 3}),
            "bio": forms.Textarea(attrs={"class": BOOTSTRAP_INPUT, "rows": 4}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": BOOTSTRAP_INPUT}))
