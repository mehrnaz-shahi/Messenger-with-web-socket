from django.shortcuts import render, redirect, HttpResponse

from . import models
from account import models as account


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('account:account')

    pvs = models.PV.objects.filter(user1=request.user) | models.PV.objects.filter(user2=request.user)

    group_members = models.GroupMember.objects.filter(user=request.user, is_member=True)
    groups = []

    for gm in group_members:
        groups.append(gm.group)
    context = {
        'pvs': pvs,
        'groups': groups
    }
    return render(request, 'main.html', context)


def start_pv_view(request, username):
    if not request.user.is_authenticated:
        redirect('account:account')

    user = account.UserProfile.objects.filter(username=username)

    if not user:
        return HttpResponse("User not found! <br> <a href=\'/\'>Return Home</a>")
    user = user[0]
    pv = models.PV.objects.filter(user1=request.user, user2=user) | models.PV.objects.filter(user2=request.user, user1=user)
    if pv:
        return redirect('chat:pv', pv_id=pv[0].id)
    
    pv = models.PV(user1 = request.user, user2=user)
    pv.save()
    return redirect('chat:pv', pv_id=pv.id)


def start_group_view(request):
    if not request.user.is_authenticated:
        redirect('account:account')
    
    name = request.POST.get('name')
    desc = request.POST.get('desc')
    t = request.POST.get('type')

    group = models.Group(owner=request.user, name=name, desc=desc, type=t)
    group.save()

    member = models.GroupMember(user=request.user, is_admin=True, is_member=True, group=group)
    member.save()

    # return redirect('chat:pv', pv_id=pv.id)