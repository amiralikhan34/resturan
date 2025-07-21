from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from .models import Category, RawMaterial, Food, FoodRawMaterial, SizeOption
from .serializers import (
    CategorySerializer,
    RawMaterialSerializer,
    FoodListSerializer,
    FoodDetailSerializer,
    SizeOptionSerializer,
    FoodRawMaterialSerializer
)


def frontend_app_view(request):


    return render(request, 'redt1.html')


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


@api_view(['GET', 'POST'])
@csrf_exempt # اضافه شدن csrf_exempt برای POST
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
    raw_material = get_object_or_404(RawMaterial, pk=pk)

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
        queryset = Food.objects.all().select_related('category').prefetch_related('available_sizes',
                                                                                  'foodrawmaterial_set__raw_material')

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

    top_consumed_materials = FoodRawMaterial.objects.values('raw_material__name', 'raw_material__unit_of_measurement') \
                                 .annotate(total_needed=Sum('quantity_needed')) \
                                 .order_by('-total_needed')[:3]

    stock_status_data = []
    for rm in RawMaterial.objects.all():
        # اصلاح: تبدیل hypothetical_max_stock به Decimal برای جلوگیری از خطای TypeError
        hypothetical_max_stock = Decimal('30.0') # <-- این خط را تغییر دادم
        percentage = (rm.current_stock / hypothetical_max_stock) * 100 if hypothetical_max_stock > 0 else 0

        status_color = "green"
        if percentage < Decimal('30'): # مقایسه با Decimal
            status_color = "red"
        elif percentage < Decimal('70'): # مقایسه با Decimal
            status_color = "orange"

        stock_status_data.append({
            "name": f"{rm.name} ({rm.current_stock} {rm.unit_of_measurement})",
            "current_stock_value": float(rm.current_stock),
            "unit": rm.unit_of_measurement,
            "percentage": round(percentage),
            "status": status_color
        })

    stock_status_data.sort(key=lambda x: x['percentage'], reverse=True)

    example_food_structure = []
    try:
        chello_kabob = Food.objects.get(name="چلو کباب کوبیده")  # Assuming this food exists
        frm_queryset = chello_kabob.foodrawmaterial_set.all().select_related('raw_material')
        example_food_structure = [
            {
                "quantity": f"{frm.quantity_needed} {frm.raw_material.unit_of_measurement}",
                "description": f"{frm.raw_material.name} {frm.notes if frm.notes else ''}".strip()
            }
            for frm in frm_queryset
        ]
    except Food.DoesNotExist:
        pass

    data = {
        "total_categories": total_categories,
        "total_raw_materials": total_raw_materials,
        "total_foods": total_foods,
        "top_consumed_materials": list(top_consumed_materials),
        "stock_status": stock_status_data,
        "example_food_structure": example_food_structure,
    }
    return Response(data)