from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from .forms import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Statistiques.views import generer_statistiques
from my_notifications.views import check_for_notifications 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class Affichage(LoginRequiredMixin, ListView):
    template_name = 'product.html'
    model = Produits
    context_object_name = 'produits'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category__id=category_id)  
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
        check_for_notifications(self.request.user, self.object)  
        return response

# class pour la modification

class update_donnees(LoginRequiredMixin, UpdateView):
    model = Produits
    form_class = AjoutProduit
    template_name = 'modification.html'
    success_url = reverse_lazy('products')
    def form_valid(self, form):
        response = super().form_valid(form)
        check_for_notifications(self.request.user, self.object)  
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


def recherche(request):
    produit = request.GET.get('q', '').strip()  
    selected_category = request.GET.get('category', '').strip()  

    donnees = Produits.objects.all()  

    if produit:
        donnees = donnees.filter(Q(name__icontains=produit))

    if selected_category:
        donnees = donnees.filter(category__id=selected_category)  

    categories = Categories.objects.all()  

    context = {
        'donnees': donnees,
        'selected_category': selected_category,
        'produit': produit,
        'categories': categories,
    }
    return render(request, 'search.html', context)


# class pour voir les details d'un produit 
def Filter(request):
    category_id = request.GET.get('category', '') 

    produits = Produits.objects.all()

    if category_id:
        produits = produits.filter(category__id=category_id)  

    categories = Categories.objects.all()  

    context = {
        'donnees': produits,
        'categories': categories,
        'selected_category': category_id, 
    }
    return render(request, 'search.html', context)


class edit(LoginRequiredMixin, DetailView):

    model = Produits
    template_name = 'icon.html'
    context_object_name = 'n'



# fonction pour la vente

def VenteProduits(request, id):
    produit = get_object_or_404(Produits, id=id)
    message = None

    if request.method == 'POST':
        form = AjoutVente(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            customer_name = form.cleaned_data['customer']

            if quantite > produit.quantite:
                message = "La quantité demandée dépasse le stock disponible !"
            else:
                customer, _ = Customer.objects.get_or_create(name=customer_name)

                total_amount = produit.price * quantite

                sale = Vente(produit=produit, quantite=quantite, total_amount=total_amount, customer=customer)
                sale.save()
                generer_statistiques(request)
            
                produit.quantite -= quantite
                produit.save()

                return redirect('facture', sale_id=sale.id)
    else:
        form = AjoutVente()

    if produit.quantite <= 10 and not message:
        message = "Attention, le stock est bas !"
        check_for_notifications(request.user,produit)
    context = {
        'produit': produit,
        'form': form,
        'message': message  
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

