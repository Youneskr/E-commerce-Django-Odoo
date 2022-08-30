from django.db import models

class OrderItem(models.Model):
    client_id = models.IntegerField(null=True, blank=True)
    product_id = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return f'Client id : {self.client_id} | Product id : {self.product_id}'