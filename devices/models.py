from django.db import models

class Sector(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    power_level = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    def __str__(self):
        return self.name

class Price(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return "%s - %s" % (self.time, self.price)

class PowerConsumption(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    datetime = models.TimeField()
    power_consumed = models.DecimalField(max_digits=6, decimal_places=3)
    cost = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    
    class Meta:
        unique_together = (('device'), ('datetime'))
    def __str__(self):
        return "%s: %s | %s" % (self.device, self.power_consumed, self.datetime)

class SectorConsumption(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    datetime = models.TimeField()
    power_consumed = models.DecimalField(max_digits=6, decimal_places=3)
    cost = models.DecimalField(max_digits=6, decimal_places=3, null=True)

