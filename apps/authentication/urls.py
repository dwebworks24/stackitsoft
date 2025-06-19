from django.urls import path
from apps.authentication import views
from apps.authentication import controller_logic
urlpatterns = [
    path('', views.otp_login, name='home'),
    path("logout/", views.logout_view, name="logout"),
    path('verify_otp/', views.sigin, name='verify_otp'),

    path("send_otp/", controller_logic.mobial_otp_logic, name="send_otp"),
    path("validate_otp/", controller_logic.mobial_otp_verify_logic, name="validate_otp"),
]