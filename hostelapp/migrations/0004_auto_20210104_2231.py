# Generated by Django 3.1.3 on 2021-01-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostelapp', '0003_auto_20210104_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='no',
            field=models.CharField(max_length=20),
        ),
    ]