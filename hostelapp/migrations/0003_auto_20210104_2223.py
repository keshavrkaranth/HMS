# Generated by Django 3.1.3 on 2021-01-04 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostelapp', '0002_warden_phoneno'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='current_no_of_persons',
            field=models.PositiveIntegerField(blank=True, default=0, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='max_no_of_persons',
            field=models.PositiveIntegerField(default=2, max_length=2),
        ),
        migrations.AlterField(
            model_name='student',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostelapp.room'),
        ),
    ]
