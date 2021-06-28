from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import OrderRequestSerializer ,OrderListSerializer,OrderUpdateRequestSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
# from .services import ProductServices

from django.conf import settings
from .models import Orders
from lib.constants import (
	BAD_REQUEST,
	BAD_ACTION,

)
from lib.exceptions import ParseException
# Create your views here.
class OrderViewSet(GenericViewSet):
	"""
	user class
	"""
	queryset = Orders.objects.all().order_by('-created_at')
	# services = ProductServices()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'order_add': OrderRequestSerializer,
		'order_list': OrderListSerializer,
		'order_update':OrderUpdateRequestSerializer
	}

	def get_queryset(self, filterdata=None):
		if filterdata:
			self.queryset = Orders.objects.filter(**filterdata)
		return self.queryset

	def get_serializer_class(self):
		"""
		Returns serializer class
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'],
	    detail=False, 
	    permission_classes=[IsAuthenticated])

	def order_add(self, request):
		"""
		Returns order
		"""

		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		order= serializer.create(serializer.validated_data)
		if order:
			return Response({"status": "Successfully order placed"}, status=status.HTTP_201_CREATED)
		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
	

	@action(methods=['get'], detail=False, permission_classes=[],)
	def order_list(self, request):
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
	def order_update(self, request):
		"""
		Return user update data
		"""
		try:
			order = request.data.copy()

			serializer = self.get_serializer(self.services.update_order(id), data=order)
			if not serializer.is_valid():

				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			else:
				serializer.save()
				return Response({"status": "order updated Successfully"}, status.HTTP_200_OK)
		except Orders.DoesNotExist:
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
