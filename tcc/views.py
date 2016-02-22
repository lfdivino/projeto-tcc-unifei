from django.shortcuts import render
from .forms import ContactForm, SignUpForm
from .models import Perguntas


def home(request):
    title = "My Title"
    form = SignUpForm()
    perguntas = Perguntas.objects.all()

    if request.method == "POST":
        print (request.POST)

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
