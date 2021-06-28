# django imports
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRoleCreateRequestSerializer ,UserRegSerializer,UserRoleListSerializer ,UserListSerializer ,UserLoginRequestSerializer,UserUpdateRequestSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .services import UserServices

from django.conf import settings
from .models import UserRole,User
from lib.constants import (
	BAD_REQUEST,
	BAD_ACTION,

)
from lib.exceptions import ParseException


# Create your views here.

class UserViewSet(GenericViewSet):
	"""
	user class
	"""
	queryset = User.objects.all()
	services = UserServices()

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'register': UserRegSerializer,
		
		'login': UserLoginRequestSerializer,
		'user_list': UserListSerializer,
		'profile': UserListSerializer,
		'profile_update':UserUpdateRequestSerializer
	}

	def get_queryset(self, filterdata=None):
		if filterdata:
			self.queryset = User.objects.filter(**filterdata)
		return self.queryset

	def get_serializer_class(self):
		"""
		Returns serializer class
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[])
	def register(self, request):
		"""
		Returns user Registration
		"""

		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		user = serializer.create(serializer.validated_data)
		if user:
			return Response({"status": "Successfully Registered"}, status=status.HTTP_201_CREATED)
		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['post'], detail=False, permission_classes=[])
	def login(self, request):
		"""
		Return user login
		"""
		serializer = self.get_serializer(data=request.data)

		if not serializer.is_valid():
			raise ParseException(BAD_REQUEST, serializer.errors)

		user = authenticate(
			email=serializer.validated_data["email"],
			password=serializer.validated_data["password"])

		if not user:
			return Response({'status': 'Invalid Credentials'},status=status.HTTP_404_NOT_FOUND)


		token = user.access_token
		name = user.first_name
		id = user.id
		role = user.role_name
		return Response({'token': token, 
						"name": name, 
						'user_id': id,
						'user_role': role.role_name},
						status=status.HTTP_200_OK)

	

	@action(methods=['get', 'patch'],
			detail=False,
			permission_classes=[IsAuthenticated, ], )
	def profile(self, request):
		"""
		Return user profile data and groups
		"""
		id = request.GET.get('id', None)
		if not id:
			return Response({"status": False, "message": "id is required"})
		try:
			serializer = self.get_serializer(self.services.get_user(id))
			return Response(serializer.data, status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
	
	
	@action(methods=['get'], detail=False, permission_classes=[],)
	def user_list(self, request):
		"""
		Return all role data
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)
	

	@action(

		methods=['get', 'put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def profile_update(self, request):
		"""
		Return user update data
		"""
		try:
			user = request.data.copy()

			serializer = self.get_serializer(self.services.update_user(id), data=user)

			if self.services.user_not_exist(id, email, mobile):
				return Response({"status": "User  already exists"}, status=status.HTTP_409_CONFLICT)
			if not serializer.is_valid():

				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			else:
				serializer.save()
				return Response({"status": "updated Successfully"}, status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)


class UserRoleViewSet(GenericViewSet):
	queryset=UserRole.objects.all()

	serializers_dict = {
		'add_userrole': UserRoleCreateRequestSerializer,
		'list_userrole':UserRoleListSerializer,
		}


	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset =UserRole.objects.filter(**filterdata)
		return self.queryset


	def get_serializer_class(self):
		"""
		Returns serilizer class
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)



	@action(methods=['post'], detail=False, permission_classes=[], )
	def add_userrole(self, request):
		"""
		Returns add user role
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			raise ParseException(BAD_REQUEST, serializer.errors)
		user_role = serializer.create(serializer.validated_data)
		if user_role:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[],)
	def list_userrole(self, request):
		"""
		Return all role data
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)
	
