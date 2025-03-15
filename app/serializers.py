from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


# class CategorySerializer(serializers.ModelSerializer):
#     parent = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), required=False
#     )

#     def to_internal_value(self, data):
#         if isinstance(data.get('parent'), str):
#             try:
#                 data['parent'] = Category.objects.get(name=data['parent']).id
#             except Category.DoesNotExist:
#                 raise serializers.ValidationError({"parent": "Invalid category name"})
#         return super().to_internal_value(data)

#     class Meta:
#         model = Category
#         fields = '__all__'
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name", allow_null=True, required=False
    )

    def to_internal_value(self, data):
        data = data.copy()  # Create a copy to avoid modifying the original
        parent_name = data.get("parent")

        if parent_name and isinstance(parent_name, str):
            try:
                parent_category = Category.objects.get(name=parent_name)
                data["parent"] = parent_category.id
            except Category.DoesNotExist:
                raise serializers.ValidationError({"parent": "Invalid category name"})

        return super().to_internal_value(data)

    class Meta:
        model = Category
        fields = '__all__'

# class CategorySerializer(serializers.ModelSerializer):
#     parent = serializers.SlugRelatedField(
#         queryset=Category.objects.all(), slug_field="name", allow_null=True, required=False
#     )
#     subcategories = serializers.SerializerMethodField()  # Returns subcategories in response

#     def get_subcategories(self, obj):
#         """Fetch subcategories dynamically"""
#         return CategorySerializer(obj.children.all(), many=True).data

#     class Meta:
#         model = Category
#         fields = ["id", "name", "parent", "subcategories"]



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

