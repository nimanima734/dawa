
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from Produits.models import Produits
from datetime import timedelta
from django.utils import timezone
from my_notifications.models import Notification
from django.utils import timezone
from my_notifications.models import Notification
from Produits.models import Produits 
def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)  # Get all notifications for the user
    unread_count = notifications.filter(unread=True).count()  # Count unread notifications
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count
    }
    return render(request, 'my_notifications/show_notifications.html', context)


def DeleteNotification(request, noti_id):
    notification = get_object_or_404(Notification, id=noti_id, user=request.user)  # Get notification by ID and user
    notification.delete()  # Delete the notification
    return redirect('show_notifications')


def MarkAsRead(request, noti_id):
    notification = get_object_or_404(Notification, id=noti_id, user=request.user)  # Get notification by ID and user
    notification.unread = False  # Mark as read
    notification.is_seen = True  # Mark as seen
    notification.save()  # Save the changes
    return redirect('show_notifications')


def MarkAsUnread(request, noti_id):
    notification = get_object_or_404(Notification, id=noti_id, user=request.user)  # Get notification by ID and user
    notification.unread = True  # Mark as unread
    notification.is_seen = False  # Mark as unseen
    notification.save()  # Save the changes
    return redirect('show_notifications')


def MarkAllAsRead(request):
    Notification.objects.filter(user=request.user, unread=True).update(unread=False, is_seen=True)  # Mark all unread notifications as read
    return redirect('show_notifications')

def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, unread=True).count()  # Get count of unread notifications
    return {'count_notifications': count_notifications}


 # افترض أن هذا هو مكان تعريف منتجك

def check_for_notifications(user ,product ):
  

  
        # مثال لفحص وتوليد إشعارات
        if product.is_expiring_soon():
            Notification.objects.create(
                notification_type=1,
                product=product,
                text_preview=f"Your medication {product.name} is expiring soon.",
                date=timezone.now(),
                user=user ,
              
                 # تعيين المستخدم هنا
            )
           
        if product.is_low_stock():
            Notification.objects.create(
                notification_type=2,
                product=product,
                text_preview=f"The stock of {product.name} is low.",
                date=timezone.now(),
                user=user,
                
                  # تعيين المستخدم هنا
            )



