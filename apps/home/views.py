from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import * 
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.core.mail import send_mass_mail
import datetime
from django.contrib.auth import get_user_model
from .utils.email_utils import send_market_update_email
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
    # sort = request.GET.get('sort')
    # if sort in ['updated_at']:
    #     markets = MarketCoin.objects.order_by(sort)
    # else:
    #     markets = MarketCoin.objects.order_by('-updated_at')
    hours_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    markets = MarketCoin.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(markets, 5)
    markets_page = paginator.get_page(page)

    return render(request, 'dashboard.html', {
        'markets': markets_page,
        'hours_list': hours_list,
        # 'sort': sort
    })




@csrf_exempt
@login_required
def update_market(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid request'}, status=400)

    market_id = request.POST.get('id')
    name = request.POST.get('name')
    unit = request.POST.get('unit')
    prices = {f'price_{h}pm': request.POST.get(f'price_{h}pm') for h in range(2, 12)}

    try:
        market = MarketCoin.objects.get(pk=market_id)
    except MarketCoin.DoesNotExist:
        return JsonResponse({'status': 'not found'}, status=404)

    # Update market details
    market.name = name
    market.unit = unit
    for key, value in prices.items():
        setattr(market, key, value or None)
    market.save()

    # Get recipient list
    User = get_user_model()
    recipient_list = list(User.objects.filter(email__isnull=False, email__gt='').values_list('email', flat=True))
    updated_by=request.user
    # Send email
    email_success, email_message = send_market_update_email(market, prices, recipient_list,updated_by)

    return JsonResponse({
        'status': 'success',
        'email_status': 'sent' if email_success else 'failed',
        'email_message': email_message,
    })