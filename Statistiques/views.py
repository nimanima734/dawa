from django.shortcuts import render
from datetime import date
from django.shortcuts import render
from django.db.models import Sum
from Produits.models import Produits, Vente
from .models import StatistiqueProduit

def generer_statistiques(request):
    today = date.today()
    produits = Produits.objects.all()

    for produit in produits:
        ventes_jour = Vente.objects.filter(produit=produit, sale_date__date=today)
        ventes_mois = Vente.objects.filter(produit=produit, sale_date__year=today.year, sale_date__month=today.month)

        stat, created = StatistiqueProduit.objects.get_or_create(produit=produit, date=today)

        stat.nbr_vente_par_jour = ventes_jour.aggregate(total=Sum("quantite"))["total"] or 0
        stat.total_vente_jour = ventes_jour.aggregate(total=Sum("total_amount"))["total"] or 0
        stat.nbr_vente_par_mois= ventes_mois.aggregate(total=Sum("quantite"))["total"] or 0
        stat.total_vente_mois = ventes_mois.aggregate(total=Sum("total_amount"))["total"] or 0

        stat.save()

    #return

def afficher_statistiques(request):
    stats = StatistiqueProduit.objects.filter(date=date.today())
    return render(request, "Statistiques/statistic.html", {"statistiques": stats})
