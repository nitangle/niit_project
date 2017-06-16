from __future__ import unicode_literals

from django.db import models


class Recipient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(widget=models.EmailField)
    institute_name = models.CharField(max_length=80)
    amount_required = models.FloatField()
    amount_received = models.FloatField()
    date_of_reception = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    def get_recipients(self, n=6):
        recent_recipients = Recipient.objects.order_by('-transaction_date')[:n]
        return recent_recipients



class Donor(models.Model):
    first_name = models.CharField(max_field=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(widget=models.EmailField)
    occupation = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=40, default=None)
    amount_donated = models.FloatField()
    donation_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "{} donated {}".format(self.first_name, self.amount_donated)

    def get_top_donors(self, n=5):
        top_donors = Donor.objects.order_by('-donation_date')[:n]
        return top_donors


class Ngos(models.Model):
    name = models.CharField(max_length=60)
    total_funds = models.FloatField()

