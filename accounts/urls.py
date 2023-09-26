from django.urls import path

from accounts import views

urlpatterns = [
    path('accounts/singup', views.AccountsCreateView.as_view(), name="signup")
]
