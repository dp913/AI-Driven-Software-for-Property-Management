from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser

# Create your views here.

@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'tenant':
        return redirect('tenant-dashboard')
    elif role == 'landlord':
        return redirect('landlord-dashboard')
    elif role == 'manager':
        return redirect('manager-dashboard')
    return redirect('login')  # fallback

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_user')
    else:
        form = CustomUserCreationForm()

    users = CustomUser.objects.filter(is_superuser=False).exclude(role='manager')  # Only show Tenants & Landlords
    return render(request, 'registration/register_user.html', {'form': form, 'users': users})


def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if user.is_superuser or user.role == 'manager':
        return redirect('register_user')

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('register_user')
    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, 'registration/edit_user.html', {'form': form, 'user_id': user.id})


def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if not user.is_superuser and user.role != 'manager':
        user.delete()
    return redirect('register_user')
