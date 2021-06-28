from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from .models import Orders
from accounts.models import User,UserRole


class OrderRequestSerializer(serializers.ModelSerializer):
    """

    """

    customer= serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    vendor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    order_status=serializers.FloatField(required=False)

    class Meta:
    	model = Orders
    	fields = '__all__'

    def create(self, validated_data):
    	order = Orders.objects.create(**validated_data)
    	return order


class OrderUpdateRequestSerializer(serializers.ModelSerializer):
    customer= serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    vendor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    order_status=serializers.FloatField(required=False)
    

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Orders
        fields = '__all__'


class RoleGetserializers(serializers.ModelSerializer):
    class Meta:
        model =  UserRole
        fields = ('role_name','status')


class CustomerGetSerializer(serializers.ModelSerializer):
    role_name=RoleGetserializers()

    class Meta:
        model = User
        
        fields = ('first_name','last_name','role_name')

class VendorGetSerializer(serializers.ModelSerializer):
    role_name=RoleGetserializers()

    class Meta:
        model = User
        
        fields =('first_name','last_name','role_name')



class OrderListSerializer(serializers.ModelSerializer):

    customer = CustomerGetSerializer()
    vendor =  VendorGetSerializer()

    class Meta:
    	model = Orders
    	fields = ('customer','vendor','order_status')