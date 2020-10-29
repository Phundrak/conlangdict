from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # Account creation
    # /signup
    path('signup/', views.signup, name="signup")
]

urlpatterns += staticfiles_urlpatterns()
