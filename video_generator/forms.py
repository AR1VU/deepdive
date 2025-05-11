from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=False, label='Full Name')

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name', '') or ''
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class CustomPasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''