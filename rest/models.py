

from django.db import models
from django.db import models
from django_jalali.db import models as jmodels
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from django.core.validators import MinValueValidator
from datetime import timedelta
import jdatetime

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name


# In your models.py

class RawMaterial(models.Model):
    UNIT_CHOICES = [
        ('gram', 'گرم'),
        ('kg', 'کیلوگرم'),
        ('milliliter', 'میلی لیتر'),
        ('liter', 'لیتر'),
        ('piece', 'عدد'),
    ]

    name = models.CharField(max_length=200, unique=True, verbose_name="نام ماده اولیه")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='raw_materials', verbose_name="دسته‌بندی")
    unit_of_measurement = models.CharField(max_length=50, choices=UNIT_CHOICES, verbose_name="واحد اندازه‌گیری")

    # --- ADD THIS FIELD ---
    current_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="موجودی انبار اصلی"
    )
    # --------------------

    unit_price = models.DecimalField(max_digits=15, decimal_places=0, default=0, help_text="قیمت واحد به ریال")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    coding = models.CharField(max_length=100, blank=True, null=True, verbose_name="کدینگ")

    class Meta:
        verbose_name = "ماده اولیه"
        verbose_name_plural = "مواد اولیه"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_unit_of_measurement_display()})"

class SizeOption(models.Model):

    name = models.CharField(max_length=50, unique=True, verbose_name="نام سایز")

    class Meta:
        verbose_name = "گزینه سایز"
        verbose_name_plural = "گزینه‌های سایز"
        ordering = ['id']

    def __str__(self):
        return self.name


# app_name/models.py




class Food(models.Model):
    # گزینه‌های از پیش تعریف‌شده برای نوع غذا
    FOOD_TYPE_CHOICES = [
        ('main', 'غذای اصلی'),
        ('appetizer', 'پیش غذا'),
        ('dessert', 'دسر'),
    ]

    name = models.CharField(max_length=200, verbose_name="نام غذا")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='foods',
                                 verbose_name="دسته‌بندی")

    # فیلد جدید برای نوع غذا
    food_type = models.CharField(
        max_length=10,
        choices=FOOD_TYPE_CHOICES,
        default='main',
        verbose_name="نوع غذا"
    )

    # فیلدهای باقی‌مانده
    preparation_time_minutes = models.IntegerField(null=True, blank=True, verbose_name="زمان آماده‌سازی (دقیقه)")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    is_finish = models.BooleanField(default=False, verbose_name="تمام شده است؟")

    # فیلدهای حذف‌شده: available_sizes, dayOnWeek, time, ghazaye_asly, pish_ghaza, deser

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذاها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_raw_materials_count(self):
        return self.foodrawmaterial_set.count()
    get_raw_materials_count.short_description = 'تعداد مواد اولیه'

class FoodRawMaterial(models.Model):

    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="غذا")
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, verbose_name="ماده اولیه")
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار لازم")
    notes = models.CharField(max_length=255, blank=True, null=True, verbose_name="توضیحات")






    class Meta:
        verbose_name = "ماده اولیه غذا"
        verbose_name_plural = "مواد اولیه غذا"
        unique_together = ('food', 'raw_material')
        ordering = ['raw_material__name']

    def __str__(self):
        return f"{self.food.name} - {self.raw_material.name} ({self.quantity_needed} {self.raw_material.unit_of_measurement})"








class loginToAddFoodPage(models.Model):
    username = models.CharField(max_length=200 )
    password = models.CharField(max_length=200 )









from django.db import models
from django.utils import timezone

class RawMaterial2(models.Model):

    name = models.CharField(max_length=255, unique=True, verbose_name="نام ماده")
    unit = models.CharField(max_length=50, verbose_name="واحد") # e.g., "کیلوگرم", "عدد", "قاشق چایخوری", "لیتر"

    class Meta:
        verbose_name = "ماده اولیه"
        verbose_name_plural = "مواد اولیه"

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Food2(models.Model):

    name = models.CharField(max_length=255, unique=True, verbose_name="نام غذا")
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name="دسته بندی") # e.g., "غذای اصلی", "خورشت"
    preparation_time_minutes = models.IntegerField(null=True, blank=True, verbose_name="زمان آماده‌سازی (دقیقه)")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذاها"

    def __str__(self):
        return self.name

class FoodBOMItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='bom_items', verbose_name="غذا")
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, verbose_name="ماده اولیه")
    quantity = models.FloatField(verbose_name="مقدار")

    class Meta:
        unique_together = ('food', 'raw_material')
        verbose_name = "ماده اولیه (BOM)"
        verbose_name_plural = "مواد اولیه (BOM)"

    def __str__(self):
        return f"{self.food.name}: {self.quantity} {self.raw_material.unit_of_measurement} of {self.raw_material.name}"


class WeeklyProgram(models.Model):

    date = models.DateField(unique=True, verbose_name="تاریخ")
    day_of_week = models.CharField(max_length=20, verbose_name="روز هفته") # e.g., "شنبه", "یکشنبه"
    main_dish = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_dish_weekly_programs', verbose_name="غذای اصلی")
    second_dish = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_dish_weekly_programs', verbose_name="غذای دوم")
    appetizer = models.CharField(max_length=255, null=True, blank=True, verbose_name="پیش غذا")
    dessert = models.CharField(max_length=255, null=True, blank=True, verbose_name="دسر")

    class Meta:
        verbose_name = "برنامه هفتگی"
        verbose_name_plural = "برنامه‌های هفتگی"
        ordering = ['date']

    def __str__(self):
        return f"برنامه هفتگی {self.day_of_week} ({self.date})"

class KitchenTask(models.Model):

    TASK_TYPES = [
        ('preparation', 'آماده‌سازی'),
        ('cooking', 'پخت'),
        ('serving', 'سرو'),
        ('cleaning', 'نظافت'),
        ('other', 'سایر'),
    ]
    name = models.CharField(max_length=255, verbose_name="نام وظیفه")
    task_type = models.CharField(max_length=50, choices=TASK_TYPES, verbose_name="نوع وظیفه")
    time = models.TimeField(verbose_name="زمان")
    date = models.DateField(default=timezone.now, verbose_name="تاریخ")
    completed = models.BooleanField(default=False, verbose_name="تکمیل شده")

    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True, related_name='serving_tasks', verbose_name="غذای مرتبط (در صورت وجود)")
    servings_count = models.IntegerField(null=True, blank=True, verbose_name="تعداد سرو")

    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('in_progress', 'در حال انجام'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")


    class Meta:
        verbose_name = "وظیفه آشپزخانه"
        verbose_name_plural = "وظایف آشپزخانه"
        ordering = ['date', 'time']

    def __str__(self):
        return f"وظیفه {self.name} در {self.date} {self.time} ({self.get_task_type_display()})"

class KitchenInventoryItem(models.Model):

    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, unique=True, verbose_name="ماده اولیه")
    quantity = models.FloatField(verbose_name="موجودی")
    location = models.CharField(max_length=100, verbose_name="محل نگهداری") # e.g., "یخچال ۱", "قفسه سبزیجات"


    class Meta:
        verbose_name = "موجودی انبار آشپزخانه"
        verbose_name_plural = "موجودی انبار آشپزخانه"
        ordering = ['raw_material__name']

    def __str__(self):
        return f"موجودی آشپزخانه: {self.raw_material.name} - {self.quantity} {self.raw_material.unit}"

class WarehouseInventoryItem(models.Model):

    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, unique=True, verbose_name="ماده اولیه")
    quantity = models.FloatField(verbose_name="موجودی")
    min_quantity = models.FloatField(default=0, verbose_name="حداقل موجودی")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="تاریخ انقضا")
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name="دسته‌بندی (کالا)")

    class Meta:
        verbose_name = "موجودی انبار اصلی"
        verbose_name_plural = "موجودی انبار اصلی"
        ordering = ['raw_material__name']

    def __str__(self):
        return f"موجودی انبار: {self.raw_material.name} - {self.quantity} {self.raw_material.unit}"



class rwmat(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام ماده")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="مقدار")
    unit = models.CharField(max_length=50, verbose_name="واحد")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ماده اولیه"
        verbose_name_plural = "مواد اولیه"

    def __str__(self):
        return self.name




class loginTokitchen(models.Model):
    username = models.CharField(max_length=200 )
    password= models.CharField(max_length=200 )




class servedfood(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام غذا")
    preparation_time_minutes = models.IntegerField(null=True, blank=True, verbose_name="زمان آماده‌سازی (دقیقه)")
    tedad = models.IntegerField(null=True, blank=True, verbose_name="تعداد سرو")
    is_finish = models.BooleanField(default=False)



    def __str__(self):
        return self.name



# models.py

import jdatetime
from django.db import models
from django_jalali.db import models as jmodels

# ... (احتمالا مدل Food شما اینجا تعریف شده)
# class Food(models.Model):
#     ...

class Coupon(models.Model):
    # فیلدهای اصلی
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='coupons', verbose_name="غذا")
    family_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تماس")
    count = models.IntegerField(default=1, verbose_name="تعداد")
    coupon_code = models.CharField(max_length=100, unique=True, verbose_name="کد ژتون")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده")

    # --- تغییرات اصلی اینجا هستند ---

    # ۱. فیلد تاریخ صدور اصلاح شد
    # auto_now_add حذف شد تا بتوانیم تاریخ را دستی وارد کنیم
    # به jDateField تغییر کرد چون فقط به تاریخ نیاز داریم نه زمان
    issue_date = jmodels.jDateField(verbose_name="تاریخ صدور", default=jdatetime.date.today)

    # ۲. فیلدهای جا افتاده اضافه شدند
    coupon_type = models.CharField(max_length=50, default='nazry', verbose_name="نوع ژتون")
    tracking_code = models.CharField(max_length=10, verbose_name="ژتون")


    class Meta:
        verbose_name = "ژتون"
        verbose_name_plural = "ژتون‌ها"
        ordering = ['-issue_date']

    def __str__(self):
        return f"ژتون {self.food.name} - {self.coupon_code}"




class loginToCupon(models.Model):
    username = models.CharField(max_length=200 )
    password= models.CharField(max_length=200 )


from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class WeeklySchedule(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="غذا")

    # --- تغییر کلیدی اینجاست ---
    schedule_date = models.DateField(verbose_name="تاریخ برنامه")

    meal_time = models.CharField(max_length=50, verbose_name="وعده غذایی",
                                 choices=[
                                     ('breakfast', 'صبحانه'),
                                     ('lunch', 'ناهار'),
                                     ('dinner', 'شام'),
                                     ('snack', 'میان وعده')
                                 ])

    capacity_nazry = models.IntegerField(blank=True, null=True, verbose_name="ظرفیت حضرتی")
    capacity_foroshi = models.IntegerField(blank=True, null=True, verbose_name="ظرفیت فروشی")

    issued_nazry_count = models.IntegerField(default=0, validators=[MinValueValidator(0)],
                                             verbose_name="تعداد حضرتی صادر شده")
    issued_foroshi_count = models.IntegerField(default=0, validators=[MinValueValidator(0)],
                                               verbose_name="تعداد فروشی صادر شده")

    cooking_amount = models.IntegerField(blank=True, null=True, verbose_name="مقدار طبخ")
    is_finished = models.BooleanField(default=False, verbose_name="اتمام")

    class Meta:
        verbose_name = "برنامه هفتگی"
        verbose_name_plural = "برنامه هفتگی غذاها"
        # در unique_together هم از فیلد جدید استفاده می‌کنیم
        unique_together = ('food', 'schedule_date', 'meal_time')
        ordering = ['schedule_date', 'meal_time']

    # بقیه متدها مثل __str__ و properties بدون تغییر باقی می‌مانند
    def __str__(self):
        # نمایش تاریخ شمسی در پنل ادمین
        try:
            import jdatetime
            jalali_date = jdatetime.date.fromgregorian(date=self.schedule_date)
            return f"{self.food.name} - {jalali_date.strftime('%Y/%m/%d')} ({self.get_meal_time_display()})"
        except (ImportError, TypeError):
            return f"{self.food.name} - {self.schedule_date} ({self.get_meal_time_display()})"

    @property
    def remaining_nazry_capacity(self):
        total_capacity = self.capacity_nazry if self.capacity_nazry is not None else 0
        return total_capacity - self.issued_nazry_count

    @property
    def remaining_foroshi_capacity(self):
        total_capacity = self.capacity_foroshi if self.capacity_foroshi is not None else 0
        return total_capacity - self.issued_foroshi_count

    def clean(self):
        super().clean()

        if self.cooking_amount is not None:
            if self.capacity_nazry is not None and self.capacity_nazry > self.cooking_amount:
                raise ValidationError({
                    'capacity_nazry': 'ظرفیت حضرتی نمی‌تواند بیشتر از مقدار طبخ باشد.'
                })
            if self.capacity_foroshi is not None and self.capacity_foroshi > self.cooking_amount:
                raise ValidationError({
                    'capacity_foroshi': 'ظرفیت فروشی نمی‌تواند بیشتر از مقدار طبخ باشد.'
                })

    @property
    def persian_day_of_week(self):
        """نام فارسی روز هفته را برمی‌گرداند"""
        if not self.schedule_date:
            return ""

        days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
        # jdatetime.fromgregorian weekday() -> شنبه=0, یکشنبه=1, ...
        jalali_date = jdatetime.date.fromgregorian(date=self.schedule_date)
        return days[jalali_date.weekday()]



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('direct_sale', 'فروش مستقیم'),
        ('token_delivery', 'تحویل با ژتون'),
    )


    customer_name = models.CharField(max_length=255, verbose_name="نام مشتری")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تماس")
    food_item = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, verbose_name="غذا")
    quantity = models.IntegerField(verbose_name="تعداد")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="نوع تراکنش")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان تراکنش")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ژتون مرتبط") # اگر تراکنش از نوع ژتون است

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-timestamp'] # نمایش از جدیدترین به قدیمی‌ترین

    def __str__(self):
        return f"{self.customer_name} - {self.food_item.name if self.food_item else 'N/A'} ({self.quantity}) - {self.get_transaction_type_display()}"





class loginToTahvil(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    class Meta:
        verbose_name = "کاربر پنل تحویل"
        verbose_name_plural = "کاربران پنل تحویل"

    def __str__(self):
        return self.username
