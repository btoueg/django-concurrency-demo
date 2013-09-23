from rest_framework import generics
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status

from .models import Order

class ConflictWithAnotherRequest(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Assuming expired database state."

    def __init__(self, detail=None):
        self.detail = (detail or self.default_detail)

class OrderSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'product',
            'status',
        )
        read_only_fields = (
            'status',
        )


class OrderList(generics.ListCreateAPIView):
    model = Order
    serializer_class = OrderSimpleSerializer

    def pre_save(self, obj):
        super(OrderList,self).pre_save(obj)
        product = obj.product
        if not product.stock > 0:
            raise ConflictWithAnotherRequest("Product is not available anymore.")
        obj.status = Order.INPROGRESS


class OrderDetail(generics.RetrieveUpdateAPIView):
    model = Order

class OrderAbort(generics.RetrieveUpdateAPIView):
    model = Order
    serializer_class = OrderSimpleSerializer

    def pre_save(self, obj):
        obj.status = Order.ABORTED
