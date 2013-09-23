from django.db import models
from django.db.models import F

class Product(models.Model):
    name = models.CharField(max_length=30)
    stock = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey('Product')
    DRAFT = 'DR'; INPROGRESS = 'PR'; ABORTED = 'AB'
    STATUS = (
        (INPROGRESS, 'In progress'),
        (ABORTED, 'Aborted'),
    )
    status = models.CharField(max_length = 2, choices = STATUS, default = DRAFT)
    EXISTING_STATUS = set([INPROGRESS])

    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_status = self.status
        print(self.__original_status)

    def save(self, *args, **kwargs):
        old_status = self.__original_status
        new_status = self.status
        has_changed_status = old_status != new_status
        if has_changed_status:
            product = Product.objects.select_for_update(nowait=True).get(pk=self.product.pk)
            if not old_status in Order.EXISTING_STATUS and new_status in Order.EXISTING_STATUS:
                product.stock = F('stock') - 1
                product.save(update_fields=['stock'])
            elif old_status in Order.EXISTING_STATUS and not new_status in Order.EXISTING_STATUS:
                product.stock = F('stock') + 1
                product.save(update_fields=['stock'])
        super(Order, self).save(*args, **kwargs)
        self.__original_status = self.status

    def __str__(self):
        return self.status
