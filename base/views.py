# from Crypto.Cipher import AES
import random
import re
from binascii import a2b_hqx, b2a_hqx
from hashlib import md5
from urllib.parse import urlencode

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from games.models import Game

User = get_user_model()

# send payment request to 3-rd party payment service
@login_required
def pay_redirect(request, price, user_id, game_id):

    n1 = str(user_id) + 'a' + str(game_id)

    checksumstr = f"pid={n1}&sid={'bFkH0ndlYnN0ZWFtX2FkbWlu'}&amount={price}&token={'IvWlKLJBOTc3sxEG9T91385mC2IA'}"
    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
    bankapi = 'https://tilkkutakki.cs.aalto.fi/payments/pay'
    query = urlencode({
    'pid': n1, 
    'sid': 'bFkH0ndlYnN0ZWFtX2FkbWlu', 
    'amount': price,
    'checksum': checksum,
    'success_url': 'https://orange2020.herokuapp.com/pay_result/',
    'cancel_url': 'https://orange2020.herokuapp.com/pay_result/',
    'error_url': 'https://orange2020.herokuapp.com/pay_result/'})
    return redirect(bankapi + '?' + query)

# get payment result from 3-rd party payment service and handle by different result
@login_required
def pay_result(request):
    pid = request.GET.get('pid')
    ref = request.GET.get('ref')
    result = request.GET.get('result')
    checksum = request.GET.get('checksum')
    u_id = pid.split("a")[0]
    g_id = pid.split("a")[1]
    checksumstr = f"pid={pid}&ref={ref}&result={result}&token={'IvWlKLJBOTc3sxEG9T91385mC2IA'}"
    checksum1 = md5(checksumstr.encode('utf-8')).hexdigest()

    if (checksum == checksum1 and result == 'success'):
        u = User.objects.get(id=u_id)
        g = Game.objects.get(id=g_id)
        g.sales = g.sales + 1
        g.save()
        u.games.add(g)
        return redirect('home')

    elif (result == 'cancel'):
        return redirect('home')
    else:
        return redirect('pay_error')

# return to error page if happen error during payment
@login_required
def pay_error(request):
    context = {
        "all_games": Game.objects.all()
    }
    return render(request, 'error.html', context)

# goto user's playground page, return all player owned games
@login_required
def games_owned(request):
    if request.user.is_authenticated:
        context = {
            "games": Game.objects.filter(users=request.user)
        }
    else:
        context = {}
    return render(request, 'playground.html', context)

# goto developer's inventory page, return all developer uploded games
@login_required
def games_deved(request):
    if request.user.is_authenticated:
        context = {
            "games": Game.objects.filter(developer=request.user.username)
        }
    else:
        context = {}
    return render(request, 'inventory.html', context)

# goto store page, return all user NOT owned games
@login_required
def games_not_owned(request):
    if request.user.is_authenticated:
        context = {
            "games": Game.objects.all().exclude(users=request.user)
        }
    else:
        context = {}
    return render(request, 'store.html', context)

# goto search page, return search result
def games_search(request):
    keyWord = request.GET['keyWord']
    keyWord = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])"," ",keyWord)
    context = {
        "games": Game.objects.filter(Q(name__iregex=keyWord) | Q(developer__icontains=keyWord)).distinct()
    }
    return render(request, 'search.html', context)

def page_not_found(request):
    return render(request, '404.html')