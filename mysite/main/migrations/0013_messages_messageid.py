# Generated by Django 4.0.4 on 2022-08-02 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_team_relevant'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='messageid',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
