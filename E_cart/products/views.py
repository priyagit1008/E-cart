from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import ProductRequestSerializer ,ProductListSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .services import ProductServices

from django.conf import settings
from .models import Products
from lib.constants import (
	BAD_REQUEST,
	BAD_ACTION,

)
from lib.exceptions import ParseException
# Create your views here.

class ProductViewSet(GenericViewSet):
	"""
	user class
	"""
	queryset = Products.objects.all()
	services = ProductServices()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'product_add': ProductRequestSerializer,
		'product_list': ProductListSerializer,
		'product_delete':ProductListSerializer
	}

	def get_queryset(self, filterdata=None):
		if filterdata:
			self.queryset = Products.objects.filter(**filterdata)
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
	def product_add(self, request):
		"""
		Returns user Registration
		"""

		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		product= serializer.create(serializer.validated_data)
		if product:
			return Response({"status": "Successfully Registered"}, status=status.HTTP_201_CREATED)
		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
	



	@action(methods=['get', 'patch'],
			detail=False,
			permission_classes=[], )
	def product_delete(self, request):
		"""
		Return user profile data and groups
		"""
		id = request.GET.get('id', None)
		if not id:
			return Response({"status": False, "message": "id is required"})
		try:
			data = self.get_serializer(self.services.get_product(id))
			data.delete()
			return Response({"status":"Successfully Deleted"}, status.HTTP_200_OK)
		except Product.DoesNotExist:
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)

	

	def user_query_string(self, filterdata):

	  dictionary = {}

	  if "product_name" in filterdata:
	      product = filterdata['product_name'].split(',')
	      dictionary["product_name__in"] = product

	  if "price_from" in filterdata:
	      dictionary["price__gte"] = filterdata.pop("price_from")

	  if "price_to" in filterdata:
	      dictionary["price__lte"] = filterdata.pop("price_to")
	      return dictionary

	
	@action(methods=['get'], detail=False, permission_classes=[], )
	def product_list(self, request, **dict):
	  """
	  Return user list
	  """
	  try:
	      filterdata = self.user_query_string(request.query_params.dict())
	      serializer = self.get_serializer(self.get_queryset(filterdata), many=True)

	      return Response(serializer.data)
	  except Products.DoesNotExist:
	      raise
	      return Response({"status": False}, status.HTTP_404_NOT_FOUND)
