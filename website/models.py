from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BusinessType(models.Model):
    business_type = models.CharField(max_length=50, name='type', unique=True)

    def __str__(self):
        return self.business_type


class Business(models.Model):
    name = models.CharField(max_length=100)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE,
                                      name='type')
    owner = models.ForeignKey(Contractor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    businesses = models.ManyToManyField(Business, blank=True)

    def __str__(self):
        return self.title

    def get_duration(self):
        return self.date_to - self.date_from
