# my_notifications/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Produits.models import Produits
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Medicine Expiration'),
        (2, 'Medicine Quantity Low'),
        (3, 'General Alert')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="show_notifications")  # Receiver of the notification
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")  # Sender of the notification
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)  # Type of notification
    
    # Medicine field is optional but relevant to some types of notifications
    product = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")  # Associated medicine
    text_preview = models.CharField(max_length=150, blank=True)  # Text preview of the notification
    
    date = models.DateTimeField(default=timezone.now)  # Date and time of notification
    unread = models.BooleanField(default=True)  # Track if notification is unread
    is_seen = models.BooleanField(default=False)  # Track if notification is seen
    
    class Meta:
        ordering = ['-date']  # Order notifications by most recent first

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"

