# from django.shortcuts import render
import random
from binascii import a2b_hqx, b2a_hqx
from hashlib import md5
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
# Create your views here.
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.edit import CreateView
from rest_framework import generics

from games.models import Game

from .forms import SignupForm
from .models import CustomUser
from .serializers import CustomUserSerializer
from .tokens import account_activation_token
from django.http import Http404
User = get_user_model()

#@login_required
class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# sign up
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Orange account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'registration/acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# activate user
def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.set_password(user.password)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        return render(request, 'registration/acc_active_invalid.html')

@login_required
def addGame(request, game_name, user_name):
	try:
		game = Game.objects.get(name = game_name)
	except Game.DoesNotExist:
		raise Http404("Not implemented")
	try:
		user = User.objects.get(name = user_name)
	except User.DoesNotExist:
		raise Http404("Not implemented")
	user.games.add(game);
	return render(request, 'playground.html')