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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="show_notifications")  
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")  
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)  
    product = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")  
    text_preview = models.CharField(max_length=150, blank=True) 
    date = models.DateTimeField(default=timezone.now) 
    unread = models.BooleanField(default=True)  
    is_seen = models.BooleanField(default=False)  
    
    class Meta:
        ordering = ['-date']  

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"

