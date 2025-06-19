from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime,timezone
from .models import *
from .utilis import *
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from decimal import Decimal
@csrf_exempt
@login_required
def shop_owner_save_logic(request):
    if request.method == 'POST':
        try:
            # Extract form data
            clusteraera = request.POST['clusteraera']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            shop_name = request.POST['shop_name']
            shop_type = request.POST['shopType']
            rcb_agreement = request.POST['rcbAgreement']
            area = request.POST['area']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']

            cluster  = Clusteraera.objects.filter(id= clusteraera).first()
            if len(first_name) < 2:
                return JsonResponse({'error': 'First name must be at least 2 characters long.'}, status=400)
            if len(phone) < 10:
                return JsonResponse({'error': 'Please enter a valid phone number.'}, status=400)
        
            user = Users()
            user.first_name = first_name
            user.last_name = last_name
            user.username = f'{first_name}{last_name}'
            user.phone = phone
            user.email = email
            user.pincode = zip_code
            user.role = 'cluster'
            user.otp = 1234
            user.created_at = datetime.now()
            user.updated_at = datetime.now()
            user.save()

            shop_owner = ShopOwner()
            shop_owner.shopowner_number = generate_shop_number()
            shop_owner.user = user
            shop_owner.cluser_aera=cluster
            shop_owner.shop_name=shop_name
            shop_owner.shop_type =shop_type
            shop_owner.rcb_agreement=bool(rcb_agreement)
            shop_owner.area=area
            shop_owner.city=city
            shop_owner.state=state
            shop_owner.created_at = datetime.now()
            shop_owner.updated_at = datetime.now()
            shop_owner.created_by = request.user
            shop_owner.save()

            return JsonResponse({'message': 'shop created successfully!','path': '/add_transaction/'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    



@csrf_exempt
@login_required
def save_new_transaction_data(request):
    if request.method == 'POST':
        try:
            cluster_aera_id = request.POST.get('cluster_aera')
            owner_id = request.POST.get('owner')
            paid_amount = request.POST.get('paid_amount')
            given_bags = request.POST.get('given_bags') == 'yes'
            lifted_status = request.POST.get('lifted_status') == 'yes'
        
       
            shop_owner = ShopOwner.objects.filter(id=owner_id).first()
            cluster_aera = Clusteraera.objects.filter(id=cluster_aera_id).first()
            if not paid_amount:
                paid_amount = 0.0
            else:
                paid_amount = float(paid_amount)
            
    
            pickup_transaction = PickupTransaction.objects.create(
                shop_owner=shop_owner,
                cluser_aera = cluster_aera,
                paid_amount= float(paid_amount),
                given_bags=given_bags,
                lifted_status=lifted_status,
                created_by=request.user
            )
            pickup_transaction.save()

            transaction_amount = 0
            index = 0
            while f'wasteData[{index}][wasteType]' in request.POST:
                waste_type_id = request.POST.get(f'wasteData[{index}][wasteType]')
                price = request.POST.get(f'wasteData[{index}][price]')
                quantity = request.POST.get(f'wasteData[{index}][quantity]')
                
                waste_type = WasteType.objects.filter(id=waste_type_id).first()
            
                new_pickup_waste_data  = PickupWastData.objects.create(
                        waste_type=waste_type,
                        quantity=quantity,
                        price=price,  
                        pickup_transaction=pickup_transaction
                    )
                
                tot_amount = int(price)*int(quantity)
                transaction_amount += tot_amount
                new_pickup_waste_data.save()
                index += 1
            
            transaction_bal = transaction_amount - float(paid_amount)
            shop_id = pickup_transaction.shop_owner_id
            # pre_tra = PickupTransaction.objects.filter(shop_owner_id = shop_id).order_by('-id')[1]

            # total_amount = pre_tra.total_amount if pre_tra.total_amount is not None else Decimal('0.0')

            # if pre_tra:
            #     total_amount = pre_tra[0].total_amount if pre_tra[0].total_amount is not None else Decimal('0.0')
            # else:
            #     total_amount = Decimal('0.0')  
            try:
                pre_tra = PickupTransaction.objects.filter(shop_owner_id=shop_id).order_by('-id')[1]
                total_amount = pre_tra.total_amount if pre_tra.total_amount is not None else Decimal('0.0')
            except IndexError:
                total_amount = Decimal('0.0')         
            transaction_bal_decimal = Decimal(transaction_bal)
            balance = total_amount + transaction_bal_decimal

            pickup_transaction.transaction_amount = transaction_amount
            pickup_transaction.total_amount = balance
            pickup_transaction.save()

            return JsonResponse({'message': 'successfully add new transaction','path': '/transaction_list/'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt   
def get_materials_list(request,material_id):
    materials = PickupWastData.objects.filter(pickup_transaction_id=material_id).values('id','waste_type__wastename', 'price', 'quantity',)
    return JsonResponse({'materials': list(materials)})


@csrf_exempt  
def get_area_based_shops(request):
    try:
        post_data = request.POST
        cluster_area_id = request.GET.get('cluster_area_id')
        if cluster_area_id != '':
            shops = ShopOwner.objects.filter(cluser_aera =cluster_area_id)
            shops_json = serializers.serialize('json', shops)
            return JsonResponse({'shops': shops_json}, safe=False)
        else:
            shops = ShopOwner.objects.none()
        return JsonResponse({'shop': shops})
    except Exception as e:
        return JsonResponse({'message': f'{e}'}, status=401)

@csrf_exempt  
@login_required
def password_updated(request):
    try:
        post_data = request.POST
        user_ID=request.user.id
        user = Users.objects.get(id=user_ID,is_active=True)
        if user:
            user.otp = request.POST.get('password')
            user.save()
        return JsonResponse({'message': 'successfully updated password'})
    except Exception as e:
        return JsonResponse({'message': f'{e}'}, status=401)