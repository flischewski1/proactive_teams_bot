# Generated by Django 4.0.4 on 2022-07-29 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_messages_channelid'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='relevant',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]