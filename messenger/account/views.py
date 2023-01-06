from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from random import randint
from . import models
from django.utils import timezone

from urllib.parse import unquote

import datetime
import requests
import http.client
import json
from random import randint

import mimetypes
import os
from django.http.response import HttpResponse


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



def logout_view(request):
    logout(request)
    return redirect('main:index')


def account_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
      
        user = models.UserProfile.objects.filter(username = username)
        if user.count() and user[0].phone_valid:
            user = user[0]
            user.first_name = first_name
            user.last_name = last_name
            user.register_complete = True

            user.save()
            login(request, user)
            return HttpResponse("login")


    return render(request, 'account.html')

def ajax_val_phone(request):
    username = request.GET.get('username', None)
    users = models.UserProfile.objects.filter(username = username)
    if users.count() and users[0].register_complete:
            user = users[0]
            user.r_code_time = timezone.now()
            user.r_code = randint(1111, 9999)
            user.save()
            conn = http.client.HTTPSConnection("restfulsms.com")

            payload = {
                    'ParameterArray': [
                        { "Parameter": "VerificationCode","ParameterValue": str(user.r_code)},
                        ],

                    "Mobile": user.username,
                    "TemplateId": "71242",
                }
            payload = json.dumps(payload)


            headers = {
                'x-sms-ir-secure-token': get_sms_token(),
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "48885b70-56a0-a612-3b1d-ed05385e3f05"
                }

            conn.request("POST", "/api/UltraFastSend", payload, headers)

            res = conn.getresponse()
            data = res.read()
            # print(user.r_code)

            return JsonResponse({'regsiter':False, 'username':username})
    else:
        if users.count():
            user = users[0]
        else:
            user = models.UserProfile(username = username)
            
        user.r_code_time = timezone.now()
        user.r_code = randint(1111, 9999)
        user.save()
        conn = http.client.HTTPSConnection("restfulsms.com")

        payload = {
                    'ParameterArray': [
                        { "Parameter": "VerificationCode","ParameterValue": str(user.r_code)},
                        ],

                    "Mobile": user.username,
                    "TemplateId": "71242",
                }
        payload = json.dumps(payload)

        headers = {
                'x-sms-ir-secure-token': get_sms_token(),
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "48885b70-56a0-a612-3b1d-ed05385e3f05"
                }

        conn.request("POST", "/api/UltraFastSend", payload, headers)

        res = conn.getresponse()
        data = res.read()
        # print(user.r_code)

        return JsonResponse({'regsiter':True, 'username':username})




def ajax_val_rcode(request):
    username = request.GET.get('username', None)
    rcode = request.GET.get('rcode', None)
    user = models.UserProfile.objects.filter(username = username)

    if user.count():
        user = user[0]
        if int(rcode) == user.r_code:
            user.phone_valid = True
            user.save()
            
            register = True
            if user.register_complete:
                login(request, user)
                register = False

            return JsonResponse({'valid':True, 'register': register})

    return JsonResponse({'valid':False})



