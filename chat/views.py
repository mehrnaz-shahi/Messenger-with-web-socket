from django.shortcuts import render, redirect

from main import models as main


def pv_view(request, pv_id):
    if not request.user.is_authenticated:
        return redirect('account:account')

    pv = main.PV.objects.filter(id=pv_id)
    if not pv:
        return redirect('main:index')

    pv = pv[0]

    if not (request.user == pv.user1 or request.user == pv.user2):
        return redirect('main:index')

    contact_user = pv.other_user(request.user)

    context = {
        'pv': pv,
        'contact': contact_user.get_full_name(),
        'contact_user': contact_user,
    }
    return render(request, 'pv.html', context)