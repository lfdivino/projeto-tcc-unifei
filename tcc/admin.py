from django.contrib import admin
from .models import Usuarios, Perguntas, PerguntasRespondidasUsuarios, Respostas
from .forms import SignUpForm, PerguntaForm

class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "timestamp", "updated"]
    form = SignUpForm
    # class Meta:
    #     model = SignUp

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "pergunta", "ativa"]
    form = PerguntaForm
    # class Meta:
    #     model = Perguntas

admin.site.register([Usuarios, Perguntas, PerguntasRespondidasUsuarios, Respostas])
