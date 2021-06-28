from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from django.core.validators import validate_email
from .models import UserRole,User
	

class UserLoginRequestSerializer(serializers.ModelSerializer):
    """
    UserLoginSerializer
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'access_token')


class UserRegSerializer(serializers.Serializer):    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=False, min_length=5)
    mobile = serializers.IntegerField(required=True)
    role_name = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all(),required=False)
    status = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = '__all__'

        # fields = ('id', 'email', 'first_name', 'last_name', 'mobile','status')
        # write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        print(user)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRoleGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        
        fields = ('role_name','status')

class UserListSerializer(serializers.ModelSerializer):
    role_name = UserRoleGetSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'mobile','status','role_name')


class UserUpdateRequestSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=False, min_length=5)
    mobile = serializers.IntegerField(required=True)
    role_name = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all(),required=False)
    status = serializers.CharField(required=False)
    

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'

class UserRoleCreateRequestSerializer(serializers.Serializer):
	"""
	UserRoleSerializer
	"""
	role_name = serializers.CharField(required=True)

	class Meta:
		model = UserRole
		fields = (
			'id','role_name','status'
		)


	def create(self,validated_data):
		userrole = UserRole.objects.create(**validated_data)
		return userrole

class UserRoleListSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserRole
		fields = (
			'id','role_name','status'
		)
