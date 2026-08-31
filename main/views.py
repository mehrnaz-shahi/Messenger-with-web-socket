from django.contrib import messages
from django.shortcuts import render, redirect

from . import models
from account import models as account


def _ensure_contacts_from_pvs(user, pvs):
    for pv in pvs:
        models.add_contact(user, pv.other_user(user))


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('account:account')

    pvs = (
        models.PV.objects.filter(user1=request.user) | models.PV.objects.filter(user2=request.user)
    ).select_related('user1', 'user2').prefetch_related('messages')

    _ensure_contacts_from_pvs(request.user, pvs)

    chat_items = []
    for pv in pvs:
        chat_items.append({
            'pv': pv,
            'other': pv.other_user(request.user),
            'last': pv.last_visible_message(),
        })

    group_members = models.GroupMember.objects.filter(user=request.user, is_member=True).select_related('group')
    groups = [gm.group for gm in group_members]
    contacts = models.Contact.objects.filter(owner=request.user).select_related('person').order_by('-created')

    context = {
        'chat_items': chat_items,
        'pvs': pvs,
        'groups': groups,
        'contacts': contacts,
        'active_tab': request.GET.get('tab', 'chat'),
    }
    return render(request, 'main.html', context)


def start_pv_view(request, username):
    if not request.user.is_authenticated:
        return redirect('account:account')

    username = (username or '').strip()
    if not username:
        messages.error(request, 'شماره تماس را وارد کنید.')
        return redirect('main:index')

    if username == request.user.username:
        messages.error(request, 'نمی‌توانید با خودتان گفتگو شروع کنید.')
        return redirect('main:index')

    user, _ = account.UserProfile.objects.get_or_create(username=username)
    models.add_contact(request.user, user)

    pv = (
        models.PV.objects.filter(user1=request.user, user2=user)
        | models.PV.objects.filter(user2=request.user, user1=user)
    )
    if pv.exists():
        return redirect('chat:pv', pv_id=pv.first().id)

    pv = models.PV.objects.create(user1=request.user, user2=user)
    return redirect('chat:pv', pv_id=pv.id)


def add_contact_view(request):
    if not request.user.is_authenticated:
        return redirect('account:account')

    if request.method != 'POST':
        return redirect('/?tab=contacts')

    username = (request.POST.get('username') or '').strip()
    if not username:
        messages.error(request, 'شماره تماس را وارد کنید.')
        return redirect('/?tab=contacts')

    if username == request.user.username:
        messages.error(request, 'نمی‌توانید خودتان را به مخاطبین اضافه کنید.')
        return redirect('/?tab=contacts')

    person, _ = account.UserProfile.objects.get_or_create(username=username)
    models.add_contact(request.user, person)
    messages.success(request, 'مخاطب اضافه شد.')
    return redirect('/?tab=contacts')


def start_group_view(request):
    if not request.user.is_authenticated:
        return redirect('account:account')

    if request.method != 'POST':
        return redirect('main:index')

    name = (request.POST.get('name') or '').strip()
    desc = (request.POST.get('desc') or '').strip()
    t = request.POST.get('type') or '1'

    if not name:
        messages.error(request, 'نام گروه یا کانال را وارد کنید.')
        return redirect('main:index')

    group = models.Group.objects.create(owner=request.user, name=name, desc=desc, type=t)
    models.GroupMember.objects.create(user=request.user, is_admin=True, is_member=True, group=group)
    return redirect('group:group', group_id=group.id)