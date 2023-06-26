from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields  the user,
    but replaces the password field with admin disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(help_text='you can change password with <a href=\"../password/\">this form</a>')

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'last_login']


class UserRegisterForm(forms.Form):
    full_name = forms.CharField(
        label=False,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Full Name',
        })
    )
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput({
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    phone_number = forms.CharField(
        max_length=11,
        label=False,
        widget=forms.NumberInput({
            'class': 'form-control',
            'placeholder': 'Phone Number',
        })
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists!')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This phone number already exists!')
        return phone_number
