from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from properties.models import Property, Unit


# Create your views here.

@login_required
def tenant_dashboard(request):
    return render(request, 'tenant_dashboard.html')

@login_required
def landlord_dashboard(request):
    landlord = request.user
    properties = Property.objects.filter(landlord=landlord)
    units = Unit.objects.filter(property__in=properties)

    total_units = units.count()
    occupied_units = units.exclude(tenant=None).count()

    occupancy_rate = round((occupied_units / total_units) * 100, 2) if total_units else 0

    return render(request, 'landlord_dashboard.html', {
        'occupancy_rate': occupancy_rate,
        # Include other context variables here
    })

@login_required
def manager_dashboard(request):
    user = request.user
    active_properties_count = Property.objects.filter(managed_by=user).count()

    context = {
        'active_properties_count': active_properties_count,
        # Add other dashboard metrics here
    }
    return render(request, 'manager_dashboard.html', context)