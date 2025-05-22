from django.urls import path
from .views import * 




urlpatterns = [
     path('', Connecter_Compte, name='login'), 
    path('homepage/', HomePageView, name='homepage'), 
    path("creation/", Creation_Compte, name="creation"),
    path('verification/', Verification_Mail, name='verification'),
    path('modification-code/<str:email>/', Changement_Code, name="modifierCode"),
    path('logout/', Deconnection, name="deconnection"),
]
