from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"



class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
