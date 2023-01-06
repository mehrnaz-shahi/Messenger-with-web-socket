from django.shortcuts import render, redirect

from main import models




def group_view(request, group_id):

    group = models.Group.objects.filter(id=group_id)

    if not group:
        return redirect('main:index')

    group = group[0]
    
    gpmessages = models.GroupMessage.objects.filter(group_member__group = group, is_deleted = False)

    group_members = models.GroupMember.objects.filter(group=group, is_member=True)

    context = {
        'group': group,
        'gpmessages': gpmessages,
        'is_member': request.user.is_member(group),
        'can_send_message': request.user.can_send_message(group),
        'group_members': group_members
    }

    return render(request, 'group.html', context)
