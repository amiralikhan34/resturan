

from rest_framework import serializers
from .models import (
    Category, RawMaterial, Food, FoodRawMaterial, SizeOption,
    FoodBOMItem, WeeklyProgram, KitchenTask,
    KitchenInventoryItem, WarehouseInventoryItem ,WeeklySchedule , Coupon ,Transaction
)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOption
        fields = '__all__'




class FoodRawMaterialSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    unit_of_measurement = serializers.CharField(source='raw_material.unit_of_measurement', read_only=True)

    class Meta:
        model = FoodRawMaterial
        fields = ['id', 'raw_material', 'raw_material_name', 'quantity_needed', 'unit_of_measurement', 'notes']
        extra_kwargs = {
            'raw_material': {'write_only': True}
        }


class FoodRawMaterialListSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش مواد اولیه در لیست غذاها."""
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    unit_of_measurement = serializers.CharField(source='raw_material.unit_of_measurement', read_only=True)

    class Meta:
        model = FoodRawMaterial
        fields = ['id', 'raw_material_name', 'quantity_needed', 'unit_of_measurement', 'notes']

from rest_framework import serializers
from .models import RawMaterial, Category


class RawMaterialSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = RawMaterial
        # Add 'coding' to the fields
        fields = ['id', 'name', 'category', 'category_name', 'unit_of_measurement', 'unit_price', 'description', 'coding']
    def get_foods_related_count(self, obj):
        return obj.foodrawmaterial_set.values('food').distinct().count()


class FoodListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    raw_materials_count = serializers.SerializerMethodField()
    main_materials = serializers.SerializerMethodField()
    food_type_display = serializers.CharField(source='get_food_type_display', read_only=True)

    # اصلاح: تعریف فیلد food_raw_materials به صورت یک سریالایزر
    food_raw_materials = FoodRawMaterialListSerializer(many=True, read_only=True, source='foodrawmaterial_set')

    class Meta:
        model = Food
        fields = [
            'id', 'name', 'category', 'category_name', 'food_type',
            'food_type_display', 'raw_materials_count', 'main_materials', 'description',
            'food_raw_materials'
        ]

    def get_raw_materials_count(self, obj):
        return obj.foodrawmaterial_set.count()

    def get_main_materials(self, obj):
        # این متد دیگر مورد نیاز نیست، اما برای حفظ ساختار آن را نگه می‌داریم.
        materials = obj.foodrawmaterial_set.all().select_related('raw_material').order_by('id')[:4]
        return [frm.raw_material.name for frm in materials]

class FoodDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    food_raw_materials = FoodRawMaterialSerializer(many=True, required=False)

    class Meta:
        model = Food
        fields = [
            'id', 'name', 'category', 'category_name', 'description', 'food_type',
            'food_raw_materials', 'preparation_time_minutes'
        ]
        read_only_fields = ['category_name']

    def create(self, validated_data):
        materials_data = validated_data.pop('food_raw_materials', [])
        food = Food.objects.create(**validated_data)
        for material_data in materials_data:
            FoodRawMaterial.objects.create(food=food, **material_data)
        return food

    def update(self, instance, validated_data):
        food_raw_materials_data = validated_data.pop('food_raw_materials', [])

        # به‌روزرسانی فیلدهای مدل اصلی
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.food_type = validated_data.get('food_type', instance.food_type)
        instance.preparation_time_minutes = validated_data.get('preparation_time_minutes',
                                                               instance.preparation_time_minutes)
        instance.save()

        # مدیریت مواد اولیه (FoodRawMaterial)
        existing_frm_map = {frm.id: frm for frm in instance.foodrawmaterial_set.all()}
        incoming_frm_ids = []

        for frm_data in food_raw_materials_data:
            frm_id = frm_data.get('id', None)
            if frm_id and frm_id in existing_frm_map:
                # به‌روزرسانی ماده اولیه موجود
                incoming_frm_ids.append(frm_id)
                frm_instance = existing_frm_map[frm_id]
                frm_instance.raw_material = frm_data.get('raw_material', frm_instance.raw_material)
                frm_instance.quantity_needed = frm_data.get('quantity_needed', frm_instance.quantity_needed)
                frm_instance.notes = frm_data.get('notes', frm_instance.notes)
                frm_instance.save()
            else:
                # ایجاد ماده اولیه جدید
                FoodRawMaterial.objects.create(food=instance, **frm_data)

        # حذف مواد اولیه‌ای که در درخواست جدید نیستند
        for frm_id_to_delete in set(existing_frm_map.keys()) - set(incoming_frm_ids):
            FoodRawMaterial.objects.get(id=frm_id_to_delete, food=instance).delete()

        return instance


class FoodBOMItemSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    raw_material_unit = serializers.CharField(source='raw_material.unit_of_measurement', read_only=True)

    class Meta:
        model = FoodBOMItem
        fields = ['id', 'raw_material', 'raw_material_name', 'raw_material_unit', 'quantity']
        extra_kwargs = {
            'raw_material': {'write_only': True}
        }





class WeeklyProgramSerializer(serializers.ModelSerializer):
    main_dish_name = serializers.CharField(source='main_dish.name', read_only=True)
    second_dish_name = serializers.CharField(source='second_dish.name', read_only=True)

    class Meta:
        model = WeeklyProgram
        fields = ['id', 'date', 'day_of_week', 'main_dish', 'main_dish_name', 'second_dish', 'second_dish_name', 'appetizer', 'dessert']




class KitchenTaskSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)

    class Meta:
        model = KitchenTask
        fields = ['id', 'name', 'task_type', 'time', 'date', 'completed', 'food', 'food_name', 'servings_count', 'status']





class KitchenInventoryItemSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    raw_material_unit = serializers.CharField(source='raw_material.unit_of_measurement', read_only=True)

    class Meta:
        model = KitchenInventoryItem
        fields = ['raw_material', 'raw_material_name', 'raw_material_unit', 'quantity', 'location']
        read_only_fields = ['raw_material']




class WeeklyScheduleSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)
    meal_time_display = serializers.CharField(source='get_meal_time_display', read_only=True)

    class Meta:
        model = WeeklySchedule
        fields = [
            'id', 'food', 'food_name', 'schedule_date', 'meal_time', 'meal_time_display',
            'capacity_nazry', 'capacity_foroshi',  'cooking_amount'
        ]



class CouponSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)
    food_category_name = serializers.CharField(source='food.category.name', read_only=True) # برای نمایش دسته بندی غذا

    class Meta:
        model = Coupon
        fields = [
            'id', 'food', 'food_name', 'family_name', 'phone_number',
            'count', 'issue_date', 'coupon_code', 'is_used', 'food_category_name'
        ]
        # فیلدهایی که توسط بک‌اند تولید یا مدیریت می‌شوند
        read_only_fields = ['issue_date', 'coupon_code', 'is_used']


class TransactionSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(source='food_item.name', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    customer_name = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)


    coupon_code = serializers.CharField(source='coupon.coupon_code', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['timestamp', 'coupon']




# serializers.py
from rest_framework import serializers
from .models import Food, WeeklySchedule

class FoodItemWithCapacitySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    remaining_foroshi_capacity = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'name', 'category_name', 'remaining_foroshi_capacity']

    def get_remaining_foroshi_capacity(self, obj):

        meal_time = self.context.get('meal_time', 'lunch')
        today = self.context.get('today', timezone.localdate())

        try:
            schedule = WeeklySchedule.objects.get(
                food=obj,
                schedule_date=today,
                meal_time=meal_time
            )
            return schedule.remaining_foroshi_capacity
        except WeeklySchedule.DoesNotExist:
            return 0


class AvailableFoodSerializer(serializers.ModelSerializer):
    """
    این سریالایزر اطلاعات غذاهای موجود برای یک تاریخ خاص را برمی‌گرداند.
    شامل نام غذا، شناسه و ظرفیت باقی‌مانده نذری است.
    """
    id = serializers.IntegerField(source='food.id')
    name = serializers.CharField(source='food.name')

    # remaining_nazry_capacity یک property در مدل است و به صورت read-only سریالایز می‌شود.

    class Meta:
        model = WeeklySchedule
        fields = ['id', 'name', 'remaining_nazry_capacity']


class CouponItemSerializer(serializers.Serializer):
    """
    این سریالایزر برای اعتبارسنجی هر آیتم غذا در درخواست صدور ژتون است.
    """
    food_id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1)


class MultiCouponIssueSerializer(serializers.Serializer):
    """
    سریالایزر اصلی برای اعتبارسنجی کل درخواست صدور ژتون گروهی.
    """
    family_name = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=20)
    issue_date = serializers.DateField()
    items = serializers.ListField(
        child=CouponItemSerializer(),
        allow_empty=False  # اطمینان از اینکه لیست غذاها خالی نباشد
    )


class WeeklyProgramSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای نمایش برنامه هفتگی.
    """
    name = serializers.CharField(source='food.name', read_only=True)

    class Meta:
        model = WeeklySchedule
        fields = ['name', 'capacity_nazry']