import csv
from django.contrib import admin
from django.http import HttpResponse
from apps.home.models import *
from apps.home.utils.email_utils import send_market_update_email_by_admin
from django.contrib.auth import get_user_model
# Register your models here.
class AdminUserlist(admin.ModelAdmin):
    list_display=('id','employee_id','username','email')
    list_filter = ['employee_id','username','email','phone']
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


class AdminMarketCoin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'created_at', 'update_at')

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # Check if it's a new object (not update)
        obj.updated_by = request.user  # Track who added it
        super().save_model(request, obj, form, change)

        if is_new:
            # Prepare price dictionary from the object
            prices = {
                '2PM': obj.price_2pm,
                '3PM': obj.price_3pm,
                '4PM': obj.price_4pm,
                '5PM': obj.price_5pm,
                '6PM': obj.price_6pm,
                '7PM': obj.price_7pm,
                '8PM': obj.price_8pm,
                '9PM': obj.price_9pm,
                '10PM': obj.price_10pm,
                '11PM': obj.price_11pm,
            }

            # Get all user emails
            User = get_user_model()
            recipient_list = list(
                User.objects.filter(email__isnull=False)
                .exclude(email__exact='')
                .values_list('email', flat=True)
            )

            # Send the email
            email_success, email_message = send_market_update_email_by_admin(
                market=obj,
                prices=prices,
                recipient_list=recipient_list,
                updated_by=request.user
            )

            # Optional message in Django admin
            if email_success:
                self.message_user(request, "MarketCoin added and email sent successfully.")
            else:
                self.message_user(request, f"MarketCoin added but email failed: {email_message}"),




admin.site.register(Users,AdminUserlist)
admin.site.register(MarketCoin,AdminMarketCoin)
