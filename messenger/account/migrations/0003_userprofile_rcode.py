# Generated by Django 3.2 on 2022-12-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userprofile_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='rcode',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]