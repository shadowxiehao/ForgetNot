from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Create your models here.

class User(AbstractBaseUser):
    # login message and password in the superclass
    email = models.CharField(max_length=128, unique=True)

    birthday = models.CharField(max_length=64, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", "male"), ("female", "female")), default="female")
    firstName = models.CharField(max_length=32, blank=True)
    lastName = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=False, blank=False)
    is_visitor = models.BooleanField(default=True)

    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = "email"

    def __serialize__(self):
        result = {'pk': self.pk, 'email': self.email, 'birthday': self.birthday, 'gender': self.gender,
                  'firstName': self.firstName,
                  'lastName': self.lastName, 'is_active': self.is_active, }
        return result


class Label(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=64)

    def is_owner(self, owner_id):
        return self.owner.id == owner_id


class Event(models.Model):
    title = models.CharField(max_length=256)
    notes = models.CharField(max_length=1024, default="", blank=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    allDay = models.BooleanField(default=False)
    rRule = models.CharField(max_length=512, null=True, blank=True, default="")
    exDate = models.CharField(max_length=1024, null=True, default="", blank=True)


class Event_User_Relation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.IntegerField(choices=((0, "owner"), (1, "invitee")), default=0)
    status = models.IntegerField(choices=((0, "pending"), (1, "accept"), (2, "Rejection")), default=0)

    label = models.ForeignKey(Label, on_delete=models.CASCADE)


class Contact_Msg(models.Model):
    email = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    message = models.CharField(max_length=2048)
