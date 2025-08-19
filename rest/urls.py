# restaurant_app/urls.py

from django.urls import path
from . import views
from .views import (
    DashboardView,
    FoodItemListView,
    DirectSaleView,
    TokenLookupView,
    TokenRedeemView,
    RecentActivitiesView
)
from django.urls import path
from .views import (
    AvailableFoodsAPIView,
    IssueMultiCouponAPIView,
    WeeklyProgramAPIView,
    DashboardDataAPIView,
    CapacityByDateAPIView,
    PrintReceiptView

)



urlpatterns = [

    path('loginToAddFood/', views.login1, name='loginToAddFood'),
    path('logintokitchen/', views.logintokitchen, name='logintokitchen'),
    path('panelAddFood/', views.frontend_app_view, name='panelAddFood'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('delFinish/<int:pk>/', views.finishfood, name='delFinish'),
    path('categories/', views.category_list_create, name='category-list-create'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('size-options/', views.size_option_list, name='size-option-list'),
    path('raw-materials/', views.raw_material_list_create, name='raw-material-list-create'),
    path('raw-materials/<int:pk>/', views.raw_material_detail, name='raw-material-detail'),
    path('foods/', views.food_list_create, name='food-list-create'),
    path('foods/<int:pk>/', views.food_detail_api, name='food-detail'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
    path('api/raw-material/create/', views.raw_material_creates, name='raw_material_create'),
    path('create/servedfood', views.create_servedfood, name='create/servedfood'),
    path('issue-coupon/', views.issue_coupon_page, name='issue_coupon_page'),
    path('loginToCupon/', views.Logintocupopn, name='loginToCupon'),
    path('weekly-schedule/', views.weekly_schedule_list_create, name='weekly_schedule_list_create'),
    path('weekly-schedule/<int:pk>/', views.weekly_schedule_detail, name='weekly_schedule_detail'),
    path('weekly-schedule/<int:pk>/cooking-amount/',views.update_cooking_amount,name='weekly-update-cooking-amount'),
    path('delTask/<int:task_id>/',views.delTask,name='delTask'),
    path('dashboard-data/', views.dashboard_data, name='dashboard_data'),
    path('available-foods/', views.get_available_foods, name='get_available_foods'),  # مسیر جدید
    path('tahvil/', views.tahvil, name='tahvil'),  # مسیر جدید
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('food-items/', FoodItemListView.as_view(), name='food-item-list'),
    path('sales/direct/', DirectSaleView.as_view(), name='direct-sale'),
    path('tokens/lookup/', TokenLookupView.as_view(), name='token-lookup'),
    path('tokens/redeem/', TokenRedeemView.as_view(), name='token-redeem'),
    path('activities/recent/', RecentActivitiesView.as_view(), name='recent-activities'),
    path('kitchen/print-program/<int:food_id>/', views.print_food_program_pdf, name='print_food_program_pdf'),
    # URL برای دریافت لیست غذاهای موجود در یک تاریخ
    path('available-foods/', AvailableFoodsAPIView.as_view(), name='available_foods'),

    # URL برای صدور ژتون
    path('issue-multi-coupon/', IssueMultiCouponAPIView.as_view(), name='issue_multi_coupon'),

    # URL برای دریافت برنامه هفتگی
    path('weekly-program/', WeeklyProgramAPIView.as_view(), name='weekly_program'),

    # URL های داشبورد
    path('dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard_data'),
    path('capacity-by-date/', CapacityByDateAPIView.as_view(), name='capacity_by_date'),
    path('print-receipt/<str:tracking_code>/', PrintReceiptView.as_view(), name='print_receipt'),

]


