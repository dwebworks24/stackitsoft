from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import * 
from django.core.serializers import serialize
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    context ={'segment': 'index'}
    try:
        html_template = loader.get_template('home/dashboard.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))


@login_required(login_url="/login/")
def datatables(request):
    context ={'segment': 'employee'}
    try:
        html_template = loader.get_template('home/data-tables.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
@login_required(login_url="/login/")
def cluster_dashboard(request):
    context ={'segment': 'cluster'}
    try:
        logged_in_user = request.user
        context['transaction'] = PickupTransaction.objects.filter(shop_owner__user= logged_in_user).order_by('-id')
        context['blance'] = PickupTransaction.objects.filter(shop_owner__user= logged_in_user).last()

        html_template = loader.get_template('home/cluster-dashboard.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
    
@login_required(login_url="/login/")
def employee_datatables(request):
    context ={'segment': 'employee'}
    try:
        html_template = loader.get_template('home/data-tables.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
@login_required(login_url="/login/")
def shop_list(request):
    context ={'segment': 'employee'}
    try:
        context['shop'] = ShopOwner.objects.all()
        html_template = loader.get_template('shop/shop_list.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))

@login_required(login_url="/login/")    
def add_shop(request):
    context ={'segment': 'employee'}
    try:
        context['clusteraera'] = Clusteraera.objects.all()
        html_template = loader.get_template('shop/add_shop.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    

@login_required(login_url="/login/")
def transaction_list(request):
    context ={'segment': 'transaction_list'}
    try:
        context['transaction'] = PickupTransaction.objects.all().order_by('-id')
        html_template = loader.get_template('transaction/transaction_list.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))

@login_required(login_url="/login/")
def add_new_transaction_shop(request):
    context ={'segment': 'add_transaction'}
    try:
       
        context['clusteraera'] = Clusteraera.objects.all()
        context['owners'] = ShopOwner.objects.all()
        # filter(cluser_aera =cluster_area_id) if cluster_area_id else ShopOwner.objects.none()
       
        context['waste'] = WasteType.objects.all()
        context['waste_obj_json'] = serialize('json', context['waste'])
        html_template = loader.get_template('transaction/new_transaction.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))
    
    
@login_required(login_url="/login/")
def password_change(request):
    context ={'segment': 'all'}
    try:
        html_template = loader.get_template('home/password-change.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errorpages/page-404.html')
        return HttpResponse(html_template.render(request))
    except:
        html_template = loader.get_template('errorpages/page-500.html')
        return HttpResponse(html_template.render(request))