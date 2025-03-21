from django.urls import path
from . import views

urlpatterns = [
    path('hot-cold/<str:lottery_type>/<int:limit>/', views.hot_cold_numbers)
]
