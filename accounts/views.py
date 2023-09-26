from django.shortcuts import render

# Create your views here.
from django.views.generic import CreatView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
from accounts.forms import AccountsSignupForm

class AccountsCreateView(CreatView):
    model = User
    template_name = 'registration/singup_form.html'
    success_url = reverse_lazy('login')
    success_message = 'Usuário registrado com sucesso!'
    form_class = AccountsSignupForm

def form_valid(self, form):
    form.instancw.password(form.instance.password)
    form.save()
    messages.success(self.request, self.success_message)
    return super(AccountsCreateView, self).form_valid(form)
