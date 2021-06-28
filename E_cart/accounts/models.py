import uuid
from django.db import models
from model_utils import Choices
from django.db.models import CharField
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from lib.models import TimeStampedModel
from .managers import UserManager


# Create your models here.
class UserRole(TimeStampedModel):
	"""
	"""
	
	ROLE = Choices(

		('customer', 'CUSTOMER '),
		('vendor ', 'VENDOR'),
		('admin', 'ADMIN'),
	)
	STATUS = Choices(
		('active', 'ACTIVE'),
		('inactive', 'INACTIVE'),
		)
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	role_name = models.CharField(
		max_length=256,
		choices=ROLE,
		default=ROLE.customer
	)
	status= models.CharField(max_length=64, choices=STATUS,blank=True, default=STATUS.active)


	class Meta:
		app_label = 'accounts'
		db_table = 'user_role'


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
	"""
	User model represents the user data in the database.
	"""
	STATUS = Choices(
		('active', 'ACTIVE'),
		('inactive', 'INACTIVE'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	first_name= models.CharField(max_length=64,null= True, blank=False,default=None)
	last_name=models.CharField(max_length=64,null=True,blank=True)
	email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False,default=None)
	mobile =models.BigIntegerField(
		validators=[
			MinValueValidator(5000000000),
			MaxValueValidator(9999999999),
		],
		unique=True,
		db_index=True,default=None,blank=False)
	role_name=models.ForeignKey(UserRole,on_delete=models.PROTECT,related_name='user_roles',blank=True,null=True)
	status= models.CharField(max_length=64, choices=STATUS,blank=True, default=STATUS.active)
	
	class Meta:
		app_label = 'accounts'
		db_table = 'user'

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['mobile']
	

	@property
	def access_token(self):
		token, is_created = Token.objects.get_or_create(user=self)
		return token.key
	
	@property
	def full_name(self):
		return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)

