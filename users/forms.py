from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add form-control class to all fields for styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Limit role choices to only Tenant and Landlord
        self.fields['role'].choices = [
            ('tenant', 'Tenant'),
            ('landlord', 'Landlord'),
        ]


class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        # Limit role choices
        self.fields['role'].choices = [
            ('tenant', 'Tenant'),
            ('landlord', 'Landlord'),
        ]