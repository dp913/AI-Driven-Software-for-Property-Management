import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from properties.models import Property, Unit


# Create your views here.

@login_required
def tenant_dashboard(request):
    tenant_user = request.user
    try:
        unit = Unit.objects.select_related('property', 'property__managed_by').get(tenant=tenant_user)
    except Unit.DoesNotExist:
        unit = None

    # Calculate the 1st of the next month
    today = datetime.date.today()
    if today.month == 12:
        next_due_date = datetime.date(today.year + 1, 1, 1)
    else:
        next_due_date = datetime.date(today.year, today.month + 1, 1)
    return render(request, 'tenant_dashboard.html', {
        'unit': unit,
        'next_due_date': next_due_date,
    })


@login_required
def tenant_unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id, tenant=request.user)
    property = unit.property
    manager = property.managed_by

    return render(request, 'tenant_unit_detail.html', {
        'unit': unit,
        'property': property,
        'manager': manager,
    })

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