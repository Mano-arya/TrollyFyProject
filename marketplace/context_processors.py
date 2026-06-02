from .models import ChatMessage

def unread_messages_count(request):
    """
    Context processor to calculate the total number of unread messages for the logged-in user.
    """
    if request.user.is_authenticated:
        # Count messages where the recipient is the current user and is_read is False
        # In this system, ChatRoom participants are the ones who can receive messages.
        # A message is 'unread' if the user is a participant but NOT the sender.
        count = ChatMessage.objects.filter(
            room__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).distinct().count()
        return {'unread_count': count}
    return {'unread_count': 0}
