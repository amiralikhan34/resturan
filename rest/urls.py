# restaurant_app/urls.py

from django.urls import path
from . import views

urlpatterns = [


    path('categories/', views.category_list_create, name='category-list-create'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),

    # API endpoints for Size Options
    path('size-options/', views.size_option_list, name='size-option-list'),

    # API endpoints for Raw Materials
    path('raw-materials/', views.raw_material_list_create, name='raw-material-list-create'),
    path('raw-materials/<int:pk>/', views.raw_material_detail, name='raw-material-detail'),

    # API endpoints for Foods
    path('foods/', views.food_list_create, name='food-list-create'),
    path('foods/<int:pk>/', views.food_detail, name='food-detail'),

    # API endpoint for Dashboard Statistics
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]