# Generated by Django 3.2.12 on 2022-05-23 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Category', '0001_initial'),
        ('Author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_stamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_stamp', models.DateTimeField(auto_now=True)),
                ('archived_stamp', models.DateTimeField(null=True)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=4048)),
                ('publish_date', models.DateField()),
                ('archived_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Author.author')),
                ('category', models.ManyToManyField(to='Category.Category')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'book',
            },
        ),
    ]
