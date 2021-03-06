# Generated by Django 3.1.3 on 2021-01-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostelapp', '0004_auto_20210104_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='current_no_of_persons',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='max_no_of_persons',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
