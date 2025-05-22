from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from .forms import *
from Utilisateurs import views
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *

from my_notifications.views import check_for_notifications 
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

# def home(request):

#     # # récuperationndes données
#     # donnees = Produits.objects.all()

#     # context = {
#     #     'donnees':donnees
#     # }

# # , context
#     return render(request,'home.html')


# def categories(request):
#     produits = Produits.objects.all()
#     categories = Categories.objects.all()  # تأكد من هذا السطر

#     return render(request, 'products.html', {
#         'produits': produits,
#         'categories': categories,  # لازم تكون موجودة باش تقدر تستخدمها
#     })


class Affichage(LoginRequiredMixin, ListView):
    template_name = 'product.html'
    model = Produits
    context_object_name = 'produits'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category__id=category_id)  # فلترة بالآيدي
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class AjoutProduits(LoginRequiredMixin, CreateView):
    model = Produits
    form_class = AjoutProduit
    template_name = 'ajout-donnees.html'
    success_url = reverse_lazy('products') 

    def form_valid(self, form):
        response = super().form_valid(form)
        check_for_notifications(self.request.user, self.object)  # تمرير المنتج الجديد فقط
        return response

# class pour la modification

class update_donnees(LoginRequiredMixin, UpdateView):
    model = Produits
    form_class = AjoutProduit
    template_name = 'modification.html'
    success_url = reverse_lazy('products')
    def form_valid(self, form):
        response = super().form_valid(form)
        check_for_notifications(self.request.user, self.object)  # تمرير المنتج الجديد فقط
        return response

# fonction pour supprimer 
@csrf_exempt
def delete_product(request, id):
    if request.method == 'POST':
        try:
            produit = Produits.objects.get(pk=id)
            produit.delete()
            return JsonResponse({'success': True})
        except Produits.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def statistic(request):
    return render(request, 'statistic.html')

# def product_list(request):
#     categories = Categories.objects.all()
#     return render(request, 'product.html', {
#         'categories': categories,
#     })

# class pour supprimer les données
# class delete(LoginRequiredMixin, DeleteView):

#     model = Produits
#     template_name = "delete.html"
#     success_url = reverse_lazy('product')


# fonction de recher de produit
# @login_required(login_url='login')

def recherche(request):
    produit = request.GET.get('q', '').strip()  # استخدام q للبحث عن الاسم
    selected_category = request.GET.get('category', '').strip()  # فئة البحث

    donnees = Produits.objects.all()  # كل المنتجات

    # تصفية النتائج بناءً على الاسم أو الفئة
    if produit:
        donnees = donnees.filter(Q(name__icontains=produit))

    if selected_category:
        donnees = donnees.filter(category__id=selected_category)  # تصفية باستخدام الـ category ID

    categories = Categories.objects.all()  # قائمة الفئات

    context = {
        'donnees': donnees,
        'selected_category': selected_category,
        'produit': produit,
        'categories': categories,
    }
    return render(request, 'search.html', context)




# # fonction pour voir les details
    
# def detail(request, id):

#     n = Produits.objects.get(id=id)

#     return render(request, 'detail.html', {'n':n})


# class pour voir les details d'un produit 
def Filter(request):
    category_id = request.GET.get('category', '')  # ناخذ قيمة category من الـ GET

    produits = Produits.objects.all()

    if category_id:
        produits = produits.filter(category__id=category_id)  # فلترة حسب id الفئة

    categories = Categories.objects.all()  # نرسل جميع الفئات للعرض في الـ combobox

    context = {
        'donnees': produits,
        'categories': categories,
        'selected_category': category_id,  # لإظهار القيمة المحددة في الـ select بعد الفلترة
    }
    return render(request, 'search.html', context)


class edit(LoginRequiredMixin, DetailView):

    model = Produits
    template_name = 'icon.html'
    context_object_name = 'n'



# fonction pour la vente

def VenteProduits(request, id):
    produit = get_object_or_404(Produits, id=id)
    message = None  # Variable pour stocker les messages d'erreur ou d'avertissement

    if request.method == 'POST':
        form = AjoutVente(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            customer_name = form.cleaned_data['customer']

            # Vérification si la quantité demandée est supérieure au stock
            if quantite > produit.quantite:
                message = "La quantité demandée dépasse le stock disponible !"
            else:
                customer, _ = Customer.objects.get_or_create(name=customer_name)

                # Calcul du montant total de la vente
                total_amount = produit.price * quantite

                # Enregistrement de la vente
                sale = Vente(produit=produit, quantite=quantite, total_amount=total_amount, customer=customer)
                sale.save()

                # Mise à jour de la quantité de vente dans le produit
                produit.quantite -= quantite
                produit.save()

                # Redirection vers la page de reçu
                return redirect('facture', sale_id=sale.id)
    else:
        form = AjoutVente()

    # Vérification si le stock est bas (par exemple <= 5)
    if produit.quantite <= 10 and not message:
        message = "Attention, le stock est bas !"
        check_for_notifications(request.user,produit)
    context = {
        'produit': produit,
        'form': form,
        'message': message  # Passer le message au template
    }
    return render(request, 'fomulaire_vente.html', context)
    

def SaveRecu(request, id):

    vente = get_object_or_404(Vente, id=id)
    customer = vente.customer
    quantite = vente.quantite
    total_amount = vente.total_amount
    produit = vente.produit

    recu = Facture_Client(
        customer = customer,
        quantite = quantite,
        total_amount = total_amount,
        produit = produit
    )

    recu.save()

    return redirect('facture', sale_id = id)


#  fonction pour afficher les données de la vente

def Facture(request, sale_id):

    sale = get_object_or_404(Vente, id=sale_id)
    customer = sale.customer
    produit = sale.produit
    quantite = sale.quantite
    sale_date = sale.sale_date
    total_amount = sale.total_amount

    context = {
        'sale':sale,
        'customer':customer,
        'produit':produit,
        'quantite':quantite,
        'sale_date': sale_date,
        'id':sale.id,
        'prix_unitaire': produit.price,
        'total_amount':total_amount
    }
    return render(request, 'facture-client.html', context)


class vente(ListView):
    template_name = 'vente.html'
    queryset = Vente.objects.all()

def recu(request):
    recus = Facture_Client.objects.all()
    
    return render (request, 'recu.html',{'recus': recus})



# fonction pour modifier les donnees 

# def modifier(request, id):

#     produit= get_object_or_404(Produits, id=id)
#     categories= Categories.objects.all()
#     errors = {}

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         category_id = request.POST.get('category')
#         price = request.POST.get('price')
#         quantite = request.POST.get('quantite')
#         description = request.POST.get('description')
#         date_expiration = request.POST.get('date_expiration')
#         image = request.FILES.get('image')


#         # validation des champs

#         if not name:
#             errors['name'] = "Le nom est requis"

#         if not category_id:
#             errors['category'] = "La categorie est requise"

#         if not price:
#             errors['price'] = "Le prix est requis"

#         if not quantite:
#             errors['quantite'] = "La quantite est requise"

#         if not description:
#             errors['description'] = "La description est requise"


#         if date_expiration:
#             try:
#                 datetime.strptime(date_expiration, '%Y-%m-%d')
#             except ValueError:
#                 errors['date_expiration'] = "Le format de la date d'expiration est incorrect. Utilisez le format AAAA-MM-JJ."

        
#         if not errors:

#             category = get_object_or_404(Categories, id=category_id)
#             produit.name = name
#             produit.category = category
#             produit.price = price
#             produit.quantite = quantite
#             produit.description = description
#             produit.date_expiration = date_expiration


#             if image:
                
#                 fs = FileSystemStorage()
#                 filname= fs.save(name.name, image)
#                 produit.image = fs.url(filname)



#         produit.save()
#         messages.success(request, "Le produit a été modifié avec succès !")
#         return redirect("home")
    
#     else:

#         for key, errror  in errors.items():
#             messages.error(request, errror)

#     return render (request, "modification.html",{'produit':produit, 'categories':categories, 'errors':errors} )
    
    





  




    

# fonction d'ajout des données

# def ajout_donnees(request):
#     errors = {}
    
#     if request.method == 'POST':
#         name = request.POST['name']
#         price_str = request.POST['price']
#         quantite = request.POST['quantite']
#         date_expiration_str = request.POST['date_expiration']
#         description = request.POST['description']
#         image = request.FILES['image']

#         # Valider la date
#         try:
#             date_expiration = datetime.strptime(date_expiration_str, '%Y-%m-%d')
#         except ValueError:
#             errors['date_expiration'] = 'Le format de la date est incorrect. Utilisez le format AAAA-MM-JJ.'

#         # Valider le prix
#         try:
#             price = float(price_str)
#             if price < 0:
#                 errors['price'] = 'Le prix ne peut pas être négatif.'
#         except ValueError:
#             errors['price'] = 'Veuillez entrer un prix valide.'

#         # Si aucune erreur, sauvegarder le produit
#         if not errors:
#             try:
#                 # Récupération des catégories dans la table en fonction de la clé primaire
#                 category = Categories.objects.get(pk=request.POST['category'])

#                 savedonnes = Produits(
#                     name=name,
#                     price=price,
#                     quantite=quantite,
#                     description=description,
#                     date_expiration=date_expiration,
#                     category=category,
#                     image=image
#                 )
#                 savedonnes.save()
#                 messages.success(request, 'Produit ajouté avec succès!')
#                 return redirect('home')
#             except Categories.DoesNotExist:
#                 errors['category'] = 'La catégorie spécifiée est introuvable.'
#             except KeyError as e:
#                 errors[str(e)] = f'Le champ {e} est manquant dans la requête.'
#             except Exception as e:
#                 messages.error(request, f'Une erreur est survenue : {e}')

#     category = Categories.objects.all()  # Notez les parenthèses ici

#     return render(request, "ajout-donnees.html", {"category": category, "errors": errors})



# def search_products(request):
#     query = request.GET.get('q', '')
#     produits = Produits.objects.filter(name__icontains=query)
#     return render(request, 'search_results.html', {'produit': produits, 'query': query})


# from django.contrib.auth import login ,authenticate,logout

# from django.contrib import messages

# def Connexion_Compte(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('homepage')
#         else:
#             messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")  # Utilisation du framework de messages
#             return redirect('login')  # Rediriger pour éviter la soumission multiple du formulaire
#     return render(request, 'login.html')


