# Generated by Django 3.1.3 on 2020-11-23 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20201123_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(default=0, max_length=6),
        ),
    ]
