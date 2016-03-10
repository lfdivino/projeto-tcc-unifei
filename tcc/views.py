import datetime
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, GroupSerializer, PerguntasSerializer, RespostasSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ContactForm
from .models import Perguntas, Respostas, PerguntasRespondidasUsuarios


@login_required
def home(request):
    perguntas = Perguntas.objects.all().exclude(
            id__in=PerguntasRespondidasUsuarios.objects.values_list('id_pergunta', flat=True).filter(
                    id_usuario=request.user
            )
    ).filter(ativa=True)
    if perguntas:
        primeira_pergunta = perguntas[0].id

        context = {
            'perguntas': perguntas,
            'primeira_pergunta': primeira_pergunta,
        }
    else:
        context = {
            'perguntas': perguntas
        }

    return render(request, "home.html", context)


def contact(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        full_name = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        message = form.cleaned_data.get("message")
        print (full_name, email, message)

    context = {
        "title": "Formularios",
        "form": form,
    }

    return render(request, "forms.html", context)


def about(request):
    context = {

    }
    return render(request, "about.html", context)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def resposta(request):
    if request.method == 'GET':
        respostas = Respostas.objects.all()
        respostas = RespostasSerializer(respostas, many=True)
        return JSONResponse(respostas.data)

    elif request.method == 'POST':
        json_resposta = JSONParser().parse(request)
        resposta = json_resposta
        login = json_resposta['login']
        password = json_resposta['password']
        del resposta['login']
        del resposta['password']
        usuario = User.objects.get(username=login, password=password)
        if usuario:
            pergunta = Perguntas.objects.get(pk=int(resposta['id_pergunta']))
            if PerguntasRespondidasUsuarios.objects.filter(id_pergunta=pergunta.id).filter(id_usuario=usuario.id):
                data = {
                    'resposta': "Pergunta ja respondida pelo usuario"
                }
                return JSONResponse(data)
            else:
                if resposta:
                    resposta_obj = Respostas.objects.create(id_pergunta=pergunta, resposta=resposta['resposta'])
                    resposta_obj.save()
                    pergunta_respondida_usuario_obj = PerguntasRespondidasUsuarios.objects.create(
                            id_usuario=usuario,
                            id_pergunta=pergunta
                    )
                    pergunta_respondida_usuario_obj.save()
                    data = {
                        'resposta': True
                    }
                    return JSONResponse(data)
                data = {
                    'resposta': "Ocorreu um erro ao salvar a resposta, tente novamente"
                }
                return JSONResponse(data)
        else:
            data = {
                'resposta': "Ocorreu um erro ao salvar a resposta, tente novamente"
            }
            return JSONResponse(data)


class PerguntaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Perguntas.objects.all()
    serializer_class = PerguntasSerializer


# class RespostaViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Respostas.objects.all()
#     serializer_class = RespostasSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
