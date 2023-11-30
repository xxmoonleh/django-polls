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

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = ('first_name', 'email', 'imagem', )
    success_url = reverse_lazy('login')
    success_message = 'Perfil atualizado com sucesso!'

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = self.request.user
        if user is None or not user.is_authenticated or user_id != user.id:
            return User.objects.none()
        return User.objects.filter(id=user.id)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(AccountUpdateView, self).form_valid(form)

from django.views.generic import TemplateView
from polls.models import QuestionUser

class AccountTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super(AccountTemplateView, self).get_context_data(**kwargs)
        voted = QuestionUser.objects.filter(user=self.request.user)
        context['questions_voted'] = voted
 
        return context

    

