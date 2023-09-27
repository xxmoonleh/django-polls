from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
from accounts.forms import AccountSignupForm

class AccountsCreateView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('login')
    success_message = 'Registro do usuário realizado com sucesso ;)'
    #fields = ('username', 'email', 'password')
    form_class = AccountSignupForm

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        form.save()
        messages.success(self.request, self.success_message)
        return super(AccountsCreateView, self).form_valid(form)