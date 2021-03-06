from enum import Enum
import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.utils import timezone

WIDTH_FIELD = 225
HEIGHT_FIELD = 225


class Role(Enum):
    ADMIN = 0
    CLIENT = 1
    CONTRACTOR = 2


class User(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    role = models.PositiveSmallIntegerField(blank=False,
                                            default=Role.ADMIN.value)
    avatar = models.ImageField('avatar', upload_to='avatars/',
                               default='default_image.png')

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     from PIL import Image

    # print("IMG: ", self.avatar.path)
    # photo = Image.open(self.avatar.path)

    #     photo.thumbnail((WIDTH_FIELD, HEIGHT_FIELD))
    #     photo.save(self.get_t)

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

    def save(self, *args, **kwargs):
        self.user.role = Role.CLIENT.value
        self.user.save()
        super().save(*args, **kwargs)


class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'contractor {}'.format(self.user.username)

    def save(self, *args, **kwargs):
        self.user.role = Role.CONTRACTOR.value
        self.user.save()
        super().save(*args, **kwargs)


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
        return self.opinion_set.all().aggregate(
            avg_rating=Avg('rating'))['avg_rating']

    get_average_rating.short_description = 'average rating'
    get_average_rating.empty_value_display = 'no opinions'
    get_average_rating.admin_order_field = 'name'

    def get_event_schedule(self):
        event_schedule = []
        for event in self.event_set.all():
            event_dict = {
                "id": str(event.pk),
                "title": str(event.title),
                "url": "/event/{}".format(event.pk),
                "class": "event-special",
                "start": str(event.date_from.timestamp() * 1000),
                "end": str(event.date_to.timestamp() * 1000)
            }
            event_schedule.append(event_dict)

        return event_schedule


class Event(models.Model):
    title = models.CharField(max_length=100)
    date_from = models.DateTimeField(blank=False, null=False)
    date_to = models.DateTimeField(blank=False, null=False)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    businesses = models.ManyToManyField(Business, blank=True)

    def __str__(self):
        return self.title

    def get_duration(self):
        return self.date_to - self.date_from

    def clean(self):
        super().clean()
        if not self.date_to or not self.date_from:
            raise ValidationError('Event must have start and end date.')
        if self.get_duration() < datetime.timedelta(days=0):
            raise ValidationError('Invalid event duration.')
        if self.date_from < timezone.now() or self.date_to < timezone.now():
            raise ValidationError('You can not add past event.')

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
