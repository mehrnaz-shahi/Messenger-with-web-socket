from django.shortcuts import render

from main import models as main


def pv_view(request, pv_id):

    pv = main.PV.objects.filter(id=pv_id)
    if pv:
        pv = pv[0]

        if not(request.user == pv.user1 or request.user == pv.user2):
            return render(request, 'error.html', context)

        if request.user == pv.user1:
            contact = pv.user2.get_full_name()
        else:
            contact = pv.user1.get_full_name()

        context = {
            'pv': pv,
            'contact': contact 
        }
        return render(request, 'pv.html', context)