from django.urls import path
from . import views

urlpatterns = [
    path('contractors/', views.list_contractors, name='contractors'),
    path('contractors/<int:pk>/', views.detail_contractor, name='detail_contractor'),
    path('create_contractor/', views.create_contractor, name='create_contractor'),
]
