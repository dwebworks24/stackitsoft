from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import * 
from django.core.serializers import serialize
# Create your views here.


def index(request):
    context ={'segment': 'index'}
    try:
        html_template = loader.get_template('index.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))

def about_us(request):
    context ={'segment': 'about us'}
    try:
        html_template = loader.get_template('about.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
def contact_us(request):
    context ={'segment': 'contact us'}
    try:
        html_template = loader.get_template('contact.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
def buy_crypto_select(request):
    context ={'segment': 'contact us'}
    try:
        html_template = loader.get_template('commingsoon.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
def buy_crypto_confirm(request):
    context ={'segment': 'contact us'}
    try:
        html_template = loader.get_template('commingsoon.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))

def buy_crypto_details(request):
    context ={'segment': 'contact us'}
    try:
        html_template = loader.get_template('commingsoon.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))    



def user_login(request):
    context ={'segment': 'Login'}
    try:
        html_template = loader.get_template('login.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))          


def forgot_password(request):
    context ={'segment': 'forgot_password'}
    try:
        html_template = loader.get_template('forgotpassword.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))  
    

def dashboard(request):
    context ={'segment': 'dashboard'}
    try:
        html_template = loader.get_template('dashboard.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))  