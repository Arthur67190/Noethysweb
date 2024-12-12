# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.urls import reverse
from core.views.mydatatableview import MyDatatable, columns, helpers
from core.views import crud
from core.models import ContactUrgence, Activite, Structure, Inscription, Individu
from fiche_individu.forms.individu_contacts import Formulaire


class Page(crud.Page):
    model = ContactUrgence
    url_liste = "contacts_urgence_liste"
    url_modifier = "contacts_urgence_modifier"
    url_supprimer = "contacts_urgence_supprimer"
    description_liste = "Voici ci-dessous la liste des contacts d'urgence et de sortie des individus."
    description_saisie = "Saisissez toutes les informations concernant le contact à saisir et cliquez sur le bouton Enregistrer."
    objet_singulier = "un contact d'urgence et de sortie"
    objet_pluriel = "des contacts d'urgence et de sortie"


class Liste(Page, crud.Liste):
    model = ContactUrgence

    def get_queryset(self):
        activites_accessibles = Activite.objects.filter(structure__in=self.request.user.structures.all())
        inscriptions_accessibles = Inscription.objects.filter(activite__in=activites_accessibles)
        individus_inscrits = Individu.objects.filter(idindividu__in=inscriptions_accessibles.values('individu'))
        return ContactUrgence.objects.select_related("famille", "individu").filter(individu__in=individus_inscrits).filter(self.Get_filtres("Q"))

    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['impression_introduction'] = ""
        context['impression_conclusion'] = ""
        context['page_titre'] = "Contacts"
        context['box_titre'] = "Liste des contacts d'urgence et de sortie"
        return context

    class datatable_class(MyDatatable):
        filtres = ["idcontact", "fpresent:famille", "ipresent:individu", "fscolarise:famille", "iscolarise:individu", "famille__nom", "individu__nom", "individu__prenom", "nom", "prenom", "rue_resid", "tel_domicile", "tel_mobile", "tel_travail", "autorisation_sortie", "autorisation_appel"]
        actions = columns.TextColumn("Actions", sources=None, processor='Get_actions_speciales')
        famille = columns.TextColumn("Famille", sources=['famille__nom'])
        individu = columns.CompoundColumn("Individu", sources=['individu__nom', 'individu__prenom'])
        tel_domicile = columns.TextColumn("Tél domicile", processor="Get_tel_domicile")
        tel_mobile = columns.TextColumn("Tél portable", processor="Get_tel_mobile")
        tel_travail = columns.TextColumn("Tél pro.", processor="Get_tel_travail")
        autorisations = columns.TextColumn("Autorisations", sources=["autorisation_sortie", "autorisation_appel"], processor='Get_autorisations')

        class Meta:
            structure_template = MyDatatable.structure_template
            columns = ["idcontact", "famille", "individu", "nom", "prenom", "tel_domicile", "tel_mobile", "tel_travail", "autorisations", "actions"]
            ordering = ["famille", "individu"]

        def Get_tel_domicile(self, instance, *args, **kwargs):
            return instance.tel_domicile

        def Get_tel_mobile(self, instance, *args, **kwargs):
            return instance.tel_mobile

        def Get_tel_travail(self, instance, *args, **kwargs):
            return instance.tel_travail

        def Get_autorisations(self, instance, *args, **kwargs):
            return instance.Get_autorisations()

        def Get_actions_speciales(self, instance, *args, **kwargs):
            html = [
                self.Create_bouton_modifier(url=reverse(kwargs["view"].url_modifier, args=[instance.pk])),
                self.Create_bouton_supprimer(url=reverse(kwargs["view"].url_supprimer, args=[instance.pk])),
                self.Create_bouton(url=reverse("famille_resume", args=[instance.famille_id]), title="Ouvrir la fiche famille", icone="fa-users"),
            ]
            return self.Create_boutons_actions(html)


class Modifier(Page, crud.Modifier):
    form_class = Formulaire

class Supprimer(Page, crud.Supprimer):
    form_class = Formulaire
