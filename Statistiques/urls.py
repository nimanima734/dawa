from django.urls import path
from . import views

urlpatterns = [
    path('afficher_statistiques/', views.afficher_statistiques, name='afficher_statistiques'),

]