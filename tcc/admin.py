from django.contrib import admin
from .models import Usuarios, Perguntas, PerguntasRespondidasUsuarios, Respostas
from .forms import PerguntaForm, RespostaForm, PerguntasRespondidasUsuariosForm


class PerguntaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "ativa"]
    form = PerguntaForm
    # class Meta:
    #     model = Perguntas


class RespostaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id_pergunta", "data_resposta"]
    form = RespostaForm


class PerguntasRespostasUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'id_pergunta']
    form = PerguntasRespondidasUsuariosForm


admin.site.register(Perguntas, PerguntaAdmin)
admin.site.register(Respostas, RespostaAdmin)
admin.site.register(PerguntasRespondidasUsuarios, PerguntasRespostasUsuarioAdmin)
