from .models import Orders


class OrderServices:

    # def get_queryset(self,filter_data):
    #     return Orders.objects.filter(**filter_data)

            
    def update_order(self,id):
        return Orders.objects.get(id=id)

        
