# Generated by Django 3.2.12 on 2022-05-24 20:15

import core.Profile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0003_assign_initial_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='expire_date',
            field=models.DateField(default=core.Profile.models.default_expire_date, null=True),
        ),
    ]
