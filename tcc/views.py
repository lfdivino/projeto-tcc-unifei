import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ContactForm, SignUpForm
from .models import Perguntas, Respostas, PerguntasRespondidasUsuarios


@login_required
def home(request):
    title = "My Title"
    form = SignUpForm()
    perguntas = Perguntas.objects.all().exclude(id__in=PerguntasRespondidasUsuarios.objects.values_list('id_pergunta', flat=True).filter(id_usuario=request.user))
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

    context = {
        'template_title': title,
        'form': form,
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