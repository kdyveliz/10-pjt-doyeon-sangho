from django.urls import path
from . import views
urlpatterns = [
    path('finlife/save-deposit-products/', views.save_deposit_products),
    path('finlife/deposit-products/', views.deposit_products),
    path('finlife/deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('finlife/deposit-products/top_rate/', views.top_rate),
]
