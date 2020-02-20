from django.urls import path
from users import views
from django.conf.urls import url, include, re_path


urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('all/', views.UserList.as_view()),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
