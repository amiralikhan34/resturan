# restaurant_app/admin.py

from django.contrib import admin
from .models import Category, RawMaterial, Food, FoodRawMaterial, SizeOption

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit_of_measurement', 'current_stock', 'foods_related_count')
    list_filter = ('category', 'unit_of_measurement')
    search_fields = ('name', 'description')
    ordering = ('name',)
    actions = ['add_stock'] # Example custom admin action

    def foods_related_count(self, obj):
        # This will call the method defined in the RawMaterialSerializer for consistency
        return obj.foodrawmaterial_set.values('food').distinct().count()
    foods_related_count.short_description = 'تعداد غذاهای مرتبط'

    # Example custom admin action: Add stock to selected raw materials
    def add_stock(self, request, queryset):
        # For simplicity, let's just add 10 to current_stock for selected items
        # In a real app, you'd likely want a form for quantity input
        for raw_material in queryset:
            raw_material.current_stock += 10
            raw_material.save()
        self.message_user(request, f"{queryset.count()} ماده اولیه با موفقیت به‌روز شد.")
    add_stock.short_description = "افزودن ۱۰ واحد به موجودی انتخاب شده"


class FoodRawMaterialInline(admin.TabularInline):
    model = FoodRawMaterial
    extra = 1 # Number of empty forms to display
    raw_id_fields = ('raw_material',) # Use a raw ID input for raw_material for better performance with many items
    # You might want to prefetch related raw materials if you enable custom form fields for better display in inline

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_available_sizes_display', 'get_raw_materials_count')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    filter_horizontal = ('available_sizes',) # Nice widget for ManyToMany
    inlines = [FoodRawMaterialInline] # Allows managing raw materials directly from Food admin
    ordering = ('name',)

    def get_available_sizes_display(self, obj):
        return ", ".join([size.name for size in obj.available_sizes.all()])
    get_available_sizes_display.short_description = 'سایزهای موجود'

    def get_raw_materials_count(self, obj):
        return obj.foodrawmaterial_set.count()
    get_raw_materials_count.short_description = 'تعداد مواد اولیه'