# Generated by Django 3.1.3 on 2021-01-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostelapp', '0010_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='created_date',
            name='user',
            field=models.CharField(max_length=20),
        ),
    ]