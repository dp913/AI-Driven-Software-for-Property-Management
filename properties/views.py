from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Property, Unit, PropertyImage
from django.conf import settings
from users.models import CustomUser
from .forms import PropertyForm, AssignTenantForm
from django.contrib import messages
from django.forms import modelformset_factory
import os
import shutil
import re
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def is_property_manager(user):
    return user.is_authenticated and user.role == 'manager'


@login_required
@user_passes_test(is_property_manager)
def manager_properties(request):
    query = request.GET.get('q', '')
    properties = Property.objects.all()

    if query:
        properties = properties.filter(
            Q(address__icontains=query) |
            Q(landlord__first_name__icontains=query) |
            Q(landlord__last_name__icontains=query) |
            Q(managed_by__first_name__icontains=query) |
            Q(managed_by__last_name__icontains=query)
        )

    properties_with_thumbnails = [
        (prop, PropertyImage.objects.filter(property=prop).first()) for prop in properties
    ]

    return render(request, 'properties/manager_properties.html', {
        'properties_with_thumbnails': properties_with_thumbnails,
        'query': query,
    })


@login_required
@user_passes_test(is_property_manager)
def add_property(request):
    from users.models import CustomUser  # If Landlord is a separate model

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        unit_count = int(request.POST.get('unit_count', 0))


        if form.is_valid():
            property = form.save(commit=False)
            property.unit_count = unit_count
            property.managed_by = request.user  # Assign current manager
            property.save()

            # Save images
            images = request.FILES.getlist('photos')
            for img in images:
                PropertyImage.objects.create(property=property, image=img)

            # Save units
            for i in range(1, unit_count + 1):
                unit_name = request.POST.get(f'unit_{i}')

                if unit_name:
                    Unit.objects.create(
                        property=property,
                        unit_number=unit_name,

                    )

            return redirect('manager_properties')
    else:
        form = PropertyForm()

    landlords = CustomUser.objects.filter(role='landlord')
    return render(request, 'properties/add_property.html', {
        'form': form,
        'landlords': landlords
    })


@login_required
@user_passes_test(is_property_manager)
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    all_units = Unit.objects.filter(property=property)
    occupied_units = all_units.filter(tenant__isnull=False)
    vacant_units = all_units.filter(tenant__isnull=True)

    images = PropertyImage.objects.filter(property=property)

    context = {
        'property': property,
        'units': all_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'images': images
    }
    return render(request, 'properties/property_detail.html', context)


@login_required
@user_passes_test(is_property_manager)
def add_tenant_to_property(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = AssignTenantForm(request.POST, property=property)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            tenant = form.cleaned_data['tenant']
            unit.tenant = tenant
            unit.rent_amount = request.POST.get('rent_amount')
            unit.lease_start = request.POST.get('lease_start') or None
            unit.lease_end = request.POST.get('lease_end') or None
            unit.save()
            messages.success(request, f"{tenant.username} assigned to unit {unit.unit_number}.")
            return redirect('property_detail', pk=pk)
    else:
        form = AssignTenantForm(property=property)

    return render(request, 'properties/add_tenant_to_property.html', {
        'form': form,
        'property': property
    })



@login_required
@user_passes_test(is_property_manager)
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)

        if form.is_valid():
            property = form.save(commit=False)  # We'll update unit_count manually later

            # Save new uploaded images
            images = request.FILES.getlist('photos')
            for img in images:
                PropertyImage.objects.create(property=property, image=img)

            # Add new units
            new_units = request.POST.getlist('new_unit[]')

            for name in new_units:
                if name.strip():
                    Unit.objects.create(property=property, unit_number=name.strip())


            # Remove selected unoccupied units
            units_to_remove = request.POST.getlist('delete_units')
            for unit_id in units_to_remove:
                try:
                    unit = Unit.objects.get(id=unit_id, property=property, tenant__isnull=True)
                    unit.delete()
                except Unit.DoesNotExist:
                    continue

            # Update unit_count based on current total units for this property
            property.unit_count = property.unit_set.count()
            property.save()

            messages.success(request, "Property updated successfully.")
            return redirect('property_detail', pk=property.id)
    else:
        form = PropertyForm(instance=property)

    unoccupied_units = property.unit_set.filter(tenant__isnull=True)

    return render(request, 'properties/edit_property.html', {
        'form': form,
        'property': property,
        'images': PropertyImage.objects.filter(property=property),
        'unoccupied_units': unoccupied_units
    })

@login_required
@user_passes_test(is_property_manager)
def delete_property(request, pk):
    if request.method == "POST":
        property_obj = get_object_or_404(Property, pk=pk)

        # Build the image folder name as per upload path logic
        safe_address = re.sub(r'[^a-zA-Z0-9_-]', '', property_obj.address[:20])
        folder_name = f"{property_obj.id}_{safe_address}"
        folder_path = os.path.join(settings.MEDIA_ROOT, 'property_photos', folder_name)

        # Step 1: Delete the folder from disk
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Step 2: Delete image records
        PropertyImage.objects.filter(property=property_obj).delete()

        # Step 3: Delete the property itself
        property_obj.delete()

        messages.success(request, "Property and associated images deleted successfully.")

    return redirect('manager_properties')

@login_required
@user_passes_test(is_property_manager)
def remove_tenant(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    # Clear tenant and lease info
    unit.tenant = None
    unit.lease_start = None
    unit.lease_end = None
    unit.rent_amount = None
    unit.save()

    messages.success(request, f"Tenant removed from unit {unit.unit_number}.")
    return redirect('property_detail', pk=unit.property.id)


@login_required
@user_passes_test(is_property_manager)
def edit_tenant_assignment(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    property = unit.property

    # Prepare dropdown options (current tenant + unassigned)
    tenant_queryset = CustomUser.objects.filter(role='tenant', unit__isnull=True)
    if unit.tenant:
        tenant_queryset = CustomUser.objects.filter(pk=unit.tenant.pk) | tenant_queryset

    if request.method == 'POST':
        tenant_id = request.POST.get('tenant')
        rent_amount = request.POST.get('rent_amount')
        lease_start = request.POST.get('lease_start') or None
        lease_end = request.POST.get('lease_end') or None

        try:
            selected_tenant = CustomUser.objects.get(pk=tenant_id, role='tenant')
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid tenant selected.")
            return redirect('property_detail', pk=property.id)

        # Update unit
        unit.tenant = selected_tenant
        unit.rent_amount = rent_amount
        unit.lease_start = lease_start
        unit.lease_end = lease_end
        unit.save()

        messages.success(request, "Tenant details updated.")
        return redirect('property_detail', pk=property.id)

    return render(request, 'properties/edit_tenant_assignment.html', {
        'unit': unit,
        'property': property,
        'tenants': tenant_queryset
    })




@require_POST
@login_required
@user_passes_test(is_property_manager)
def delete_property_image(request, image_id):
    try:
        image = PropertyImage.objects.get(id=image_id)
        image.delete()
        return JsonResponse({'success': True})
    except PropertyImage.DoesNotExist:
        return JsonResponse({'success': False}, status=404)



def is_landlord(user):
    return user.is_authenticated and user.role == 'landlord'





@login_required
@user_passes_test(is_landlord)
def landlord_property_list(request):
    landlord = request.user
    properties = Property.objects.filter(landlord=landlord).prefetch_related('unit_set')
    properties_with_thumbnails = []

    for prop in properties:
        first_image = PropertyImage.objects.filter(property=prop).first()
        properties_with_thumbnails.append((prop, first_image))
    return render(request, 'properties/landlord_properties.html',
                  {'properties_with_thumbnails': properties_with_thumbnails})


@login_required
@user_passes_test(is_landlord)
def landlord_property_detail(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, landlord=request.user)
    images = PropertyImage.objects.filter(property=property_obj)
    units = property_obj.unit_set.all()

    total_units = units.count()
    occupied_units = units.exclude(tenant=None).count()
    occupancy_rate = (occupied_units / total_units) * 100 if total_units else 0
    total_rent = sum(u.rent_amount for u in units if u.rent_amount) if total_units else 0

    property_manager = property_obj.managed_by  # Can be None

    return render(request, 'properties/landlord_property_detail.html', {
        'property': property_obj,
        'units': units,
        'occupancy_rate': round(occupancy_rate, 2),
        'total_rent': round(total_rent, 2),
        'images': images,
        'property_manager': property_manager,
    })



@login_required
@user_passes_test(is_landlord)
def landlord_unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    return render(request, 'properties/landlord_unit_detail.html', {
        'unit': unit
    })