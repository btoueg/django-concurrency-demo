from .models import Product, Order

from django.views.generic import View
from django.http.response import HttpResponse

class OrderCreate(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product')
        product = Product.objects.get(pk = product_id)
        if not product.stock > 0:
            return HttpResponse("Conflict", status = 409)
        order = Order()
        order.product = product
        order.status = Order.INPROGRESS
        order.save()
        return HttpResponse(order.id, status = 201)

from django.db import transaction

class OrderCancel(View):
    def post(self, request, pk, *args, **kwargs):
        with transaction.commit_manually():
            order = Order.objects.select_for_update(nowait=False).get(pk=pk)
            order.status = Order.ABORTED
            order.save()
            transaction.commit()
        return HttpResponse("Order aborted")
