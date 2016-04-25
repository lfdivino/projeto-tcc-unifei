import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, PerguntasSerializer, RespostasSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import *
from .models import *
from django.core.context_processors import csrf
import hashlib, datetime, random
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='/login/')
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


@staff_member_required
def analise_dados(request):
    context = {
        'title': 'Analise dos Dados'
    }

    template = 'admin/analise_dados.html'
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def respostas(request, question_id=None):
    if request.method == 'GET':
        if question_id:
            respostas = Respostas.objects.filter(id_pergunta=question_id)
            respostas = RespostasSerializer(respostas, many=True)
            return JSONResponse(respostas.data)
        else:
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


@csrf_exempt
def perguntas(request):
    if request.method == 'GET':
        perguntas = Perguntas.objects.all()
        perguntas = PerguntasSerializer(perguntas, many=True)
        return JSONResponse(perguntas.data)


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            random_string = str(random.random()).encode('utf8')

            salt = hashlib.sha1(random_string).hexdigest()[:5]

            salted = (salt + email).encode('utf8')

            activation_key = hashlib.sha1(salted).hexdigest()

            key_expires = datetime.datetime.today() + datetime.timedelta(3)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Siseel: Ativação de registro'
            email_body = "Olá %s, obrigado por se registrar. Para ativar a sua conta, clique no link a seguir em até 72 horas http://http://siseel.herokuapp.com/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'lf.divino@yahoo.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/register_success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('register.html', args, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('/')


def register_success(request):
    context = {
        'title': 'Obrigado por registrar!'
    }

    return render(request, "register_success.html", context)


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', context_instance=RequestContext(request))

