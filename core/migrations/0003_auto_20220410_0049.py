# Generated by Django 3.1.9 on 2022-04-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220410_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='print',
            name='print_no',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
