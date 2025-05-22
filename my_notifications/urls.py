# my_notifications/urls.py



from django.urls import path
from . import views

urlpatterns = [
    path('show_notifications/', views.ShowNotifications, name='show_notifications'),
    path('notification/read/<int:noti_id>/', views.MarkAsRead, name='mark_as_read'),
    path('notification/unread/<int:noti_id>/', views.MarkAsUnread, name='mark_as_unread'),
    path('notification/delete/<int:noti_id>/', views.DeleteNotification, name='delete_notification'),
    path('notification/mark_all_as_read/', views.MarkAllAsRead, name='mark_all_as_read'),
]
