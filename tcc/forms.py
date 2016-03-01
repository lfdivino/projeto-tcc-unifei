from django import forms
from .models import Perguntas, Respostas, PerguntasRespondidasUsuarios


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
