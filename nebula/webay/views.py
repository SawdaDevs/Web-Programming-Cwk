from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from webay.forms import UserForm, UserProfileForm, ProfileImageForm, ItemForm, ItemImageForm
from webay.models import UserProfile, Notification

from .models import Bid, Item


def index(request):
    return render(request, 'webay/base.html')


def not_logged_in(user):
    return not user.is_authenticated


def auctions(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'webay/auctions.html', context)

def item_view(request, item_id):
    auc_item = Item.objects.get(id=item_id)
    if Bid.objects.filter(item=item_id).exists():
        bids = Bid.objects.filter(item=item_id)
        highest_amount = Bid.objects.filter(item=item_id).order_by('amount')[0].amount
    else:
        highest_amount = auc_item.base_price
        bids = {}

    context = {
        'items': Item.objects.all(),
        'bids': bids,
        'highest_bid': highest_amount,
        'auction_item': auc_item
    }
    return render(request, 'webay/item_detail.html', context)


def deleteItem(request):
    id = int(QueryDict(request.body).get('id'))
    item_del = Item.objects.get(id=id)
    item_del.delete()
    response = JsonResponse({
        'result': 'success'
    })
    response.status_code = 200
    return response


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
    return render(request, 'webay/profile_form.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                      'image_form': image_form,
                  })
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


def get_user_details(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)
        return JsonResponse({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'dob': profile.dob,
            'address': profile.address,
            'mobile': profile.mobile,
        })


def update_profile_pic(request):
    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        profile = UserProfile.objects.get(user=request.user)
        profile.profile_pic = image_file
        profile.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


def update_profile_details(request):
    if request.method == 'PUT':
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=request.user)
        data = QueryDict(request.body)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        profile.dob = data['dob']
        profile.address = data['address']
        profile.mobile = data['mobile']
        user.save()
        profile.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


def get_notifications(request):
    return JsonResponse(dict(notifications=list(
        Notification.objects.filter(recipient_id=request.user.id).values('id', 'read_message', 'item_id'))))


def get_notifications_message(request, id):
    notification = Notification.objects.filter(id=id).get();
    return HttpResponse(notification.message, content_type="text/html")


def get_number_unread_notifs(request):
    notification = Notification.objects.filter(recipient_id=request.user.id, read_message=0).count()
    return HttpResponse(notification)


def mark_notification_as_read(request, id):
    notification = Notification.objects.get(id=id)
    print(notification)
    notification.read_message = 1
    notification.save()
    return HttpResponse(status=200)


def display_notifications(request):
    return render(request, "webay/notifications.html")


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        print(search)
        # items = items.objects.filter(name__contains=search)

        return redirect('webay:index')
    else:
        raise Http404('search not found')


@login_required
def logout(request):
    django_logout(request)
    return redirect('/')
