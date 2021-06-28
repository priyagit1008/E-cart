from django.db import models
import uuid
from django.db import models
from model_utils import Choices
from django.db.models import CharField
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from lib.models import TimeStampedModel
# Create your models here.

class Products(TimeStampedModel):
	"""
	product table 

	"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product_name = models.CharField(max_length=64,null= True, blank=False,default=None)
	price=models.FloatField(max_length=64,null=True,blank=True)

	class Meta:
		app_label = 'products'
		db_table = 'products'




