from django import forms
from .models import Property
from .models import Unit
from users.models import CustomUser

class FullNameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Assumes CustomUser has first_name and last_name fields
        return f"{obj.first_name} {obj.last_name}".strip() if obj.first_name or obj.last_name else obj.username


class PropertyForm(forms.ModelForm):
    landlord = FullNameModelChoiceField(
        queryset=CustomUser.objects.filter(role='landlord', unit__isnull=True),
        required=True,
        label='Assign Landlord'
    )

    class Meta:
        model = Property
        fields = ['address', 'unit_count', 'landlord']



class AssignTenantForm(forms.Form):
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.none(),
        label='Select Unit'
    )
    tenant = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='tenant', unit__isnull=True),
        label='Select Tenant'
    )

    def __init__(self, *args, **kwargs):
        property = kwargs.pop('property', None)
        super().__init__(*args, **kwargs)
        if property:
            self.fields['unit'].queryset = Unit.objects.filter(property=property, tenant__isnull=True)
