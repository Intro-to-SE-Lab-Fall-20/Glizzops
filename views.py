from django.shortcuts import render, redirect
from .models import Tutorial, TimestampMixin, Inbox, Message
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, ComposeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='Glizzymail/home.html',
                  context = {"tutorials":Tutorial.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("Glizzymail:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "Glizzymail/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "Glizzymail/register.html",
                  context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("Glizzymail:homepage")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "Glizzymail/login.html",
                    context={"form":form})

def compose(request):
    if request.method == 'GET':
        form = ComposeForm()
    else:
        form = ComposeForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email_address = form.cleaned_data['email_address']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email_address, ['glizzymailtest@gmail.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("Glizzymail:homepage")

    form = ComposeForm()
    return render(request, "Glizzymail/compose.html", {'form':form})

def homepage(request):
    return render(request = request,
                  template_name='Glizzymail/home.html',
                  context = {"tutorials":Tutorial.objects.all})

def Inbox(request):
    return render(request = request,
                  template_name='Glizzymail/inbox.html',
                  context = {"messages":Message.objects.all})