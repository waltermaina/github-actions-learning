from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/bitcoin-price/', views.bitcoin_price_api, name='bitcoin_price_api'),
]
