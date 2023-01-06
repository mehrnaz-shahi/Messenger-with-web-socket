from django.db import models
from django.utils import timezone

from account import models as account

GROUPE_TYPE = (
    ('1', 'Group'),
    ('2', 'Channel')
)

class Group(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to="group/images/",blank=True, null=True)
    type = models.CharField(max_length=2, choices=GROUPE_TYPE)
    owner = models.ForeignKey(account.UserProfile, on_delete=models.CASCADE)


class GroupMember(models.Model):
    created = models.DateTimeField(default = timezone.now, verbose_name = "زمان ثبت نام")
    user = models.ForeignKey(account.UserProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)
    can_send_message = models.BooleanField(default=True)
    leave_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() + '-' + self.group.name 


class GroupMessage(models.Model):
    created = models.DateTimeField(default = timezone.now)
    group_member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    media = models.FileField(blank=True, null=True, upload_to="group/messages/")
    is_deleted = models.BooleanField(default=False)


class PV(models.Model):
    created = models.DateTimeField(default = timezone.now)
    user1 = models.ForeignKey(account.UserProfile, related_name='user1s', on_delete=models.CASCADE)
    user2 = models.ForeignKey(account.UserProfile, related_name='user2s',on_delete=models.CASCADE)


class PVMessage(models.Model):
    created = models.DateTimeField(default = timezone.now)
    pv = models.ForeignKey(PV, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(account.UserProfile, related_name='userpvmessages',on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    media = models.FileField(blank=True, null=True, upload_to="pv/messages/")
    is_deleted = models.BooleanField(default=False)
