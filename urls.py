from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('register', views.register, name='register'),
    path('choose_district/<int:id>', views.choose_district, name='choose_district'),
    path('register_shop/<int:id>', views.register_shop, name='register_shop'),
    path('shop_register', views.shop_register, name='shop_register'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('view_district', views.view_district, name='view_district'),
    path('add_taluk/<int:id>',views.add_taluk, name='add_taluk'),
    path('taluk_add', views.taluk_add, name='taluk_add'),
    path('view_taluk/<int:id>', views.view_taluk, name='view_taluk'),
    path('ration_home', views.ration_home, name='ration_home'),
    path('view_ration/<int:id>', views.view_ration, name='view_ration'),
    path('view_ration_pending/<int:id>', views.view_ration_pending, name='view_ration_pending'),
    path('approve_ration/<int:id>', views.approve_ration, name='approve_ration'),
    path('view_user_requests', views.view_user_requests, name='view_user_requests'),
    path('ration_view_users', views.ration_view_users, name='ration_view_users'),
    path('approve_user/<str:id>', views.approve_user, name='approve_user'),
    path('add_card_items', views.add_card_items, name='add_card_items'),
    path('card_items_add', views.card_items_add, name='card_items_add'),
    path('edit_card_item/<int:id>', views.edit_card_item, name='edit_card_item'),
    path('card_item_edit', views.card_item_edit, name='card_item_edit'),
    path('delete_card_item/<int:id>', views.delete_card_item, name='delete_card_item'),

    path('view_card_items', views.view_card_items, name='view_card_items'),
    path('ration_card_items', views.ration_card_items, name='ration_card_items'),
    path('order_requests', views.order_requests, name='order_requests'),
    path('proceed_items/<int:id>', views.proceed_items, name='proceed_items'),
    path('send_items', views.send_items, name='send_items'),
    path('provide/<int:id>', views.provide, name='provide'),
    path('delete_available_item/<int:id>', views.delete_available_item, name='delete_available_item'),
    path('purchase_requests',views.purchase_requests, name='purchase_requests'),
    path('make_bill/<str:id>', views.make_bill, name='make_bill'),
    path('remove_available_item/<int:id>', views.remove_available_item, name='remove_available_item'),
    path('cancel_purchase/<int:id>', views.cancel_purchase, name='cancel_purchase'),
    path('make_purchase/<str:consid>/<str:ta>/<str:user>', views.make_purchase, name='make_purchase'),
    path('view_bills', views.view_bills, name='view_bills'),
    path('view_complaints', views.view_complaints, name='view_complaints'),
    path('send_reply', views.send_reply, name='send_reply'),
    path('bill_details/<int:id>', views.bill_details, name='bill_details'),
    path('admin_view_bills/<int:id>', views.admin_view_bills, name='admin_view_bills'),
    path('admin_bill_details/<int:id>', views.admin_bill_details, name='admin_bill_details'),











]