from django.urls import path, re_path
from apps.home import views
from apps.home import controller_logic

urlpatterns = [
    # path('dashboard/', views.cluster_datatables, name='dashboard'),
    # path('cluster_datatables/', views.datatables, name='cluster_datatables'),
    
    path('employee_datatables/', views.datatables, name='employee_datatables'),
    path('cluster_dashboard/', views.cluster_dashboard, name='cluster-dashboard'),

    path('password_change/', views.password_change, name='password_change'),
    path('addshop/', views.add_shop, name='addshop'),
    path('shop_list/', views.shop_list, name='shop_list'),
    path('add_transaction/', views.add_new_transaction_shop, name='add_transaction'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),

    path('save_shop/', controller_logic.shop_owner_save_logic, name='save_shop'),
    path('save_transaction_data/', controller_logic.save_new_transaction_data, name='save_transaction_data'),

    path('get_materials_list/<int:material_id>/', controller_logic.get_materials_list, name='get_materials_list'),
    
    path('get_shop_list/', controller_logic.get_area_based_shops, name='get_shop_list'),
    path('password_updated/', controller_logic.password_updated, name='password_updated'),
]
