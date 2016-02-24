from django.contrib import admin
from .models import Usuarios, Perguntas, PerguntasRespondidasUsuarios, Respostas
from .forms import SignUpForm, PerguntaForm, RespostaForm


class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp", "updated"]
    form = SignUpForm
    # class Meta:
    #     model = SignUp


class PerguntaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "ativa"]
    form = PerguntaForm
    # class Meta:
    #     model = Perguntas


class RespostaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id_pergunta", "data_resposta"]
    form = RespostaForm


admin.site.register(Perguntas, PerguntaAdmin)
admin.site.register(Respostas, RespostaAdmin)
