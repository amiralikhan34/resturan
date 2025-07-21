# restaurant_app/models.py

from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name'] # Optional: order by name by default

    def __str__(self):
        return self.name

class RawMaterial(models.Model):

    UNIT_CHOICES = [
        ('gram', 'گرم'),
        ('kg', 'کیلوگرم'),
        ('milliliter', 'میلی لیتر'),
        ('liter', 'لیتر'),
        ('piece', 'عدد'),
    ]

    name = models.CharField(max_length=200, unique=True, verbose_name="نام ماده اولیه")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='raw_materials', verbose_name="دسته‌بندی")
    unit_of_measurement = models.CharField(max_length=50, choices=UNIT_CHOICES, verbose_name="واحد اندازه‌گیری")
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="موجودی فعلی")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    # You might consider adding a 'min_stock' or 'max_stock' for progress bar calculations

    class Meta:
        verbose_name = "ماده اولیه"
        verbose_name_plural = "مواد اولیه"
        ordering = ['name'] # Optional: order by name by default

    def __str__(self):
        return f"{self.name} ({self.unit_of_measurement})"

class SizeOption(models.Model):

    name = models.CharField(max_length=50, unique=True, verbose_name="نام سایز")

    class Meta:
        verbose_name = "گزینه سایز"
        verbose_name_plural = "گزینه‌های سایز"
        ordering = ['id'] # Order by ID or a specific order if defined

    def __str__(self):
        return self.name

class Food(models.Model):

    name = models.CharField(max_length=200, unique=True, verbose_name="نام غذا")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='foods', verbose_name="دسته‌بندی")
    available_sizes = models.ManyToManyField('SizeOption', verbose_name="سایزهای موجود")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذاها"
        ordering = ['name'] # Optional: order by name by default

    def __str__(self):
        return self.name

    def get_raw_materials_count(self):
        return self.foodrawmaterial_set.count()
    get_raw_materials_count.short_description = 'تعداد مواد اولیه' # For Django Admin

class FoodRawMaterial(models.Model):

    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="غذا")
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, verbose_name="ماده اولیه")
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار لازم")
    notes = models.CharField(max_length=255, blank=True, verbose_name="توضیحات خاص")

    class Meta:
        verbose_name = "ماده اولیه غذا"
        verbose_name_plural = "مواد اولیه غذا"
        unique_together = ('food', 'raw_material')
        ordering = ['raw_material__name']

    def __str__(self):
        return f"{self.food.name} - {self.raw_material.name} ({self.quantity_needed} {self.raw_material.unit_of_measurement})"