from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404


@login_required(login_url='login')
def HomePageView(request):
    return render(request, 'homepage.html')


def send_verification_code(email, request):
    
    code = str(random.randint(1000, 9999))

    request.session['verification_code'] = code
    request.session['verification_email'] = email

    send_mail(
        subject='Dawa Pharma - Confirmation de votre adresse e-mail',
        message=f'Votre code de confirmation est : {code}',
        from_email='Dawa Pharma <bouchrasraoui09@gmail.com>',
        recipient_list=[email],
        fail_silently=False,
    )


# fonction pour créer un compte 

def Creation_Compte(request):
    
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, "Les mots de passe ne sont pas identiques. veuillez réessayer.")
            return redirect("creation")

        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[^\w\s]', password):
            messages.error(request, 'Le mot de passse doit contenir au moins 8 caractères, incluant des lettres, des chiffres et des caractères spéciaux.')
            return redirect("creation")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "L'adresse e-mail invalide. Veuillez réessayer.")
            return redirect("creation")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà. Veuillez réessayer.")
            return redirect("creation")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée. Veuullez en choisir une autre.")
            return redirect("creation")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        request.session['verification_type'] = 'activation'
        send_verification_code(email, request)

        return redirect("verifier_code")

    return render(request, "creation.html")




# fonction pour se connecter

def Connecter_Compte(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("homepage")
        
        else:
            messages.error(request, "Nom d'utilisateur ou le mot de passe incorect.")
            return redirect("login")
    return render (request, 'login.html')



def Verification_Mail(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if not email:
            messages.error(request, "Veuillez rentrer une adresse mail valide.")
            return render(request, "verificaionMail.html")

        user = User.objects.filter(email=email).first()

        if user:
            request.session['verification_type'] = 'password_reset'
            send_verification_code(email, request)  
            return redirect("verifier_code") 
        else:
            messages.error(request, "Cette adresse ne correspond à aucun compte. Veuillez réessayer ou créez un compte.")
            return redirect("verification")

    return render(request, "verificaionMail.html", status=200)



def Changement_Code(request, email):

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        messages.error(request, "L'utilisateur Introuvable.")
        return redirect("verification")
    
    if request.method == "POST":

        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')


        if password == password_confirm:

            if len(password) < 8:
                messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")

            elif not any(char.isdigit() for char in password):

                messages.error(request, "Le mot de passe doit contenir au moins un chiffre")

            elif not any(char.isalpha() for char in password):

                messages.error(request, "Le mot de passe doit contenir au moins une lettre.")

            else:
                user.set_password(password)
                user.save()
                messages.success(request, "Le mot de passe a bien été modifié. Connectez-vous maintenant")

                return redirect("login")


        else:
            messages.error(request, "Les mots de passe ne correspondent pas. Réessayez")

            
    
    context = {
            'email':email
        }
    return render(request, "nouveauMDP.html", context)





def Verifier_Code(request):
    if request.method == "POST":
        code_saisi = request.POST.get('code')
        code_session = request.session.get('verification_code')
        email = request.session.get('verification_email')
        verification_type = request.session.get('verification_type')  # نوع التحقق

        if code_saisi == code_session:
            if verification_type == 'activation':
                try:
                    user = User.objects.get(email=email)
                    user.is_active = True
                    user.save()
                except User.DoesNotExist:
                    messages.error(request, "Utilisateur non trouvé.")
                    return redirect("creation")

                messages.success(request, "Votre compte est activé, connectez-vous maintenant.")
                return redirect("login")

            elif verification_type == 'password_reset':
              
                return redirect("modifierCode", email=email)

            else:
                messages.error(request, "Type de vérification inconnu.")
                return redirect("verification")

        else:
            messages.error(request, "Code incorrect. Veuillez réessayer.")

    return render(request, "verifierCode.html")




def Deconnection(request):
    logout(request)
    return redirect("login") 
def users_view(request):
    
    users = User.objects.filter(is_active=True)
    return render(request, 'users.html', {'users': users})


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def create_admin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

      
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            return redirect('create_admin')
        
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée.")
            return redirect('create_admin')
        
      
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Adresse e-mail invalide.")
            return redirect('create_admin')
        
       
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) \
           or not re.search(r'\d', password) or not re.search(r'[^\w\s]', password):
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères, incluant lettres, chiffres et caractères spéciaux.")
            return redirect('create_admin')

       
        User.objects.create_superuser(username=username, email=email, password=password)
        messages.success(request, "Nouvel administrateur créé avec succès.")
        return redirect('users')  

    return render(request, 'create_admin.html')
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser: 
        user.delete()
    return redirect('users')

