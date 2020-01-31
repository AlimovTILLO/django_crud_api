from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import Product, User
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            'Необработанные пароли не сохраняются, поэтому нет '
            'возможности увидеть пароль этого пользователя, '
            'но вы можете изменить пароль, используя '
            '<button ><a href="{}"> эту форму</a></button>.'),
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                'content_type')

    def clean_password(self):
        return self.initial["password"]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }