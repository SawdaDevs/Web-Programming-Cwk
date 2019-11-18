from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from webay.forms import UserForm, UserProfileForm, ProfileImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'webay/base.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        image_form = ProfileImageForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        image_form = ProfileImageForm()
    return render(request, 'webay/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'image_form': image_form,
                   'registered': registered
                   })


def profile(request):
    print(request.user.username)
    return render(request, 'webay/profile.html')


@login_required
def logout(request):
    django_logout(request)
    return redirect('/')
