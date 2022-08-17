# Generated by Django 3.1.9 on 2022-08-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220505_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.CharField(choices=[(1, 'ADMIN'), (2, 'STAFF'), (3, 'MAINTAINER')], default=2, max_length=1),
        ),
    ]
