from django.urls import path
from . import views

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('deposit-products/top_rate/', views.top_rate),
    path('save-savings-products/', views.save_savings_products),
    path('savings-products/', views.savings_products),
    path('savings-product-options/<str:fin_prdt_cd>/', views.savings_product_options),
    path('savings-products/top_rate/', views.top_rate_savings_products),
]
