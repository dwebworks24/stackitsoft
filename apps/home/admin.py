import csv
from django.contrib import admin
from django.http import HttpResponse
# Register your models here.
from .models import *
# Register your models here.
class AdminUserlist(admin.ModelAdmin):
    list_display=('id','username','email')
    list_filter = ['username','email','phone','referal_code']
    actions = ['export_to_csv']
    def export_to_csv(self, request,queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=export.csv'
        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for obj in queryset:
             writer.writerow([getattr(obj, field) for field in fieldnames])
        return response
    export_to_csv.short_description = "Download selected as csv"

class AdminCluster_aera(admin.ModelAdmin):
    list_display=('id','cluster_aera',)

class AdminShopOwner(admin.ModelAdmin):
    list_display=('id','shopowner_number')


class AdminWasteType(admin.ModelAdmin):
    list_display=('id','quantity','wastename','price')


class AdminPickupTransaction(admin.ModelAdmin):
    list_display=('id','pickup_date','shop_owner','lifted_status',)


class AdminPickupWastData(admin.ModelAdmin):
    list_display=('id','waste_type','quantity','get_shop_owner')
    def get_shop_owner(self, obj):
        return obj.pickup_transaction.shop_owner

admin.site.register(Users,AdminUserlist)
admin.site.register(ShopOwner,AdminShopOwner)
admin.site.register(WasteType,AdminWasteType)
admin.site.register(PickupTransaction,AdminPickupTransaction)
admin.site.register(PickupWastData,AdminPickupWastData)
admin.site.register(Clusteraera,AdminCluster_aera)