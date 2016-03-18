from django.contrib.auth.models import User, Group
from .models import Perguntas, Respostas
from rest_framework import serializers


class RespostasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respostas
        fields = ('id_pergunta', 'resposta', 'data_resposta')


class PerguntasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Perguntas
        fields = ('id', 'pergunta', 'ativa')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
