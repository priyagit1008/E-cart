from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    """
    TimeStampedModel is an abstract model to add following fields in every
    model where it is inherited.
      - is_active
      - created_at
      - updated_at
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True