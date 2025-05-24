from django.urls import path
from .views import * 




urlpatterns = [
     path('', Connecter_Compte, name='login'), 
    path('homepage/', HomePageView, name='homepage'), 
    path("creation/", Creation_Compte, name="creation"),
    path('verification/', Verification_Mail, name='verification'),
    path('modification-code/<str:email>/', Changement_Code, name="modifierCode"),
    path('logout/', Deconnection, name="deconnection"),
    path('users/', users_view, name='users'),
    path('users/create_admin/', create_admin_view, name='create_admin'),
    path("verifier-code/", Verifier_Code, name="verifier_code"),
    path("modifier-code/<str:email>/", Changement_Code, name="modifierCode"),
]
