from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from Produits.models import Produits
from django.utils import timezone
from Produits.models import Produits 
from django.db.models import Q

def ShowNotifications(request):
    user = request.user
    # notifications = Notification.objects.filter(user=user) 
    notifications = Notification.objects.filter(Q(user=user) | Q(user__isnull=True))

    unread_count = notifications.filter(unread=True).count() 
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count
    }
    return render(request, 'my_notifications/show_notifications.html', context)


def DeleteNotification(request, noti_id):
    notification = get_object_or_404(Notification, id=noti_id, user=request.user) 
    notification.delete() 
    return redirect('show_notifications')


def MarkAsRead(request, noti_id):
    notification = get_object_or_404(Notification, id=noti_id, user=request.user)  
    notification.unread = False 
    notification.is_seen = True 
    notification.save()  
    return redirect('show_notifications')


def MarkAsUnread(request, noti_id):
    notification = get_object_or_404(Notification, id=noti_id, user=request.user)  
    notification.unread = True 
    notification.is_seen = False  
    notification.save()  
    return redirect('show_notifications')


def MarkAllAsRead(request):
    Notification.objects.filter(user=request.user, unread=True).update(unread=False, is_seen=True)  
    return redirect('show_notifications')


def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, unread=True).count() 
    return {'count_notifications': count_notifications}


def check_for_notifications(user ,product ):
    
        if product.is_expiring_soon():
            Notification.objects.create(
                notification_type=1,
                product=product,
                text_preview=f"Your medication {product.name} is expiring soon.",
                date=timezone.now(),
                user=None ,
            )
           
        if product.is_low_stock():
            Notification.objects.create(
                notification_type=2,
                product=product,
                text_preview=f"The stock of {product.name} is low.",
                date=timezone.now(),
                user=None ,
            )
