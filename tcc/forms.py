from django import forms
from .models import Perguntas, Respostas, PerguntasRespondidasUsuarios
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        if not extension == "edu":
            raise forms.ValidationError("Please use a valid .EDU email address")
        return email


class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Perguntas
        fields = ['pergunta', 'ativa']


class CustomUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()


class RespostaForm(forms.ModelForm):
    class Meta:
        model = Respostas
        fields = ['id_pergunta', 'resposta', 'data_resposta']


class PerguntasRespondidasUsuariosForm(forms.ModelForm):
    class Meta:
        model = PerguntasRespondidasUsuarios
        fields = ['id_usuario', 'id_pergunta']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ja utilizado!')

    #modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()


        return user