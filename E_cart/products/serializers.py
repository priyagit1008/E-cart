from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from django.core.validators import validate_email
from .models import Products


class ProductRequestSerializer(serializers.ModelSerializer):
    """

    """

    product_name = serializers.CharField(required=True)
    price = serializers.FloatField(required=False)

    class Meta:
    	model = Products
    	fields = '__all__'

    def create(self, validated_data):
    	product = Products.objects.create(**validated_data)
    	return product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Products
    	fields = '__all__'

