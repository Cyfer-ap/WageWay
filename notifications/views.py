from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from users.utils import is_user_online
from .models import Message
from .forms import MessageForm
from users.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Notification
@login_required
def inbox(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    conversations = {}
    for message in messages:
        other = message.receiver if message.sender == request.user else message.sender
        if other not in conversations:
            conversations[other] = message
    return render(request, 'notifications/inbox.html', {'conversations': conversations})


@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Fetch conversation messages
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # Mark unread messages as seen
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True, status='seen')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.status = 'sent'
            msg.save()
            Notification.objects.create(
                user=other_user,
                message=f"New message from {request.user.username}",
                url=reverse('conversation', args=[request.user.id])
            )



            return redirect('conversation', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'notifications/conversation.html', {
        'form': form,
        'messages': messages,
        'other_user': other_user,
        'is_online': is_user_online(other_user),
    })




@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})



