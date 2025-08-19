from django.contrib import admin
from django.db import models

from .models import (
    Category, RawMaterial, SizeOption, Food, FoodRawMaterial, FoodBOMItem,
    WeeklyProgram, KitchenTask, KitchenInventoryItem, WarehouseInventoryItem,
    loginToAddFoodPage, WeeklySchedule, Coupon, loginToCupon, rwmat, servedfood, loginTokitchen,
    # مطمئن شوید که تمام مدل‌ها در فایل models.py شما وجود دارند.
)

from django_jalali.db import models as jmodels

from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date.widgets import AdminJalaliDateWidget


# ---------- Category ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('id',)


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    # 'unit_price' جایگزین 'current_stock' شد.
    list_display = ('name', 'category', 'unit_of_measurement', 'unit_price', 'foods_count')
    list_filter = ('category', 'unit_of_measurement')
    search_fields = ('name', 'description')
    ordering = ('name',)

    def foods_count(self, obj):
        return obj.foodrawmaterial_set.values('food').distinct().count()

    foods_count.short_description = "تعداد غذاهای مرتبط"

    # اکشن مربوط به افزایش موجودی (stock) حذف شد، زیرا فیلد آن در مدل وجود ندارد.
    # actions = ['increase_stock_by_10']


class FoodRawMaterialInline(admin.TabularInline):
    model = FoodRawMaterial
    extra = 1
    raw_id_fields = ('raw_material',)


# کلاس FoodBOMItemInline حذف شد، چون فیلد آن در مدل Food نیست.
# اگر این مدل‌ها همچنان در پروژه شما وجود دارند اما ارتباطشان با Food قطع شده، این کلاس‌ها باید جداگانه مدیریت شوند.


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    # نمایش فیلدهای جدید مدل
    list_display = ('name', 'category', 'food_type', 'preparation_time_minutes', 'raw_materials_count')
    search_fields = ('name', 'description')

    # فیلتر کردن بر اساس فیلدهای جدید
    list_filter = ('category', 'food_type')

    ordering = ('name',)
    inlines = [FoodRawMaterialInline]

    # متدهای مربوط به نمایش فیلدهای حذف‌شده حذف شدند.
    def raw_materials_count(self, obj):
        return obj.foodrawmaterial_set.count()

    raw_materials_count.short_description = "تعداد مواد اولیه"


@admin.register(KitchenInventoryItem)
class KitchenInventoryItemAdmin(admin.ModelAdmin):
    list_display = ('raw_material', 'quantity', 'location')
    list_filter = ('location',)
    search_fields = ('raw_material__name',)
    ordering = ('raw_material__name',)


@admin.register(loginToAddFoodPage)
class LoginToAddFoodPageAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)


admin.site.register(loginToCupon)
admin.site.register(rwmat)
admin.site.register(servedfood)
admin.site.register(KitchenTask)
admin.site.register(WarehouseInventoryItem)
admin.site.register(WeeklyProgram)
admin.site.register(loginTokitchen)


@admin.register(Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('coupon_code', 'food', 'family_name', 'phone_number', 'count', 'issue_date', 'is_used')
    list_filter = ('issue_date', 'food', 'is_used')
    search_fields = ('coupon_code', 'family_name', 'phone_number', 'food__name')
    readonly_fields = ('coupon_code', 'issue_date', 'is_used')
    list_select_related = ('food',)
    jalali_date_fields = ('issue_date',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, jmodels.jDateTimeField):
            kwargs['widget'] = AdminJalaliDateWidget
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
        'food',
        'schedule_date',
        'meal_time',
        'capacity_nazry',
        'capacity_foroshi',
        'cooking_amount',
    )
    readonly_fields = (
        'cooking_amount',
    )
    fields = (
        'food',
        'schedule_date',
        'meal_time',
        'cooking_amount',
        'capacity_nazry',
        'capacity_foroshi',
        'is_finished',
    )
    list_filter = (
        'schedule_date',
        'meal_time',
        'food__name',
    )
    search_fields = (
        'food__name',
        'schedule_date',
        'meal_time'
    )
    list_select_related = ('food',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, jmodels.jDateField):
            kwargs['widget'] = AdminJalaliDateWidget
        elif isinstance(db_field, jmodels.jDateTimeField):
            kwargs['widget'] = AdminJalaliDateWidget
        return super().formfield_for_dbfield(db_field, **kwargs)

    jalali_date_fields = ('schedule_date',)