from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.safestring import mark_safe
from django.shortcuts import reverse

from biometrics.biometrics import (
    ACTIVITY_RATINGS, BODY_FRAME_TYPE_CHOICES, SEX_CHOICES, hamwi_ideal_weight
)


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    dob = models.DateField(verbose_name='date of birth')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES.items())
    height = models.FloatField(help_text='inches')
    usual_weight = models.PositiveSmallIntegerField(help_text='lbs')
    frame_type = models.CharField(
        max_length=1, choices=BODY_FRAME_TYPE_CHOICES.items(), help_text='based off wrist size'
    )
    notes = models.TextField()

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def age(self):
        return relativedelta(date.today(), self.dob).years

    @property
    def ideal_weight(self):
        return hamwi_ideal_weight(self.sex, self.height, self.frame_type)

    def get_metrics_url(self):
        return reverse('client_metrics', kwargs={'pk': self.id}) if self.id else None

    def metrics_link(self):
        url = self.get_metrics_url()
        return mark_safe('<a href={}>Click here</a>'.format(url)) if url else 'N/A'
    metrics_link.short_description = 'Biometrics Dashboard'


class Entry(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField(default=date.today)
    notes = models.TextField(null=True, blank=True)

    # OMRON MEASUREMENTS
    weight = models.FloatField(help_text='lbs')
    bmi = models.FloatField(null=True, blank=True, verbose_name='body mass index')
    body_fat = models.FloatField(null=True, blank=True, help_text='%')
    skeletal_muscle = models.FloatField(null=True, blank=True, help_text='%')
    resting_metabolism = models.FloatField(null=True, blank=True, help_text='kcal')
    body_age = models.PositiveSmallIntegerField(null=True, blank=True)
    visceral_fat_level = models.PositiveSmallIntegerField(null=True, blank=True)

    # OTHERS
    waist_circumference = models.FloatField(null=True, blank=True, help_text='cm')
    activity_rating = models.PositiveSmallIntegerField(
        null=True, blank=True, choices=enumerate(ACTIVITY_RATINGS)
    )
    total_energy_intake = models.FloatField(null=True, blank=True, help_text='kcal')

    def __str__(self):
        return 'Entry from {}'.format(self.date)

    class Meta:
        unique_together = ('client', 'date')
