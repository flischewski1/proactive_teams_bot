# Generated by Django 4.0.4 on 2022-08-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_user_firstlogindate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstmessage',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
