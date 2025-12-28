from django.urls import path
from . import views

urlpatterns = [
    # path('', views.list_warehouses),
    path('', views.index, name='index'),
    path('materials/', views.list_materials, name='materials'),
    path('boms/', views.list_boms, name='boms'),
    path('warehouses/', views.list_warehouses, name='warehouses'),
    path('works/', views.list_works, name='works'),
    path('materials/<int:pk>/', views.detail_material, name='detail_material'),
    path('boms/<int:pk>/', views.detail_bom, name='detail_bom'),
    path('warehouses/<int:pk>/', views.detail_warehouse, name='detail_warehouse'),
    path('works/<int:pk>/', views.detail_work, name='detail_work'),
    path('create_material/', views.create_material, name='create_material'),
    path('delete_material/<int:pk>/', views.delete_material, name='delete_material'),
    path('create_bom/', views.create_bom, name='create_bom'),
    path('create_work/', views.create_work, name='create_work'),
    path('movements/', views.list_movements, name='movements'),
]
