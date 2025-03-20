from django.urls import path
from . import views

urlpatterns = [
    path('kl8/', views.lottery_data, {'lottery_type': 'kl8'}),
    path('3d/', views.lottery_data, {'lottery_type': '3d'}),
    path('p5/', views.lottery_data, {'lottery_type': 'p5'}),
    path('ssq/', views.lottery_data, {'lottery_type': 'ssq'}),
    path('super/', views.lottery_data, {'lottery_type': 'super'}),
]
