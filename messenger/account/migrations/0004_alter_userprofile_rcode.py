# Generated by Django 3.2 on 2022-12-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userprofile_rcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='rcode',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
