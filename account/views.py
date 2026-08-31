from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout

import http.client
import json
import logging
import random
import sys

from . import models

logger = logging.getLogger('django')


def get_sms_token():
    conn = http.client.HTTPSConnection("restfulsms.com")

    payload = "{\r\n\t\"UserApiKey\":\"******\",\r\n\t\"SecretKey\":\"*******#\"\r\n}\r\n"

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "54b79b6e-85a7-0794-7b73-69ea5fb8cd7c"
        }

    conn.request("POST", "/api/Token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return (json.loads(data.decode("utf-8"))['TokenKey'])






def login1_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        rcode = random.randint(1111, 9999)

        user = models.UserProfile.objects.filter(username=username)

        if not user:
            user = models.UserProfile(username=username)
        else:
            user = user[0]
        
        user.rcode = str(rcode)
        user.save()

        otp_line = f'OTP code for {user.username}: {rcode}'
        print(otp_line, flush=True)
        sys.stderr.write(otp_line + '\n')
        sys.stderr.flush()
        logger.warning(otp_line)

        return HttpResponseRedirect(reverse('account:validate') + "?username={}".format(user.username))


    return render(request, 'login1.html')



def login2_view(request):

    error = ''

    if request.method == 'POST':
        username =  request.POST.get('username')
        rcode =  request.POST.get('rcode')

        user = models.UserProfile.objects.filter(username=username, rcode=rcode)
        if user:
            user = user[0]
            if user.register_complete:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(reverse('account:register') + "?username={}".format(user.username))
        else:
            error = 'کد تایید صحیح نمی‌باشد'




    username = request.GET.get('username')
    debug_otp = ''
    if settings.DEBUG and username:
        existing = models.UserProfile.objects.filter(username=username).first()
        if existing and existing.rcode:
            debug_otp = existing.rcode

    context = {
        'username': username,
        'error': error,
        'debug_otp': debug_otp,
    }
    return render(request, 'login2.html', context)



def login3_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print('1', first_name, username)

        user = models.UserProfile.objects.filter(username=username)

        if not user:
            return HttpResponseRedirect('/')

        user = user[0]
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.register_complete = True
        user.save()
        login(request, user)
        return HttpResponseRedirect('/')


    username = request.GET.get('username')

    context = {
        'username': username,
    }

    return render(request, 'login3.html', context)







def logout_view(request):
    logout(request)
    return redirect('main:index')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('account:account')

    if request.method == 'POST':
        user = request.user
        user.first_name = (request.POST.get('first_name') or '').strip()
        user.last_name = (request.POST.get('last_name') or '').strip()
        user.email = (request.POST.get('email') or '').strip() or None
        user.username_public = bool(request.POST.get('username_public'))
        user.email_public = bool(request.POST.get('email_public'))
        user.image_public = bool(request.POST.get('image_public'))
        if request.FILES.get('image'):
            user.image = request.FILES['image']
        user.save()
        messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد.')

    return redirect('/?tab=profile')