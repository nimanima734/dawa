from django.db import models

# Create your models here.
from django.db import models
from Produits.models import Produits,Vente

class StatistiqueProduit(models.Model):
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    date = models.DateField()

    nbr_vente_par_jour = models.IntegerField(default=0)
    total_vente_jour = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    nbr_vente_par_mois = models.IntegerField(default=0)
    total_vente_mois = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('produit', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.produit.name} - {self.date}"