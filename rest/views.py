from django.shortcuts import redirect, render
from django.contrib import messages
from .models import rwmat
from django.http import JsonResponse
import json
from django.db.models.fields import return_None
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import Category, RawMaterial, Food, FoodRawMaterial, SizeOption , loginTokitchen ,loginToCupon , loginToTahvil
from django.contrib import messages
from .forms import RawMaterialForm
from . import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.utils import timezone # Import timezone for date/time handling
from datetime import datetime # Import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from django.utils import timezone
import jdatetime
import random
import string
from collections import defaultdict

from django.db import transaction
from django.db.models import F, Sum
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import WeeklySchedule, Coupon, Food
from .serializers import (
    MultiCouponIssueSerializer,
    AvailableFoodSerializer,
    WeeklyProgramSerializer
)


from .models import Category, SizeOption, RawMaterial, Food, FoodRawMaterial, WeeklySchedule ,Transaction
from .serializers import (
    CategorySerializer, SizeOptionSerializer, RawMaterialSerializer,
     FoodRawMaterialSerializer, WeeklyScheduleSerializer ,CouponSerializer ,TransactionSerializer
)

from .models import rwmat
from .serializers import (
    CategorySerializer,
    RawMaterialSerializer,
    FoodListSerializer,
    FoodDetailSerializer,
    SizeOptionSerializer,
    FoodRawMaterialSerializer

)
from .models import loginToAddFoodPage
from django.shortcuts import redirect , HttpResponse , render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum, F, Q
from django.db import transaction
from datetime import date, datetime

import random
import string
import uuid

# برای API Views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

from .models import Food, Coupon, Category, WeeklySchedule
from .serializers import CouponSerializer, WeeklyScheduleSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum, F, Q
from django.db import transaction
from datetime import date, datetime

import random
import string
import uuid


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

from .models import Food, Coupon, Category, WeeklySchedule

from .serializers import CouponSerializer, WeeklyScheduleSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, timedelta
from django.db import transaction
from django.db.models import F

from .models import (
    Food2, RawMaterial2, FoodBOMItem, WeeklyProgram,
    KitchenTask, KitchenInventoryItem, WarehouseInventoryItem
)

from .models import servedfood , rwmat



def frontend_app_view(request):
    if request.COOKIES.get('is_logged_in') != 'true':
        return HttpResponse('شما به این صفحه دسترسی ندارید . لطفا لاکین کنید')

    wSh=WeeklySchedule.objects.all()
    return render(request, 'AddFoodPage.html' ,{'wSh':wSh})


@api_view(['GET', 'POST'])
@csrf_exempt
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data,
                                        partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def size_option_list(request):
    sizes = SizeOption.objects.all()
    serializer = SizeOptionSerializer(sizes, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from .models import RawMaterial
from .serializers import RawMaterialSerializer

@api_view(['GET', 'POST'])
@csrf_exempt
def raw_material_list_create(request):
    if request.method == 'GET':
        queryset = RawMaterial.objects.all().select_related('category')

        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | \
                       queryset.filter(description__icontains=search_query)

        serializer = RawMaterialSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RawMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def raw_material_detail(request, pk):
    try:
        raw_material = RawMaterial.objects.get(pk=pk)
    except RawMaterial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RawMaterialSerializer(raw_material)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RawMaterialSerializer(raw_material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        raw_material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@csrf_exempt
def food_list_create(request):
    if request.method == 'GET':
        # حذف prefetch_related('available_sizes')
        queryset = Food.objects.all().select_related('category').prefetch_related('foodrawmaterial_set__raw_material')

        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | \
                       queryset.filter(description__icontains=search_query)

        serializer = FoodListSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FoodDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'GET':
        serializer = FoodDetailSerializer(food)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FoodDetailSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
@csrf_exempt
def dashboard_stats(request):
    total_categories = Category.objects.count()
    total_raw_materials = RawMaterial.objects.count()
    total_foods = Food.objects.count()

    top_consumed_materials = FoodRawMaterial.objects.values(
        'raw_material__name',
        'raw_material__unit_of_measurement'
    ).annotate(total_needed=Sum('quantity_needed')).order_by('-total_needed')[:3]

    stock_status_data = []
    for rm in RawMaterial.objects.all():
        hypothetical_max_stock = Decimal('30.0')
        # ✅ 'unit_price' جایگزین 'current_stock' شد.
        percentage = (rm.unit_price / hypothetical_max_stock) * 100 if hypothetical_max_stock > 0 else 0

        status_color = "green"
        if percentage < Decimal('30'):
            status_color = "red"
        elif percentage < Decimal('70'):
            status_color = "orange"

        stock_status_data.append({
            "name": f"{rm.name} ({rm.unit_price} {rm.unit_of_measurement})",
            "unit_price_value": float(rm.unit_price),
            "unit": rm.unit_of_measurement,
            "percentage": round(percentage),
            "status": status_color
        })

    stock_status_data.sort(key=lambda x: x['percentage'], reverse=True)

    example_food_structure = []
    # فیلتر کردن بر اساس food_type بجای نام غذا
    main_food_example = Food.objects.filter(food_type='main').first()
    if main_food_example:
        frm_queryset = main_food_example.foodrawmaterial_set.all().select_related('raw_material')
        example_food_structure = [
            {
                "quantity": f"{frm.quantity_needed} {frm.raw_material.unit_of_measurement}",
                "description": f"{frm.raw_material.name} {frm.notes if frm.notes else ''}".strip()
            }
            for frm in frm_queryset
        ]

    data = {
        "total_categories": total_categories,
        "total_raw_materials": total_raw_materials,
        "total_foods": total_foods,
        "top_consumed_materials": list(top_consumed_materials),
        "stock_status": stock_status_data,
        "example_food_structure": example_food_structure,
    }
    return Response(data)





def home(request):
    return render(request, 'PageOfPanel.html')



def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = loginToAddFoodPage.objects.filter(username=username, password=password).first()

        if user:
            response = redirect('/api/panelAddFood/')
            response.set_cookie('is_logged_in', 'true', max_age=3600)
            return response
        else:
            return HttpResponse("❌ نام کاربری یا رمز عبور اشتباه است", status=401)

    return render(request, 'LoginToAddFoodPage.html')


# rest/views.py

from django.shortcuts import render, redirect
import jdatetime
from datetime import timedelta
from .models import WeeklySchedule, RawMaterial, Food, rwmat, servedfood  # مدل‌های مورد نیاز را ایمپورت کنید


def kitchen(request):
    if 'kitchen_user' not in request.COOKIES:
        return redirect('/login-kitchen/')

    # --- مرحله ۱: دریافت پارامترها از URL ---
    view_type = request.GET.get('view_type', 'daily')

    # تاریخ را از URL بخوان، اگر نبود از امروز استفاده کن
    date_str = request.GET.get('date')
    if date_str:
        try:
            # تبدیل رشته تاریخ میلادی از URL به آبجکت jdatetime
            gregorian_date = jdatetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            base_date = jdatetime.date.fromgregorian(date=gregorian_date)
        except ValueError:
            base_date = jdatetime.date.today()
    else:
        base_date = jdatetime.date.today()

    # --- مرحله ۲: محاسبه بازه زمانی صحیح ---
    if view_type == 'daily':
        start_date_g = base_date.togregorian()
        end_date_g = base_date.togregorian()
        display_date = base_date.strftime('%A %d %B %Y')

    elif view_type == 'weekly':
        # محاسبه شروع هفته بر اساس تاریخ نمایش داده شده
        start_of_week = base_date - timedelta(days=(base_date.weekday() + 1) % 7)
        end_of_week = start_of_week + timedelta(days=6)
        start_date_g = start_of_week.togregorian()
        end_date_g = end_of_week.togregorian()
        display_date = f"هفته منتهی به {end_of_week.strftime('%d %B')}"

    else:  # monthly
        start_of_month = base_date.replace(day=1)
        # برای پیدا کردن روز آخر ماه بعد، یک ماه به تاریخ اضافه کرده و یک روز کم می‌کنیم
        next_month_start = (start_of_month + timedelta(days=32)).replace(day=1)
        end_of_month = next_month_start - timedelta(days=1)

        start_date_g = start_of_month.togregorian()
        end_date_g = end_of_month.togregorian()
        display_date = f"ماه {start_of_month.strftime('%B %Y')}"

    # --- مرحله ۳: فقط یک کوئری برای برنامه‌ریزی ---
    # هر دو جدول از همین یک کوئری استفاده خواهند کرد
    schedules = WeeklySchedule.objects.filter(
        schedule_date__range=[start_date_g, end_date_g]
    ).select_related('food').order_by('schedule_date', 'meal_time')

    # --- مرحله ۴: آماده‌سازی Context برای ارسال به Template ---
    context = {
        # **مهم:** هر دو متغیر را با یک کوئری یکسان پر می‌کنیم
        # شما در template خود تصمیم می‌گیرید هر جدول را چگونه نمایش دهید
        'foods2': schedules,
        'WSh': schedules,

        # سایر داده‌های مورد نیاز
        'raw_materials': RawMaterial.objects.all(),
        'rwmat': rwmat.objects.all(),
        'rw_mater': RawMaterial.objects.all(),
        'is_served': servedfood.objects.all(),
        'foods': Food.objects.all(),  # برای dropdown ها

        # متغیرها برای کنترل فیلتر و تاریخ در template
        'current_jalali_date': display_date,
        'view_type': view_type,
    }

    return render(request, 'kitchen.html', context)

def food_list(request):
    foods = Food.objects.all().order_by('name')
    return render(request, 'food_list.html', {'foods': foods})

def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    bom_items = FoodBOMItem.objects.filter(food=food)
    return render(request, 'food_detail.html', {'food': food, 'bom_items': bom_items})

def food_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        Food.objects.create(name=name, price=price)
        return redirect('food_list')
    return render(request, 'food_form.html')

def food_edit(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        food.name = request.POST.get('name')
        food.price = request.POST.get('price')
        food.save()
        return redirect('food_detail', food_id=food.id)
    return render(request, 'food_form.html', {'food': food})

def food_delete(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect('food_list')


def raw_material_list(request):
    materials = RawMaterial.objects.all().order_by('name')
    return render(request, 'raw_material_list.html', {'materials': materials})




def weekly_program_list(request):
    programs = WeeklyProgram.objects.all().order_by('date')
    return render(request, 'weekly_program_list.html', {'programs': programs})

def weekly_program_current(request):
    today = timezone.localdate()
    days_since_saturday = (today.weekday() - 5 + 7) % 7
    start_of_week = today - timedelta(days=days_since_saturday)
    end_of_week = start_of_week + timedelta(days=6)

    programs = WeeklyProgram.objects.filter(date__range=[start_of_week, end_of_week])
    return render(request, 'weekly_program_list.html', {'programs': programs})



def kitchen_task_list(request):
    selected_date = request.GET.get('date', timezone.localdate().isoformat())
    try:
        selected_date = date.fromisoformat(selected_date)
    except ValueError:
        return HttpResponse("تاریخ نامعتبر است.")

    tasks = KitchenTask.objects.filter(date=selected_date).order_by('time')
    return render(request, 'kitchen_task_list.html', {'tasks': tasks, 'date': selected_date})



def kitchen_task_toggle(request, task_id):
    task = get_object_or_404(KitchenTask, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('kitchen_task_list')



def kitchen_inventory_list(request):
    items = KitchenInventoryItem.objects.all().order_by('raw_material__name')
    return render(request, 'kitchen_inventory_list.html', {'items': items})

def kitchen_inventory_add(request):
    if request.method == 'POST':
        raw_material_id = request.POST.get('raw_material')
        quantity = float(request.POST.get('quantity', 0))
        location = request.POST.get('location', 'محل پیش‌فرض آشپزخانه')

        try:
            raw_material = RawMaterial.objects.get(id=raw_material_id)
        except RawMaterial.DoesNotExist:
            return HttpResponse("ماده اولیه یافت نشد.")

        KitchenInventoryItem.objects.create(raw_material=raw_material, quantity=quantity, location=location)
        return redirect('kitchen_inventory_list')

    materials = RawMaterial.objects.all()
    return render(request, 'kitchen_inventory_form.html', {'materials': materials})




def transfer_from_warehouse(request):
    if request.method == 'POST':
        raw_material_id = request.POST.get('raw_material_id')
        quantity_to_transfer = float(request.POST.get('quantity', 0))
        location = request.POST.get('location', 'محل پیش‌فرض آشپزخانه')

        try:
            with transaction.atomic():
                warehouse_item = WarehouseInventoryItem.objects.get(raw_material_id=raw_material_id)
                if warehouse_item.quantity < quantity_to_transfer:
                    return HttpResponse("موجودی کافی در انبار نیست.")

                warehouse_item.quantity -= quantity_to_transfer
                warehouse_item.save()

                kitchen_item, created = KitchenInventoryItem.objects.get_or_create(
                    raw_material_id=raw_material_id,
                    defaults={'quantity': quantity_to_transfer, 'location': location}
                )
                if not created:
                    kitchen_item.quantity += quantity_to_transfer
                    kitchen_item.save()
            return redirect('kitchen_inventory_list')
        except WarehouseInventoryItem.DoesNotExist:
            return HttpResponse("ماده اولیه در انبار اصلی یافت نشد.")




def warehouse_inventory_list(request):
    items = WarehouseInventoryItem.objects.all().order_by('raw_material__name')
    return render(request, 'warehouse_inventory_list.html', {'items': items})



def warehouse_inventory_add(request):
    if request.method == 'POST':
        raw_material_id = request.POST.get('raw_material')
        quantity = float(request.POST.get('quantity', 0))
        location = request.POST.get('location', 'انبار اصلی')

        try:
            raw_material = RawMaterial.objects.get(id=raw_material_id)
        except RawMaterial.DoesNotExist:
            return HttpResponse("ماده اولیه یافت نشد.")

        WarehouseInventoryItem.objects.create(raw_material=raw_material, quantity=quantity, location=location)
        return redirect('warehouse_inventory_list')

    materials = RawMaterial.objects.all()
    return render(request, 'warehouse_inventory_form.html', {'materials': materials})



def warehouse_inventory_report(request):
    total_items = WarehouseInventoryItem.objects.count()
    low_stock = WarehouseInventoryItem.objects.filter(quantity__lt=F('min_quantity')).count()
    today = timezone.localdate()
    expired = WarehouseInventoryItem.objects.filter(expiry_date__lt=today).count()
    expiring_soon = WarehouseInventoryItem.objects.filter(expiry_date__gte=today, expiry_date__lte=today + timedelta(days=30)).count()

    return render(request, 'warehouse_inventory_report.html', {
        'total_items': total_items,
        'low_stock': low_stock,
        'expired': expired,
        'expiring_soon': expiring_soon,
    })




def finishfood(request, pk):
    task = get_object_or_404(Food, id=pk)
    task.is_finish = True
    task.save(update_fields=['is_finish'])
    return redirect('/api/kitchen')


# In your views.py

from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect
from decimal import Decimal
import pytz
from .models import RawMaterial, rwmat  # Make sure your models are imported


def raw_material_creates(request):
    # Time restriction check
    try:
        iran_tz = pytz.timezone('Asia/Tehran')
        now_in_iran = timezone.now().astimezone(iran_tz)
        if not (now_in_iran.hour >= 22 or now_in_iran.hour < 4):
            return HttpResponse("خطا: ثبت درخواست فقط بین ساعت ۴ بامداد تا ۱۰ صبح امکان‌پذیر است.")
    except pytz.UnknownTimeZoneError:
        return HttpResponse("خطا: منطقه زمانی 'Asia/Tehran' یافت نشد.")

    # Process the form
    if request.method == "POST":
        name = request.POST.get("name")
        quantity_str = request.POST.get("quantity")
        coding = request.POST.get("coding")

        if not all([name, quantity_str, coding]):
            return HttpResponse("خطا: نام ماده، مقدار و کدینگ نمی‌توانند خالی باشند.")

        try:
            quantity_to_transfer = Decimal(quantity_str)
            if quantity_to_transfer <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return HttpResponse("خطا: مقدار وارد شده باید یک عدد مثبت معتبر باشد.")

        try:
            main_warehouse_item = RawMaterial.objects.get(coding=coding, name=name)
        except RawMaterial.DoesNotExist:
            return HttpResponse("خطا: ماده اولیه‌ای با این نام و کدینگ در انبار اصلی یافت نشد.")

        # This line will now work correctly


        try:
            kitchen_item, created = rwmat.objects.get_or_create(
                name=name,
                defaults={
                    'unit': main_warehouse_item.unit_of_measurement,
                    'quantity': 0
                }
            )
            kitchen_item.quantity += quantity_to_transfer
            kitchen_item.save()

            # This line will also work correctly now
            main_warehouse_item.current_stock -= quantity_to_transfer
            main_warehouse_item.save()

            return redirect('/api/kitchen/')

        except Exception as e:
            return HttpResponse(f"خطا در هنگام ثبت در دیتابیس: {e}")

    return redirect('/api/kitchen/')


def logintokitchen(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = loginTokitchen.objects.filter(username=username, password=password).first()
        if user:
            response = redirect('/api/kitchen')


            response.set_cookie('kitchen_user', username, max_age=24 * 60 * 60, httponly=True)
            return response
        else:
            return HttpResponse("اطلاعات وارد شده نادرست است")

    return render(request, 'loginKitchen.html')



def create_servedfood(request):
    name = request.POST.get('name')
    prep_time = request.POST.get('preparation_time_minutes')
    tedad = request.POST.get('tedad')
    is_finish = request.POST.get('is_finish') == 'on'

    servedfood.objects.create(
        name=name,
        preparation_time_minutes=prep_time or None,
        tedad=tedad or None,
        is_finish=is_finish
    )
    return redirect('/api/kitchen')










def Logintocupopn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = loginToCupon.objects.filter(username=username, password=password).first()
        if user:
            response = redirect('/api/issue-coupon/')
            response.set_cookie('copun', username, max_age=24 * 60 * 60, httponly=True)
            return response
        else:
            return HttpResponse("اطلاعات وارد شده نادرست است")


    return render(request, 'loginCupon.html')




def generate_coupon_code(food_id, phone_number, issue_date_gregorian):

    if not isinstance(issue_date_gregorian, date):

        if isinstance(issue_date_gregorian, datetime):
            issue_date_gregorian = issue_date_gregorian.date()
        else:

            issue_date_gregorian = date.today()


    phone_part = phone_number[-3:] if phone_number and len(phone_number) >= 3 else "000"

    date_part = issue_date_gregorian.strftime('%j')

    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))

    code = f"{phone_part}{date_part}{random_part}"


    if len(code) > 9:
        code = code[:9]
    elif len(code) < 9:
        code += ''.join(random.choices(string.ascii_uppercase + string.digits, k=9 - len(code)))

    return code.upper()


def get_today_schedule_for_food_and_meal(food_id, meal_time, check_date=None):

    target_date = check_date if check_date else timezone.localdate()
    try:
        schedule = WeeklySchedule.objects.get(
            schedule_date=target_date,
            food_id=food_id,
            meal_time=meal_time
        )
        return schedule
    except WeeklySchedule.DoesNotExist:
        return None



def frontend_app_view(request):
    if request.COOKIES.get('is_logged_in') != 'true':
        return HttpResponse('شما به این صفحه دسترسی ندارید . لطفا لاکین کنید')

    wSh = WeeklySchedule.objects.all()
    return render(request, 'AddFoodPage.html', {'wSh': wSh})


def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = loginToAddFoodPage.objects.filter(username=username, password=password).first()

        if user:
            response = redirect('/api/panelAddFood/')
            response.set_cookie('is_logged_in', 'true', max_age=3600, httponly=True)
            return response
        else:
            return HttpResponse("❌ نام کاربری یا رمز عبور اشتباه است", status=401)

    return render(request, 'LoginToAddFoodPage.html')


def home(request):
    return render(request, 'PageOfPanel.html')


def logintokitchen(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = loginTokitchen.objects.filter(username=username, password=password).first()
        if user:
            response = redirect('/api/kitchen')
            response.set_cookie('kitchen_user', username, max_age=24 * 60 * 60, httponly=True)
            return response
        else:
            return HttpResponse("اطلاعات وارد شده نادرست است")

    return render(request, 'loginKitchen.html')


def kitchen(request):
    if 'kitchen_user' not in request.COOKIES:
        return redirect('/login-kitchen/')

    persian_months = {
        1: "فروردین", 2: "اردیبهشت", 3: "خرداد",
        4: "تیر", 5: "مرداد", 6: "شهریور",
        7: "مهر", 8: "آبان", 9: "آذر",
        10: "دی", 11: "بهمن", 12: "اسفند"
    }

    persian_weekdays = {
        0: "شنبه", 1: "یکشنبه", 2: "دوشنبه", 3: "سه‌شنبه",
        4: "چهارشنبه", 5: "پنجشنبه", 6: "جمعه"
    }

    view_type = request.GET.get('view_type', 'daily')
    date_str = request.GET.get('date')

    if date_str:
        try:
            gregorian_date = jdatetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            base_date = jdatetime.date.fromgregorian(date=gregorian_date)
        except ValueError:
            base_date = jdatetime.date.today()
    else:
        base_date = jdatetime.date.today()

    if view_type == 'daily':
        start_date_g = end_date_g = base_date.togregorian()
        weekday_name = persian_weekdays[base_date.weekday()]
        display_date = f"{weekday_name}، {base_date.day} {persian_months[base_date.month]} {base_date.year}"

    elif view_type == 'weekly':
        start_of_week = base_date - timedelta(days=(base_date.weekday() + 1) % 7)
        end_of_week = start_of_week + timedelta(days=6)
        start_date_g = start_of_week.togregorian()
        end_date_g = end_of_week.togregorian()
        display_date = f"هفته منتهی به {end_of_week.day} {persian_months[end_of_week.month]}"

    else:  # 'monthly'
        start_of_month = base_date.replace(day=1)
        next_month_start = (start_of_month + timedelta(days=32)).replace(day=1)
        end_of_month = next_month_start - timedelta(days=1)
        start_date_g = start_of_month.togregorian()
        end_date_g = end_of_month.togregorian()
        display_date = f"ماه {persian_months[start_of_month.month]} {start_of_month.year}"

    schedules = WeeklySchedule.objects.filter(
        schedule_date__range=[start_date_g, end_date_g]
    ).select_related('food').order_by('schedule_date', 'meal_time')

    context = {
        'foods2': schedules,
        'foods3': Food.objects.all(),
        'WSh': schedules,
        'raw_materials': RawMaterial.objects.all(),
        'rwmat': rwmat.objects.all(),
        'rw_mater': RawMaterial.objects.all(),
        'is_served': servedfood.objects.all(),
        'foods': Food.objects.all(),
        'current_jalali_date': display_date,
        'view_type': view_type,
    }

    return render(request, 'kitchen.html', context)


def Logintocupopn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = loginToCupon.objects.filter(username=username, password=password).first()
        if user:
            response = redirect('/api/issue-coupon/')
            response.set_cookie('copun', username, max_age=24 * 60 * 60, httponly=True)
            return response
        else:
            return HttpResponse("اطلاعات وارد شده نادرست است")

    return render(request, 'loginCupon.html')


def tahvil(request):
    if 'tahvil' not in request.COOKIES:
        return redirect('api/loginToTahvil/')  # مسیر ورود پنل تحویل
    else:
        return render(request, 'tahvil.html')


def logintotahvil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = loginToTahvil.objects.filter(username=username, password=password).first()

        if user:
            response = redirect('/api/tahvil/')
            response.set_cookie('tahvil', username, max_age=24 * 60 * 60, httponly=True)
            return response
        else:
            return HttpResponse("اطلاعات وارد شده نادرست است", status=401)
    else:
        return render(request, 'loginToTahvil.html')




@api_view(['GET', 'POST'])
@csrf_exempt
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def size_option_list(request):
    sizes = SizeOption.objects.all()
    serializer = SizeOptionSerializer(sizes, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@csrf_exempt
def raw_material_list_create(request):
    if request.method == 'GET':
        queryset = RawMaterial.objects.all().select_related('category')

        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | \
                       queryset.filter(description__icontains=search_query)

        serializer = RawMaterialSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RawMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def raw_material_detail(request, pk):
    try:
        raw_material = RawMaterial.objects.get(pk=pk)
    except RawMaterial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RawMaterialSerializer(raw_material)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RawMaterialSerializer(raw_material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        raw_material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@csrf_exempt
def food_list_create(request):
    if request.method == 'GET':
        # ✅ 'available_sizes' از prefetch_related حذف شد.
        # ✅ 'food_type' به عنوان فیلتر جدید اضافه شد.
        queryset = Food.objects.all().select_related('category').prefetch_related(
            'foodrawmaterial_set__raw_material'
        )

        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | \
                       queryset.filter(description__icontains=search_query) | \
                       queryset.filter(food_type__icontains=search_query)

        serializer = FoodListSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FoodDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def food_detail_api(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'GET':
        serializer = FoodDetailSerializer(food)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FoodDetailSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@csrf_exempt
def dashboard_stats(request):
    total_categories = Category.objects.count()
    total_raw_materials = RawMaterial.objects.count()
    total_foods = Food.objects.count()

    top_consumed_materials = FoodRawMaterial.objects.values(
        'raw_material__name',
        'raw_material__unit_of_measurement'
    ).annotate(total_needed=Sum('quantity_needed')).order_by('-total_needed')[:3]

    stock_status_data = []
    for rm in RawMaterial.objects.all():
        hypothetical_max_stock = Decimal('30.0')  # این مقدار باید از مدل یا تنظیمات خوانده شود
        percentage = (rm.unit_price / hypothetical_max_stock) * 100 if hypothetical_max_stock > 0 else 0

        status_color = "green"
        if percentage < Decimal('30'):
            status_color = "red"
        elif percentage < Decimal('70'):
            status_color = "orange"

        stock_status_data.append({
            "name": f"{rm.name} ({rm.unit_price} {rm.unit_of_measurement})",
            "unit_price_value": float(rm.unit_price),
            "unit": rm.unit_of_measurement,
            "percentage": round(percentage),
            "status": status_color
        })

    stock_status_data.sort(key=lambda x: x['percentage'], reverse=True)

    example_food_structure = []
    chello_kabob = Food.objects.filter(name="چلو کباب کوبیده").first()
    if chello_kabob:
        frm_queryset = chello_kabob.foodrawmaterial_set.all().select_related('raw_material')
        example_food_structure = [
            {
                "quantity": f"{frm.quantity_needed} {frm.raw_material.unit_of_measurement}",
                "description": f"{frm.raw_material.name} {frm.notes if frm.notes else ''}".strip()
            }
            for frm in frm_queryset
        ]

    data = {
        "total_categories": total_categories,
        "total_raw_materials": total_raw_materials,
        "total_foods": total_foods,
        "top_consumed_materials": list(top_consumed_materials),
        "stock_status": stock_status_data,
        "example_food_structure": example_food_structure,
    }
    return Response(data)





def update_cooking_amount(request, pk):

    obj = get_object_or_404(WeeklySchedule, pk=pk)

    if request.method == 'POST':

        cooking_amount_val = request.POST.get('cooking_amount', None)


        try:
            obj.cooking_amount = int(cooking_amount_val)
        except (ValueError, TypeError):

            obj.cooking_amount = cooking_amount_val if cooking_amount_val else ''

        obj.save(update_fields=['cooking_amount'])
        messages.success(request, 'مقدار طبخ با موفقیت ذخیره شد.')

        return redirect("/api/kitchen/")  # برگرد به صفحه‌ای که ازش اومده


# In your views.py

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import WeeklySchedule, rwmat  # نام مدل برنامه غذایی و انبار آشپزخانه خود را وارد کنید
from decimal import Decimal


# یک تابع کمکی برای تبدیل واحدها (بسیار مهم)
# این تابع گرم را به کیلوگرم تبدیل می‌کند. می‌توانید آن را گسترش دهید.
def convert_to_kitchen_unit(quantity, unit_from, unit_to):
    """Converts quantity from one unit to another (e.g., gram to kilogram)."""
    unit_from = unit_from.lower()
    unit_to = unit_to.lower()

    if unit_from == unit_to:
        return quantity

    # تبدیل گرم به کیلوگرم
    if unit_from in ['g', 'gr', 'gram', 'گرم'] and unit_to in ['kg', 'kilogram', 'کیلوگرم']:
        return quantity / Decimal('1000')

    # تبدیل کیلوگرم به گرم
    if unit_from in ['kg', 'kilogram', 'کیلوگرم'] and unit_to in ['g', 'gr', 'gram', 'گرم']:
        return quantity * Decimal('1000')

    # اگر تبدیل تعریف نشده بود، خطا برگردان
    raise ValueError(f"امکان تبدیل واحد از '{unit_from}' به '{unit_to}' وجود ندارد.")


def delTask(request, task_id):
    """
    This view marks a task as finished and deducts the consumed raw materials
    from the kitchen inventory based on the food's BOM.
    """
    # ۱. برنامه غذایی مورد نظر را پیدا کن
    schedule = get_object_or_404(WeeklySchedule, pk=task_id)

    # اگر غذا قبلا تمام شده، کاری انجام نده
    if schedule.is_finished:
        return redirect('/api/kitchen/')

        # ۲. بررسی کن که آیا مقدار طبخ ثبت شده است یا نه
    if not schedule.cooking_amount or schedule.cooking_amount <= 0:
        return HttpResponse(f"خطا: لطفا ابتدا مقدار طبخ را برای غذای '{schedule.food.name}' ثبت کنید.")

    food_to_cook = schedule.food
    boms = food_to_cook.foodrawmaterial_set.all()
    cooked_quantity = schedule.cooking_amount

    # ۳. به ازای هر ماده اولیه در BOM، محاسبه را انجام بده
    for bom_item in boms:
        raw_material = bom_item.raw_material
        quantity_per_portion = bom_item.quantity_needed  # مقدار لازم برای یک پرس

        # مقدار کل مصرفی برای این ماده اولیه
        total_consumed = quantity_per_portion * cooked_quantity

        try:
            # ۴. ماده اولیه را در انبار آشپزخانه (rwmat) پیدا کن
            kitchen_inventory_item = rwmat.objects.get(name=raw_material.name)

            # ۵. تبدیل واحد را انجام بده
            # واحد ماده اولیه در BOM (مثلا گرم) را به واحد همان ماده در انبار آشپزخانه (مثلا کیلوگرم) تبدیل کن
            unit_from_bom = raw_material.unit_of_measurement
            unit_in_kitchen = kitchen_inventory_item.unit

            try:
                consumed_in_kitchen_unit = convert_to_kitchen_unit(total_consumed, unit_from_bom, unit_in_kitchen)
            except ValueError as e:
                return HttpResponse(str(e))  # نمایش خطای تبدیل واحد

            # ۶. بررسی کن آیا موجودی کافی است یا نه
            if kitchen_inventory_item.quantity < consumed_in_kitchen_unit:
                return HttpResponse(
                    f"خطا: موجودی '{raw_material.name}' در انبار آشپزخانه کافی نیست. نیاز: {consumed_in_kitchen_unit} {unit_in_kitchen} | موجودی: {kitchen_inventory_item.quantity} {unit_in_kitchen}")

            # ۷. از موجودی انبار آشپزخانه کم کن و ذخیره کن
            kitchen_inventory_item.quantity -= consumed_in_kitchen_unit
            kitchen_inventory_item.save()

        except rwmat.DoesNotExist:
            return HttpResponse(
                f"خطا: ماده اولیه '{raw_material.name}' در انبار آشپزخانه شما ثبت نشده است. لطفا ابتدا آن را از انبار اصلی تحویل گرفته و ثبت کنید.")
        except Exception as e:
            return HttpResponse(f"یک خطای پیش‌بینی نشده رخ داد: {e}")

    # ۸. در نهایت، برنامه غذایی را به عنوان "تمام شده" علامت بزن
    schedule.is_finished = True
    schedule.save()

    return redirect('/api/kitchen/')


def create_servedfood(request):

    name = request.POST.get('name')
    prep_time = request.POST.get('preparation_time_minutes')
    tedad = request.POST.get('tedad')
    is_finish = request.POST.get('is_finish') == 'on'

    servedfood.objects.create(
        name=name,
        preparation_time_minutes=prep_time or None,
        tedad=tedad or None,
        is_finish=is_finish
    )
    messages.success(request, f"غذای '{name}' به عنوان سرو شده ثبت شد.")
    return redirect('/api/kitchen')







@api_view(['GET'])
def get_available_foods(request):
    selected_date_str = request.query_params.get('date')



    current_date_gregorian = timezone.localdate()
    if selected_date_str:
        try:
            current_date_gregorian = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "فرمت تاریخ نامعتبر است. از YYYY-MM-DD استفاده کنید."},
                            status=status.HTTP_400_BAD_REQUEST)


    available_schedules = WeeklySchedule.objects.filter(
        schedule_date=current_date_gregorian,
        capacity_nazry__gt=F('issued_nazry_count')
    ).select_related('food', 'food__category').order_by('meal_time', 'food__name')


    available_foods_data = []
    for schedule_entry in available_schedules:
        remaining_capacity = schedule_entry.remaining_nazry_capacity
        food_data = {
            'id': schedule_entry.food.id,
            'name': schedule_entry.food.name,
            'category_name': schedule_entry.food.category.name if schedule_entry.food.category else 'بدون دسته',
            'remaining_nazry_capacity': remaining_capacity,
            'meal_time': schedule_entry.meal_time,
            'meal_time_display': schedule_entry.get_meal_time_display()
        }
        available_foods_data.append(food_data)

    return Response(available_foods_data)


@api_view(['GET'])
def dashboard_data(request):
    today_gregorian = timezone.localdate()




    total_nazry_capacity_today = WeeklySchedule.objects.filter(
        schedule_date=today_gregorian,
        meal_time='lunch'
    ).aggregate(Sum('capacity_nazry'))['capacity_nazry__sum'] or 0


    issued_coupons_today_count = WeeklySchedule.objects.filter(
        schedule_date=today_gregorian,
        meal_time='lunch'
    ).aggregate(Sum('issued_nazry_count'))['issued_nazry_count__sum'] or 0


    remaining_nazry_capacity = max(0, total_nazry_capacity_today - issued_coupons_today_count)


    recent_coupons_today = Coupon.objects.filter(issue_date=today_gregorian).select_related('food',
                                                                                                  'food__category').order_by(
        '-issue_date')[:10]

    serialized_recent_coupons = []
    for coupon in recent_coupons_today:
        serialized_recent_coupons.append({
            'coupon_code': coupon.coupon_code,
            'family_name': coupon.family_name,
            'food_name': coupon.food.name,
            'food_category_name': coupon.food.category.name if coupon.food.category else '-',
            'count': coupon.count,
            'issue_date': coupon.issue_date.isoformat(),
        })

    data = {
        'issued_coupons_today_count': issued_coupons_today_count,
        'recent_coupons_today': serialized_recent_coupons,
        'total_nazry_capacity_today': total_nazry_capacity_today,
        'used_nazry_capacity_today': issued_coupons_today_count,
        'remaining_nazry_capacity': remaining_nazry_capacity,
        'can_issue_more_coupons': remaining_nazry_capacity > 0
    }
    return Response(data)



# کد کامل و اصلاح‌شده برای ویو weekly_schedule_list_create
@api_view(['GET', 'POST'])
@csrf_exempt
def weekly_schedule_list_create(request):
    if request.method == 'GET':
        # بخش GET بدون تغییر باقی می‌ماند
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        schedules = WeeklySchedule.objects.all().select_related('food', 'food__category')

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                schedules = schedules.filter(schedule_date__gte=start_date)
            except ValueError:
                return Response({"error": "فرمت تاریخ شروع نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                schedules = schedules.filter(schedule_date__lte=end_date)
            except ValueError:
                return Response({"error": "فرمت تاریخ پایان نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        schedules = schedules.order_by('schedule_date', 'meal_time', 'food__name')
        serializer = WeeklyScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # --- منطق جدید برای ایجاد یا به‌روزرسانی ---
        data = request.data
        food_id = data.get('food')
        schedule_date = data.get('schedule_date')
        meal_time = data.get('meal_time')

        # 1. بررسی می‌کنیم آیا رکوردی با این مشخصات وجود دارد یا خیر
        try:
            instance = WeeklySchedule.objects.get(
                food_id=food_id,
                schedule_date=schedule_date,
                meal_time=meal_time
            )
            # 2. اگر وجود داشت، آن را آپدیت می‌کنیم
            serializer = WeeklyScheduleSerializer(instance, data=data, partial=True)
            status_code = status.HTTP_200_OK # وضعیت موفقیت برای آپدیت
        except WeeklySchedule.DoesNotExist:
            # 3. اگر وجود نداشت، یک رکورد جدید ایجاد می‌کنیم
            serializer = WeeklyScheduleSerializer(data=data)
            status_code = status.HTTP_201_CREATED # وضعیت موفقیت برای ایجاد

        # 4. داده‌ها را اعتبارسنجی و ذخیره می‌کنیم
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status_code)

        # 5. اگر خطا وجود داشت، آن را برمی‌گردانیم
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def weekly_schedule_detail(request, pk):
    schedule = get_object_or_404(WeeklySchedule, pk=pk)

    if request.method == 'GET':
        serializer = WeeklyScheduleSerializer(schedule)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WeeklyScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        current_meal_time = request.query_params.get('meal_time', 'lunch')


        total_capacity_nazry = WeeklySchedule.objects.filter(
            schedule_date=today,
            meal_time=current_meal_time
        ).aggregate(Sum('capacity_nazry'))['capacity_nazry__sum'] or 0

        total_capacity_foroshi = WeeklySchedule.objects.filter(
            schedule_date=today,
            meal_time=current_meal_time
        ).aggregate(Sum('capacity_foroshi'))['capacity_foroshi__sum'] or 0


        total_issued_nazry_today = WeeklySchedule.objects.filter(
            schedule_date=today,
            meal_time=current_meal_time
        ).aggregate(Sum('issued_nazry_count'))['issued_nazry_count__sum'] or 0

        total_sold_foroshi_today = WeeklySchedule.objects.filter(
            schedule_date=today,
            meal_time=current_meal_time
        ).aggregate(Sum('issued_nazry_count'))['issued_nazry_count__sum'] or 0


        remaining_nazry_capacity_total = max(0, total_capacity_nazry - total_issued_nazry_today)
        remaining_foroshi_capacity_total = max(0, total_capacity_foroshi - total_sold_foroshi_today)


        today_transactions = Transaction.objects.filter(timestamp__date=today)
        today_direct_sales = today_transactions.filter(transaction_type='direct_sale').aggregate(Sum('quantity'))[
                                 'quantity__sum'] or 0
        today_token_deliveries = \
        today_transactions.filter(transaction_type='token_delivery').aggregate(Sum('quantity'))['quantity__sum'] or 0

        data = {
            'total_in_person_capacity_today': total_capacity_nazry,
            'total_sale_capacity_today': total_capacity_foroshi,
            'issued_in_person_today': total_issued_nazry_today,
            'sold_foroshi_today': total_sold_foroshi_today,
            'remaining_in_person_capacity': remaining_nazry_capacity_total,
            'remaining_sale_capacity': remaining_foroshi_capacity_total,
            'today_direct_sales_count': today_direct_sales,
            'today_token_deliveries_count': today_token_deliveries,
        }
        return Response(data, status=status.HTTP_200_OK)


class FoodItemListView(generics.ListAPIView):

    serializer_class = FoodListSerializer

    def get_queryset(self):
        today = timezone.localdate()
        current_meal_time = self.request.query_params.get('meal_time', 'lunch')


        schedules = WeeklySchedule.objects.filter(
            schedule_date=today,
            meal_time=current_meal_time,
            capacity_foroshi__gt=0
        ).select_related('food', 'food__category').order_by('food__name')



        foods_with_capacity = []
        for schedule in schedules:
            if schedule.remaining_foroshi_capacity > 0:
                foods_with_capacity.append({
                    'id': schedule.food.id,
                    'name': schedule.food.name,
                    'category_name': schedule.food.category.name if schedule.food.category else 'بدون دسته',
                    'remaining_foroshi_capacity': schedule.remaining_foroshi_capacity,
                })
        return foods_with_capacity

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        return Response(queryset)


MEAL_TIMES = ['breakfast', 'lunch', 'dinner', 'snack']


class DirectSaleView(APIView):
    def post(self, request, *args, **kwargs):
        food_id = request.data.get('food_id')
        quantity = request.data.get('quantity')
        customer_name = request.data.get('customer_name')
        phone_number = request.data.get('phone_number')

        if not all([food_id, quantity, customer_name]):
            return Response({'error': 'شناسه غذا، تعداد و نام مشتری الزامی هستند.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            food_item = get_object_or_404(Food, id=food_id)
        except (ValueError, TypeError):
            return Response({'error': 'تعداد باید یک عدد صحیح و مثبت باشد.'}, status=status.HTTP_400_BAD_REQUEST)
        except Food.DoesNotExist:
            return Response({'error': 'غذای انتخاب شده یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with db_transaction.atomic():
                schedule = None
                for mt in MEAL_TIMES:
                    try:
                        s = WeeklySchedule.objects.select_for_update().get(
                            food=food_item,
                            schedule_date=timezone.localdate(),
                            meal_time=mt
                        )
                        if quantity <= s.remaining_foroshi_capacity:
                            schedule = s
                            meal_time = mt
                            break
                    except WeeklySchedule.DoesNotExist:
                        continue

                if not schedule:
                    return Response({'error': 'برای هیچ یک از وعده‌های امروز ظرفیت فروشی کافی یافت نشد.'},
                                    status=status.HTTP_404_NOT_FOUND)

                schedule.issued_foroshi_count = F('issued_foroshi_count') + quantity
                schedule.save(update_fields=['issued_foroshi_count'])

                transaction = Transaction.objects.create(
                    customer_name=customer_name,
                    phone_number=phone_number,
                    food_item=food_item,
                    quantity=quantity,
                    transaction_type='direct_sale'
                )

                return Response({
                    'message': f'{quantity} پرس {food_item.name} با موفقیت در وعده {meal_time} به {customer_name} فروخته شد.',
                    'transaction': TransactionSerializer(transaction).data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'خطا در ثبت فروش: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# views.py

from django.utils import timezone
from django.db.models import F
from django.db import transaction as db_transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# ... سایر import های شما

class TokenLookupView(APIView):
    def post(self, request, *args, **kwargs):
        token_number = request.data.get('coupon_code')
        if not token_number:
            return Response({'error': 'کد ژتون لازم است.'}, status=status.HTTP_400_BAD_REQUEST)

        # --- شروع بخش عیب‌یابی ---
        print(f"==================== DEBUGGING ====================")
        print(f"Searching for Token: {token_number}")
        today_date = timezone.localdate()
        print(f"Server's understanding of 'today' is: {today_date}")
        # --- پایان بخش عیب‌یابی ---

        try:
            coupon = Coupon.objects.select_related('food__category').get(tracking_code=token_number)

            if coupon.is_used:
                return Response({'error': 'این ژتون قبلا استفاده شده است.'}, status=status.HTTP_400_BAD_REQUEST)

            schedule = None
            meal_time_display = None  # برای نمایش نام فارسی در پیام موفقیت‌آمیز

            # ===== تغییر اصلی و نهایی اینجاست =====
            # از مقادیر انگلیسی که در دیتابیس ذخیره شده استفاده می‌کنیم
            MEAL_TIMES_CHOICES = {
                'breakfast': 'صبحانه',
                'lunch': 'ناهار',
                'dinner': 'شام'
            }

            for db_value, display_name in MEAL_TIMES_CHOICES.items():
                s = WeeklySchedule.objects.filter(
                    food=coupon.food,
                    schedule_date=timezone.localdate(),
                    meal_time=db_value  # <--- جستجو با مقدار صحیح دیتابیس
                ).first()

                if s and coupon.count <= s.remaining_nazry_capacity:
                    schedule = s
                    meal_time_display = display_name
                    break
            # =====================================

            if not schedule:
                return Response({'error': 'برای هیچ یک از وعده‌های امروز ظرفیت حضرتی کافی یافت نشد.'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = CouponSerializer(coupon)
            response_data = serializer.data
            response_data['food_name'] = coupon.food.name
            response_data['meal_time'] = meal_time_display  # نمایش نام فارسی

            return Response(response_data, status=status.HTTP_200_OK)

        except Coupon.DoesNotExist:
            return Response({'error': 'ژتون یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)


# views.py
class TokenRedeemView(APIView):
    def post(self, request, *args, **kwargs):
        token_number = request.data.get('coupon_code')
        if not token_number:
            return Response({'error': 'کد ژتون لازم است.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # جستجو بر اساس کد رهگیری (tracking_code) انجام می‌شود
            coupon = Coupon.objects.select_related('food').get(tracking_code=token_number)
        except Coupon.DoesNotExist:
            return Response({'error': 'ژتون یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        if coupon.is_used:
            return Response({'error': 'این ژتون قبلا استفاده شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                schedule = None
                meal_time_display = None # برای نمایش نام فارسی در پیام موفقیت‌آمیز

                # ===== تغییر اصلی اینجاست =====
                # از مقادیر انگلیسی که در دیتابیس ذخیره شده برای جستجو استفاده می‌کنیم
                MEAL_TIMES_CHOICES = {
                    'breakfast': 'صبحانه',
                    'lunch': 'ناهار',
                    'dinner': 'شام'
                }

                for db_value, display_name in MEAL_TIMES_CHOICES.items():
                    try:
                        s = WeeklySchedule.objects.select_for_update().get(
                            food=coupon.food,
                            schedule_date=timezone.localdate(),
                            meal_time=db_value # <--- جستجو با مقدار صحیح دیتابیس
                        )
                        if coupon.count <= s.remaining_nazry_capacity:
                            schedule = s
                            meal_time_display = display_name
                            break
                    except WeeklySchedule.DoesNotExist:
                        # اگر برای این وعده برنامه‌ای نبود، به سراغ وعده بعدی می‌رویم
                        continue
                # =====================================

                if not schedule:
                    return Response({'error': 'برای هیچ یک از وعده‌های امروز ظرفیت حضرتی کافی یافت نشد.'},
                                    status=status.HTTP_404_NOT_FOUND)

                # به‌روزرسانی وضعیت ژتون و برنامه غذایی
                coupon.is_used = True
                coupon.save(update_fields=['is_used'])

                schedule.issued_nazry_count = F('issued_nazry_count') + coupon.count
                schedule.save(update_fields=['issued_nazry_count'])

                # ثبت تراکنش
                transaction = Transaction.objects.create(
                    customer_name=coupon.family_name,
                    phone_number=coupon.phone_number,
                    food_item=coupon.food,
                    quantity=coupon.count,
                    transaction_type='token_delivery',
                    coupon=coupon
                )

                return Response({
                    # از نام فارسی وعده در پیام استفاده می‌کنیم
                    'message': f'{coupon.count} پرس {coupon.food.name} در وعده {meal_time_display} با موفقیت به {coupon.family_name} تحویل داده شد.',
                    'transaction': TransactionSerializer(transaction).data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            # لاگ کردن خطا برای عیب‌یابی بهتر در آینده
            print(f"An unexpected error occurred in TokenRedeemView: {str(e)}")
            return Response({'error': f'خطا در تحویل ژتون: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecentActivitiesView(generics.ListAPIView):
    queryset = Transaction.objects.all().select_related('food_item', 'coupon').order_by('-timestamp')[:10]
    serializer_class = TransactionSerializer



class FoodCategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodDetailSerializer


class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodDetailSerializer

class RecentActivitiesView(generics.ListAPIView):
    queryset = Transaction.objects.all().select_related('food_item', 'coupon').order_by('-timestamp')[:10]
    serializer_class = TransactionSerializer



class FoodCategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodDetailSerializer


class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodDetailSerializer





def logintotahvil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = loginToTahvil.objects.filter(username=username, password=password).first()

        if user:

            response = redirect('/api/tahvil/')
            response.set_cookie('tahvil', username, max_age=24 * 60 * 60, httponly=True)
            return response
        else:

            return HttpResponse("اطلاعات وارد شده نادرست است", status=401)
    else:
        try:

            return render(request, 'loginToTahvil.html')
        except Exception as e:

            return HttpResponse(f"قالب loginToTahvil.html پیدا نشد یا خطایی در رندر رخ داد: {e}", status=500)


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

# مدل‌های خود را به درستی ایمپورت کنید
# فرض می‌کنیم مدل برنامه‌ریزی شما WeeklySchedule نام دارد
from .models import Food, WeeklySchedule, FoodRawMaterial

# In rest/views.py

def print_food_program_pdf(request, food_id):
    # 1. آیتم WeeklySchedule را بر اساس ID دریافت کنید. اگر پیدا نشد، خود جنگو 404 می‌دهد.
    scheduled_item = get_object_or_404(WeeklySchedule, pk=food_id)

    # 2. تاریخ را از آیتم بخوانید
    jalali_date = "تاریخ ثبت نشده"
    if scheduled_item.schedule_date:
        try:
            # استفاده از کتابخانه jdatetime اگر در پروژه نصب است
            import jdatetime
            jalali_date = jdatetime.date.fromgregorian(date=scheduled_item.schedule_date).strftime('%Y/%m/%d')
        except (ImportError, TypeError):
            jalali_date = scheduled_item.schedule_date.strftime('%Y/%m/%d')

    # 3. تعریف اصلی غذا و مواد اولیه آن را از طریق رابطه ForeignKey پیدا کنید
    base_food = scheduled_item.food  # دسترسی مستقیم به آبجکت Food
    bom_materials = base_food.foodrawmaterial_set.all() if base_food else []

    # 4. داده‌ها را به قالب PDF ارسال کنید
    context = {
        'food_schedule': scheduled_item,
        'base_food': base_food,
        'bom_materials': bom_materials,
        'food_jalali_date': jalali_date,
    }

    html_string = render_to_string('pdf_templates/food_program_report.html', context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="food_program_{food_id}.pdf"'

    return response


# Dajngo Imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Sum

# Python Imports
from datetime import datetime, date, timedelta
import json
import random
import string

# Local Imports
from .models import Food, Coupon, WeeklySchedule


# =================================================================
# 1. Page Rendering View
# =================================================================

def issue_coupon_page(request):
    """
    این ویو فقط صفحه اصلی پنل را رندر می‌کند.
    """
    # (اگر از سیستم لاگین جنگو استفاده می‌کنید، بهتر است از @login_required استفاده کنید)
    if 'copun' not in request.COOKIES:
        return redirect('Logintocupopn')
    cupon = Coupon.objects.all()
    return render(request, 'issue_coupon.html' , {'cupon': cupon})


# =================================================================
# 2. API Views for the Frontend
# =================================================================
# In your views.py
class AvailableFoodsAPIView(APIView):
    """
    API برای دریافت لیست غذاهای موجود در یک تاریخ مشخص.
    فقط غذاهایی را برمی‌گرداند که ظرفیت نذری باقی‌مانده دارند.
    """

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Query parameter 'date' is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # فیلتر کردن برنامه‌هایی که در تاریخ مشخص شده قرار دارند و ظرفیت باقی‌مانده دارند
            schedules = WeeklySchedule.objects.filter(
                schedule_date=date_str,
                # استفاده از F object برای مقایسه دو فیلد در دیتابیس
                capacity_nazry__gt=F('issued_nazry_count')
            ).select_related('food')  # بهینه‌سازی کوئری با join کردن جدول غذا

            serializer = AvailableFoodSerializer(schedules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IssueMultiCouponAPIView(APIView):
    """
    API اصلی برای صدور ژتون گروهی.
    این ویو بسیار مهم است و عملیات را به صورت اتمیک (transactional) انجام می‌دهد.
    """

    def generate_tracking_code(self):
        """یک کد پیگیری 8 رقمی منحصر به فرد ایجاد می‌کند."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Coupon.objects.filter(tracking_code=code).exists():
                return code

    @transaction.atomic  # تضمین می‌کند که تمام عملیات دیتابیس یا با هم موفق شوند یا هیچ‌کدام
    def post(self, request):
        serializer = MultiCouponIssueSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        issue_date = validated_data['issue_date']
        items = validated_data['items']

        # ایجاد یک کد پیگیری برای این گروه از ژتون‌ها
        tracking_code = self.generate_tracking_code()
        created_coupons = []

        for item in items:
            food_id = item['food_id']
            count = item['count']

            try:
                # قفل کردن رکورد برنامه هفتگی برای جلوگیری از race condition
                # select_for_update تضمین می‌کند که هیچ درخواست دیگری همزمان این رکورد را تغییر ندهد
                schedule = WeeklySchedule.objects.select_for_update().get(
                    food_id=food_id,
                    schedule_date=issue_date
                )

                # بررسی مجدد ظرفیت در سمت سرور
                if schedule.remaining_nazry_capacity < count:
                    food = Food.objects.get(id=food_id)
                    # اگر ظرفیت کافی نبود، یک خطا با پیام مشخص برگردان
                    raise ValidationError(
                        f"ظرفیت برای غذای '{food.name}' کافی نیست. باقی‌مانده: {schedule.remaining_nazry_capacity}")

                # **منطق اصلی: افزایش تعداد صادر شده**
                schedule.issued_nazry_count = F('issued_nazry_count') + count
                schedule.save()

                # ایجاد ژتون در دیتابیس
                coupon = Coupon.objects.create(
                    food_id=food_id,
                    family_name=validated_data['family_name'],
                    phone_number=validated_data['phone_number'],
                    count=count,
                    issue_date=issue_date,
                    coupon_code=f"C-{food_id}-{random.randint(1000, 9999)}",  # یک کد ساده
                    tracking_code=tracking_code,
                    coupon_type='nazry'  # چون از ظرفیت نذری کم می‌کنیم
                )
                created_coupons.append(coupon)

            except WeeklySchedule.DoesNotExist:
                return Response(
                    {"error": f"غذایی با شناسه {food_id} برای تاریخ {issue_date} برنامه‌ریزی نشده است."},
                    status=status.HTTP_404_NOT_FOUND
                )
            except ValidationError as e:
                # برگرداندن خطای ظرفیت به فرانت‌اند
                return Response({"error": e.detail[0]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "ژتون با موفقیت صادر شد.", "tracking_code": tracking_code},
            status=status.HTTP_201_CREATED
        )


class WeeklyProgramAPIView(APIView):
    """
    API برای دریافت برنامه هفتگی غذاها.
    خروجی را بر اساس روزهای هفته فارسی گروه‌بندی می‌کند.
    """

    def get(self, request):
        today = jdatetime.date.today()
        start_of_week = today - jdatetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + jdatetime.timedelta(days=6)

        # تبدیل تاریخ شمسی به میلادی برای کوئری
        start_of_week_gregorian = start_of_week.togregorian()
        end_of_week_gregorian = end_of_week.togregorian()

        schedules = WeeklySchedule.objects.filter(
            schedule_date__range=[start_of_week_gregorian, end_of_week_gregorian]
        ).order_by('schedule_date').select_related('food')

        # گروه‌بندی نتایج بر اساس روز هفته
        program_by_day = defaultdict(list)
        for schedule in schedules:
            # استفاده از property مدل برای گرفتن نام روز فارسی
            day_name = schedule.persian_day_of_week
            serializer = WeeklyProgramSerializer(schedule)
            program_by_day[day_name].append(serializer.data)

        return Response(program_by_day)


# ویوهای داشبورد که در فرانت‌اند شما استفاده شده‌اند
class DashboardDataAPIView(APIView):
    def get(self, request):
        today = timezone.now().date()

        issued_today = Coupon.objects.filter(issue_date=today).aggregate(total=Sum('count'))['total'] or 0

        today_schedules = WeeklySchedule.objects.filter(schedule_date=today)
        total_capacity = today_schedules.aggregate(total=Sum('capacity_nazry'))['total'] or 0
        total_issued_on_schedules = today_schedules.aggregate(total=Sum('issued_nazry_count'))['total'] or 0

        data = {
            "issued_coupons_today_count": issued_today,
            "total_nazry_capacity_today": total_capacity,
            "remaining_nazry_capacity": total_capacity - total_issued_on_schedules
        }
        return Response(data)


class CapacityByDateAPIView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Query parameter 'date' is required."}, status=status.HTTP_400_BAD_REQUEST)

        schedules = WeeklySchedule.objects.filter(schedule_date=date_str)
        total_capacity = schedules.aggregate(total=Sum('capacity_nazry'))['total'] or 0
        total_issued = schedules.aggregate(total=Sum('issued_nazry_count'))['total'] or 0

        data = {
            "total_capacity": total_capacity,
            "remaining_capacity": total_capacity - total_issued
        }
        return Response(data)


# restaurant/views.py

# ... سایر import ها
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_list_or_404, get_object_or_404
from weasyprint import HTML, CSS
from django.conf import settings
import os


# ... ویوهای قبلی شما ...

class PrintReceiptView(APIView):
    """
    این ویو یک رسید PDF برای یک کد پیگیری مشخص تولید می‌کند.
    """

    def get(self, request, tracking_code):
        # دریافت تمام ژتون‌های مرتبط با این کد پیگیری
        # استفاده از get_list_or_404 برای اطمینان از وجود حداقل یک ژتون
        coupons = get_list_or_404(Coupon, tracking_code=tracking_code)

        # اطلاعات برای همه ژتون‌های یک گروه یکسان است، پس از اولین مورد استفاده می‌کنیم
        first_coupon = coupons[0]
        context = {
            'family_name': first_coupon.family_name,
            'tracking_code': first_coupon.tracking_code,
            'issue_date': first_coupon.issue_date,
            'items': coupons,  # لیست تمام غذاها و تعدادشان
        }

        # رندر کردن قالب HTML به یک رشته
        html_string = render_to_string('receipt.html', context)

        # پیدا کردن مسیر فایل‌های استاتیک برای WeasyPrint
        # این به WeasyPrint کمک می‌کند تا لوگو و فونت را پیدا کند
        base_url = request.build_absolute_uri('/')

        # تبدیل رشته HTML به PDF
        pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

        # ساخت پاسخ HTTP با محتوای PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="receipt-{tracking_code}.pdf"'

        return response