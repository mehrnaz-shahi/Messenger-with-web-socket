# Generated by Django 3.2 on 2022-12-29 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20221215_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pvmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userpvmessages', to=settings.AUTH_USER_MODEL),
        ),
    ]
