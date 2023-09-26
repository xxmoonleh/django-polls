from django import forms

# Import o model "User" padrão pára usuários
from django.contrib.auth import get_user_model
User = get_user_model()

# Criar forms django personalizado
class AccountsSignupForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        max_length=50,
        widget=forms.widgets.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')