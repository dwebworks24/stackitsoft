from django.urls import path, re_path
from apps.home.views import *
from apps.home import controller_logic

urlpatterns = [
    path('', index, name='home'),
    path('about-us/', about_us, name='about-us'),
    path('buy-crypto-select/', buy_crypto_select, name='buy-crypto-select'),
    path('buy-crypto-confirm/', buy_crypto_confirm, name='buy-crypto-confirm'),
    path('buy-crypto-details/', buy_crypto_details, name='buy-crypto-details'),
    path('markets/', buy_crypto_details, name='markets'),
    path('contact-us/', contact_us, name='contact-us'),
    path('404/', custom_404_test),


    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('update-market/', update_market, name='update_market'),
    path('dashboard/', dashboard, name='dashboard'),

    

]
