# restaurant_app/serializers.py

from rest_framework import serializers
from django.db.models import Sum
from .models import Category, RawMaterial, Food, FoodRawMaterial, SizeOption

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' # ['id', 'name']

class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOption
        fields = '__all__' # ['id', 'name']

class FoodRawMaterialSerializer(serializers.ModelSerializer):
    # To display raw material name and unit when reading
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    unit_of_measurement = serializers.CharField(source='raw_material.unit_of_measurement', read_only=True)

    class Meta:
        model = FoodRawMaterial
        fields = ['id', 'raw_material', 'raw_material_name', 'quantity_needed', 'unit_of_measurement', 'notes']
        # 'raw_material' field (PK of RawMaterial) is for writing (POST/PUT)
        # 'raw_material_name' and 'unit_of_measurement' are for display (GET)
        extra_kwargs = {
            'raw_material': {'write_only': True} # This makes 'raw_material' input-only
        }


class RawMaterialSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    foods_related_count = serializers.SerializerMethodField() # Custom field for related foods count

    class Meta:
        model = RawMaterial
        fields = ['id', 'name', 'category', 'category_name', 'unit_of_measurement', 'current_stock', 'description', 'foods_related_count']

    def get_foods_related_count(self, obj):
        # Counts the number of distinct foods this raw material is linked to
        return obj.foodrawmaterial_set.values('food').distinct().count()


class FoodListSerializer(serializers.ModelSerializer):
    # Used for listing foods, showing summary info
    category_name = serializers.CharField(source='category.name', read_only=True)
    available_sizes = SizeOptionSerializer(many=True, read_only=True)
    raw_materials_count = serializers.SerializerMethodField()
    main_materials = serializers.SerializerMethodField() # To show limited main materials

    class Meta:
        model = Food
        fields = ['id', 'name', 'category', 'category_name', 'available_sizes', 'raw_materials_count', 'main_materials', 'description']

    def get_raw_materials_count(self, obj):
        return obj.foodrawmaterial_set.count()

    def get_main_materials(self, obj):
        # Return names of the first few raw materials for display, e.g., max 4
        materials = obj.foodrawmaterial_set.all().select_related('raw_material').order_by('id')[:4]
        return [frm.raw_material.name for frm in materials]


class FoodDetailSerializer(serializers.ModelSerializer):
    # Used for creating/updating foods, with nested raw materials
    category_name = serializers.CharField(source='category.name', read_only=True)
    # For available_sizes, we want to write using IDs and read using names
    available_sizes = serializers.PrimaryKeyRelatedField(queryset=SizeOption.objects.all(), many=True)
    food_raw_materials = FoodRawMaterialSerializer(many=True, source='foodrawmaterial_set', required=False) # Nested serializer

    class Meta:
        model = Food
        fields = ['id', 'name', 'category', 'category_name', 'description', 'available_sizes', 'food_raw_materials']

    def create(self, validated_data):
        # Handle ManyToMany for available_sizes
        available_sizes_data = validated_data.pop('available_sizes')
        # Handle nested FoodRawMaterial data
        food_raw_materials_data = validated_data.pop('foodrawmaterial_set', []) # Default to empty list if not provided

        food = Food.objects.create(**validated_data)
        food.available_sizes.set(available_sizes_data) # Set ManyToMany relation

        for frm_data in food_raw_materials_data:
            FoodRawMaterial.objects.create(food=food, **frm_data)
        return food

    def update(self, instance, validated_data):
        # Update scalar fields of Food
        for attr, value in validated_data.items():
            if attr not in ['available_sizes', 'foodrawmaterial_set']: # Exclude nested fields from direct update
                setattr(instance, attr, value)
        instance.save()

        # Update ManyToMany for sizes
        available_sizes_data = validated_data.get('available_sizes')
        if available_sizes_data is not None:
            instance.available_sizes.set(available_sizes_data)

        # Update nested FoodRawMaterial
        food_raw_materials_data = validated_data.get('foodrawmaterial_set')
        if food_raw_materials_data is not None:
            # Get existing IDs for updating/deleting
            existing_frm_map = {frm.id: frm for frm in instance.foodrawmaterial_set.all()}
            incoming_frm_ids = []

            for frm_data in food_raw_materials_data:
                frm_id = frm_data.get('id', None)
                if frm_id and frm_id in existing_frm_map: # Existing material - update
                    incoming_frm_ids.append(frm_id)
                    frm_instance = existing_frm_map[frm_id]
                    for attr, value in frm_data.items():
                        if attr != 'id':
                            setattr(frm_instance, attr, value)
                    frm_instance.save()
                else: # New material - create (id will be None or not in existing map)
                    FoodRawMaterial.objects.create(food=instance, **frm_data)

            # Delete materials that are no longer in the incoming data
            for frm_id_to_delete in set(existing_frm_map.keys()) - set(incoming_frm_ids):
                FoodRawMaterial.objects.get(id=frm_id_to_delete, food=instance).delete()

        return instance