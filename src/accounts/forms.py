from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.handlers.modwsgi import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            queryset = User.objects.filter(email=email)

            if not queryset.exists():
                raise forms.ValidationError('Такого пользователя нет!')

            if not check_password(password, queryset[0].password):
                raise forms.ValidationError('Пароль не верный!')

            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен.')
        return super(UserLoginForm, self).clean(*args, **kwargs)
