from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserPageForm(forms.Form):
    """
        Форма для правки информации о пользователе в /app_users/full_size/change_about.html
    """
    f_name = forms.CharField(max_length=150,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }))
    l_name = forms.CharField(max_length=150,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }))
    about = forms.CharField(required=False, max_length=500,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'id': 'aboutTextarea',
                                'placeholder': 'label',
                                'style': 'height: 100px',
                            }))


class LoginForm(forms.Form):
    """
        Форма для входа пользователя на всех страницах, где используется /main_base.html
    """
    username = forms.CharField(min_length=2, max_length=35,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control form-control-sm',
                                   'placeholder': _('Login'),
                               }))
    password = forms.CharField(min_length=3, max_length=30,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control form-control-sm',
                                   'placeholder': _('Password'),
                               }))


class RegisterForm(UserCreationForm):
    """
        Форма для регистрации пользователя в /app_users/sign_up.html
    """
    about = forms.CharField(required=False, max_length=500,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'id': 'aboutTextarea',
                                'placeholder': 'label',
                                'style': 'height: 100px',
                            }))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs = {
            'class': 'form-control mb-2',
            'placeholder': _('Password'),
        }

        self.fields['password2'].widget.attrs = {
            'class': 'form-control mb-3',
            'placeholder': _('Repeat password'),
        }

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'about')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': _('Login'),
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('First Name'),
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': _('Last Name'),
            }),
        }
