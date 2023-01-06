from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from random import randint
from django.utils import timezone

import boto3
from botocore.exceptions import ClientError

from urllib.parse import unquote

import datetime
import requests
import http.client
import json
import random

import mimetypes
import os
from django.http.response import HttpResponse

from . import models


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
        
        user.rcode = rcode
        user.save()


        print(rcode)

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

    context = {
        'username': username,
        'error': error
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