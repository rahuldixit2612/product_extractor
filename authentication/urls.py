from django.urls import path
from . import views

urlpatterns = [
    path('', views.extract_data, name='extract_data'),
    path('extract-data/', views.extract_data, name='extract_data'),
]
