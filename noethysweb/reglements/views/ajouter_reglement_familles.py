from django.urls import reverse
from core.views import crud
from core.views.mydatatableview import MyDatatable, columns
from core.models import Activite, Famille, Reglement
from django.db.models import Q

class Page(crud.Page):
    model = Reglement

class Liste(Page, crud.Liste):
    model = Famille
    
    def get_queryset(self):
        user = self.request.user
        
        activite_ids = Activite.objects.filter(structure__in=user.structures.all(),visible=True).values_list('idactivite', flat=True)
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(prestation__activite__idactivite__in=activite_ids)).distinct()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['page_titre'] = "Liste des paiements en ligne"
        context['box_titre'] = "Liste des paiements en ligne"
        return context
    
    class datatable_class(MyDatatable):
        famille = columns.TextColumn("Famille", sources=['nom'])
        actions = columns.TextColumn("Actions", sources=None, processor='Get_actions_speciales')
        
        class Meta():
            structure_template = MyDatatable.structure_template
            columns = ['idfamille','utilisateur', 'famille']
        
        def Get_actions_speciales(self, instance, *args, **kwargs):
            html = [
                self.Create_bouton_ouvrir(url=reverse("famille_reglements_ajouter", kwargs={"idfamille": instance.idfamille}), title="Ajouter un règlement")
            ]
            return self.Create_boutons_actions(html)