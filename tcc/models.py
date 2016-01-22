from django.db import models


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=200, blank=False, null=False)
    aniversario = models.DateField(blank=False, null=False)
    formado = models.BooleanField(blank=False, null=False)
    matricula = models.IntegerField(blank=True, null=True)
    formatura = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.nome_completo


class Perguntas(models.Model):
    id = models.AutoField(primary_key=True)
    pergunta = models.TextField(blank=False, null=False)
    ativa = models.BooleanField()

    def __unicode__(self):
        return self.pergunta


class PerguntasRespondidasUsuarios(models.Model):
    class Meta:
        unique_together = (('id_usuario', 'id_pergunta'),)

    id_usuario = models.ForeignKey(Usuarios)
    id_pergunta = models.ForeignKey(Perguntas)


class Respostas(models.Model):
    id = models.AutoField(primary_key=True)
    id_pergunta = models.ForeignKey(Perguntas)
    resposta = models.IntegerField(blank=False, null=False)
    data_resposta = models.DateField(blank=False, null=False)

    def __unicode__(self):
        return self.resposta
