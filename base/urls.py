from django.conf.urls import include, re_path
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #path('', views.home, name="home"),
    path('pay_error', views.pay_error, name="pay_error"),
    path('pay/<int:price>/<int:user_id>/<int:game_id>', views.pay_redirect, name="pay_redirect"),
    re_path(r'^pay_result/$', views.pay_result, name = 'pay_result'),
    path('playground', views.games_owned, name="playground"),
    path('inventory', views.games_deved, name="inventory"),
    path('store', views.games_not_owned, name="store"),
    path('search', views.games_search, name="search"),
    path('not_found', views.page_not_found, name="404"),
]
