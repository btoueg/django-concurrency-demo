from django.db import models, transaction
from django.db.models import F
from time import sleep

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

    def save(self, *args, **kwargs):
        if self.status == "AB": # If status == AB, check products we need to update
            with transaction.commit_manually():
                updated_product = Product.objects.filter(order__pk = self.pk, order__status = 'PR').update(stock = F('stock') + 1 )
                sleep(1) # To have some fun
                if updated_product == 1:
                    super(Order, self).save(*args, **kwargs)
                    transaction.commit()
                    return # Everthing OK
                else:
                    # Product had already been decremented
                    transaction.rollback() # Nothing have been done anyway


        # Globalement tu devrais éviter les changements de status dans les deux sens. Creez un nouvel Order si l'ancien a été Aborted
        if self.id is None: # self.status in Order.EXISTING_STATUS:
            Product.objects.filter(pk = self.product.pk).update(stock = F('stock') + 1 )
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.status
