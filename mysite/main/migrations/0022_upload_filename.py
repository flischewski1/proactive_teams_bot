# Generated by Django 4.0.4 on 2022-08-12 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='filename',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
