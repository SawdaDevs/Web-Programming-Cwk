from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from webay.forms import UserForm, UserProfileForm, ProfileImageForm, ItemForm, ItemImageForm
from webay.models import UserProfile



# Create your views here.

def not_logged_in(user):
    return not user.is_authenticated


def index(request):
    return render(request, 'webay/base.html')


@user_passes_test(not_logged_in, login_url='/profile')
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


@login_required
def profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']

        profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.mobile = mobile
        profile.address = address

        user.save()
        profile.save()

        return redirect('webay:profile')


    else:
        profile = UserProfile.objects.get(user=request.user)
    return render(request, 'webay/profile_form.html', {'profile': profile})


@login_required
def add_item(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        item_form = ItemForm(data=request.POST)
        item_image_form = ItemImageForm(data=request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.user = user
            item.start_datetime = timezone.now()
            if 'item_pic' in request.FILES:
                item.item_pic = request.FILES['item_pic']
            item.save()
            return redirect('webay:profile')  # Modify redirect so it goes to my items once you've finished that section

        else:
            print(item_form.errors, item_image_form.errors)
    else:
        item_form = ItemForm(initial={'user': user.pk})
        item_image_form = ItemImageForm()
    return render(request, 'webay/additem.html',
                  {
                      'itemForm': item_form,
                      'itemImageForm': item_image_form,
                  })


@login_required
def upload_image(request):
    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        profile = UserProfile.objects.get(user=request.user)

        if profile:
            # if user doesn't have a profile yet
            # need to create a profile first
            profile.profile_pic = image_file
            profile.save()
        return HttpResponse(profile.profile_pic.url)
    else:
        raise Http404('Image file not received')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        print(search)
        #items = items.objects.filter(name__contains=search)

        return redirect('webay:index')
    else:
        raise Http404('search not found')

@login_required
def logout(request):
    django_logout(request)
    return redirect('/')
