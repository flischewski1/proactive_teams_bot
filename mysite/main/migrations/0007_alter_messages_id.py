# Generated by Django 4.0.4 on 2022-07-27 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_user_messages_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
