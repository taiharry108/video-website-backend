# Generated by Django 2.1.15 on 2020-05-21 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_ep'),
    ]

    operations = [
        migrations.AddField(
            model_name='ep',
            name='idx',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]