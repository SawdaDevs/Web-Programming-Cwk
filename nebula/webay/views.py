from django.contrib.auth import logout as django_logout
from django.http import HttpResponse, JsonResponse, QueryDict
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from webay.forms import UserForm, UserProfileForm, ProfileImageForm
from django.views.decorators.csrf import csrf_exempt
from .models import Bid, Item

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

def item_view(request,item_id):
    auc_item = Item.objects.get(id=item_id)
    if Bid.objects.filter(item = item_id).exists():
        bids = Bid.objects.filter(item = item_id)
        highest_amount = Bid.objects.filter(item = item_id).order_by('amount')[0].amount
    else:
        highest_amount = auc_item.base_price
        bids = {}


    context = {
        'items': Item.objects.all(),
        'bids' : bids,
        'highest_bid': highest_amount,
        'auction_item' : auc_item
    } 
    return render(request, 'webay/item_detail.html',context)   

def deleteItem(request):
        id = int(QueryDict(request.body).get('id'))
        item_del = Item.objects.get(id=id)
        item_del.delete()
        response = JsonResponse({
            'result': 'success'
        })
        response.status_code = 200
        return response

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
