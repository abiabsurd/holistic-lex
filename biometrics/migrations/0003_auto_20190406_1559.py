# Generated by Django 2.1.5 on 2019-04-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biometrics', '0002_auto_20190308_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='weight',
            field=models.FloatField(blank=True, help_text='lbs', null=True),
        ),
    ]