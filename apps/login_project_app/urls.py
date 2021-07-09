from django.urls import path
from . import views

urlpatterns = [
    path('register', views.nuevo),
    path('login', views.login),
    path('success', views.success),
    path('login', views.login),
    path('logout/', views.logout),
]
