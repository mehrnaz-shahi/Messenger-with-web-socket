# Generated by Django 4.1.4 on 2023-01-15 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='group/images/')),
                ('type', models.CharField(choices=[('1', 'Group'), ('2', 'Channel')], max_length=2)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان ثبت نام')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_member', models.BooleanField(default=True)),
                ('leave_date', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1s', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2s', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PVMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(blank=True, null=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='pv/messages/')),
                ('is_deleted', models.BooleanField(default=False)),
                ('pv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='main.pv')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userpvmessages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(blank=True, null=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='group/messages/')),
                ('is_deleted', models.BooleanField(default=False)),
                ('group_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.groupmember')),
            ],
        ),
    ]
