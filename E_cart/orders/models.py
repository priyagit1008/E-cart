from django.db import models
import uuid
from model_utils import Choices
from django.db.models import CharField
from django.core.validators import MaxValueValidator,MinValueValidator
from lib.models import TimeStampedModel
from accounts.models import User
# Create your models here.

class Orders(TimeStampedModel):
	"""
	orders table 
	"""
	
	ORDER_STATUS = Choices(

		('Placed', 'PLACED'),
		('Accepted ', 'ACCEPTED'),
		('Canceled', 'CANCELED'),
	)
	order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	customer =  models.ForeignKey(User,on_delete=models.PROTECT,
		related_name='user_customer',blank=True,null=True)
	vendor = models.ForeignKey(User,on_delete=models.PROTECT,
		related_name='user_vendor',blank=True,null=True)
	order_status = models.CharField(max_length=64, 
		choices=ORDER_STATUS,blank=True, default=ORDER_STATUS.Placed)

	class Meta:
		app_label = 'orders'
		db_table = 'orders'
