from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.template import loader
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



@csrf_exempt
def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        # Validate fields
        if not email or not employee_id or not password:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        try:
            user = Users.objects.get(email=email, employee_id=employee_id)
        except Users.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Employee ID or Email.'})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful.', 'redirect_url': '/dashboard/'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid password.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})          


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