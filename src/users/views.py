from django.shortcuts import render, redirect
from .forms import UserForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import login, logout
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = UserForm()

    context = {
        'form': form
    }

    return render(request, "users/register.html", context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("store:home")

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "p_form": p_form,
        "u_form": u_form,
    }
    return render(request, "users/profile.html", context)