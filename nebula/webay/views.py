from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.views.generic import DetailView
from webay.forms import UserForm, UserProfileForm, ProfileImageForm
from .models import Bid
from .models import Item


def index(request):
    return render(request, 'webay/base.html')


def auctions(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'webay/auctions.html', context)


def bids(request):
    context = {
        'bids': Bid.objects.filter()
    }
    return render(request, 'webay/bids.html', context)


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.user:
            return True
        return False


class ItemDetailView(DetailView):
    model = Item
    template_name = 'webay/item_detail.html'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['bids'] = Bid.objects.all()
        return context


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
    print(request.user.username)
    return render(request, 'webay/profile.html')


@login_required
def logout(request):
    django_logout(request)
    return redirect('/')
