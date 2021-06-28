from .models import Products


class ProductServices:

    def get_queryset(self,filter_data):
        return Products.objects.filter(**filter_data)

            
    def get_product(self,id):
        return Products.objects.get(id=id)

        
