from .models import UserRole, User
from django.db.models import Q


class UserServices:

    def get_queryset(self,filter_data):
        return User.objects.filter(**filter_data)

            
    def get_user(self,id):
        return User.objects.get(id=id)
    
    def user_not_exist(self,id,email,mobile):
        return User.objects.filter(~Q(id=id),(Q(email=email)|Q(mobile=mobile))).exists()

        
