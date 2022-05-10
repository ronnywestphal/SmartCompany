from django.db import models

# Create your models here.
'''class Price(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return "%s - %s" % (self.time, self.price)
'''
class Price_week(models.Model):
    date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return "%s - %s" % (self.date, self.price)