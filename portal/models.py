from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class UserProfile(User):

    institute_name = models.CharField(max_length=80, blank=True)
    occupation = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=40, blank=True)
    aadhar_card_no = models.CharField(max_length=40, blank=True)
    aadhar_card_pic = models.ImageField(upload_to='portal/aadhar_cards', blank=True)
    pan_card_no = models.CharField(max_length=20, blank=True)
    pan_card_pic = models.ImageField(upload_to='portal/pan_cards', blank=True)
    email_confirmed = models.BooleanField(default=False)


class Recipient(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_required = models.FloatField(MinValueValidator(5000))
    # amount_received = models.FloatField()
    reason = models.TextField(default=None)
    date_of_reception = models.DateTimeField()

    def __str__(self):
        return self.user.first_name


class Donor(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_donated = models.FloatField(MinValueValidator(1))
    donation_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(default=None)

    def __str__(self):
        return self.user.first_name


class Ngo(models.Model):
    name = models.CharField(max_length=60, default='PHLOXIT')
    total_funds = models.FloatField(MinValueValidator(1))


class PeopleHelped(models.Model):
    person = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    amount_received = models.FloatField(MinValueValidator(1))
