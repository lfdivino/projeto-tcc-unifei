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

    if request.method == "POST":
        print(request.POST)
        resposta_pergunta = request.POST
        pergunta = Perguntas.objects.get(pk=resposta_pergunta["pergunta_id"])
        respostas = Respostas(
            id_pergunta=pergunta,
            resposta=resposta_pergunta["resposta"],
            data_resposta=datetime.date.today()
        )
        respostas.save()
        pergunta_resposta_user = PerguntasRespondidasUsuarios(
            id_usuario = request.user,
            id_pergunta = pergunta
        )
        pergunta_resposta_user.save()

    context = {
        'perguntas': perguntas,
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
def respostateste(request):

    if request.method == 'GET':
        snippets = Respostas.objects.all()
        serializer = RespostasSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        resposta = RespostasSerializer(data=data)
        if resposta.is_valid():
            resposta.save()
            return JSONResponse(resposta.data, status=201)
        return JSONResponse(resposta.errors, status=400)


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

