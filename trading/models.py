from django.db import models


class Trade(models.Model):
    owner = models.IntegerField()
    is_active = models.BooleanField(default=True)
    sell = models.IntegerField()
    buy = models.IntegerField()
    quantity = models.DecimalField(max_digits=19, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    participant = models.IntegerField(blank=True)
