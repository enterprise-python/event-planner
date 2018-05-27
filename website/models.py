from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(Enum):
    ADMIN = 0
    CLIENT = 1
    CONTRACTOR = 2


class User(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    role = models.PositiveSmallIntegerField(blank=False,
                                            default=Role.ADMIN.value)

    def __str__(self):
        return self.username

    def get_role(self):
        return Role(self.role).name

    get_role.short_description = 'role'
    get_role.admin_order_field = 'role'

    def is_admin(self):
        return self.get_role() == Role.ADMIN.name

    def is_client(self):
        return self.get_role() == Role.CLIENT.name

    def is_contractor(self):
        return self.get_role() == Role.CONTRACTOR.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'client {}'.format(self.user.username)


class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'contractor {}'.format(self.user.username)


class BusinessType(models.Model):
    business_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.business_type


class Business(models.Model):
    name = models.CharField(max_length=100)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)
    owner = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    description = models.TextField(max_length=500,
                                   default='Business description...')

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.name

    def get_average_rating(self):
        opinions = self.opinion_set.all()
        if opinions:
            return sum(opinion.rating for opinion in opinions) / len(opinions)

    get_average_rating.short_description = 'average rating'
    get_average_rating.empty_value_display = 'no opinions'
    get_average_rating.admin_order_field = 'name'

    def get_event_schedule(self):
        event_schedule = []
        for event_id, event in enumerate(self.event_set.all()):
            event_schedule.append((event_id, event.date_from, event.date_to))

        return event_schedule


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

    get_duration.short_description = 'duration'
    get_duration.admin_order_field = 'date_from'


class Opinion(models.Model):
    RATINGS = (
        (1, 'Very bad'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    )

    rating = models.PositiveSmallIntegerField(choices=RATINGS)
    text = models.TextField(max_length=500)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        text_limit = 50
        return self.text if len(self.text) <= text_limit else '{}...'.format(
            self.text[:text_limit])
