from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import MemberProfile

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='Utilizador', max_length=150)
    password = forms.CharField(label='Palavra-passe', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Utilizador ou palavra-passe invalidos.')
            cleaned_data['user'] = user

        return cleaned_data


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150)
    last_name = forms.CharField(label='Apelido', max_length=150, required=False)
    username = forms.CharField(label='Nome de utilizador', max_length=150)
    email = forms.EmailField(label='Email')
    member_number = forms.CharField(label='Numero de associado', max_length=30)
    phone = forms.CharField(label='Telefone', max_length=20, required=False)
    identity_card = forms.CharField(label='BI', max_length=30, required=False)
    password1 = forms.CharField(label='Palavra-passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar palavra-passe', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de utilizador ja esta em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ja esta registado.')
        return email

    def clean_member_number(self):
        member_number = self.cleaned_data['member_number']
        if MemberProfile.objects.filter(member_number=member_number).exists():
            raise forms.ValidationError('Este numero de associado ja existe.')
        return member_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As palavras-passe nao coincidem.')

        if password1:
            validate_password(password1)

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        MemberProfile.objects.create(
            user=user,
            member_number=self.cleaned_data['member_number'],
            phone=self.cleaned_data['phone'],
            identity_card=self.cleaned_data['identity_card'],
            role=MemberProfile.Role.MEMBER,
        )
        return user
