# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import logging, json
logger = logging.getLogger(__name__)
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _
from core.views import crud
from core.models import PortailMessage, PortailRenseignement, Piece
from portail.forms.transmettre_piece import Formulaire
from portail.views.base import CustomView
from django.shortcuts import render, redirect
from django.contrib import messages



class Page(CustomView):
    model = PortailMessage
    menu_code = "portail_documents"

    def get_context_data(self, **kwargs):
        context = super(Page, self).get_context_data(**kwargs)
        context['page_titre'] = _("Transmettre un document")
        context['box_titre'] = None
        context['box_introduction'] = _("Renseignez les caractéristiques du document et cliquez sur le bouton Envoyer.")
        return context

    def get_success_url(self):
        return reverse_lazy("portail_documents")


class Ajouter(Page, crud.Ajouter):
    form_class = Formulaire
    texte_confirmation = _("Le document a bien été transmis")
    titre_historique = _("Ajouter une pièce")
    template_name = "portail/edit.html"

    def Get_detail_historique(self, instance):
        return "Famille=%s, Pièce=%s" % (self.request.user.famille, instance.Get_nom())

    def form_valid(self, form):
        # Appel de la méthode parent pour la validation
        response = super().form_valid(form)

        # Gestion des fichiers téléchargés
        documents = {
            'document1': form.cleaned_data.get('document1'),
            'document2': form.cleaned_data.get('document2'),
            'document3': form.cleaned_data.get('document3'),
            'document4': form.cleaned_data.get('document4'),
        }

        for field_name, file in documents.items():
            if file:
                Piece.objects.create(
                    titre=form.cleaned_data.get('titre'),
                    document=file,
                    famille=self.request.user.famille,
                    individu=form.cleaned_data.get('individu'),
                    type_piece=form.cleaned_data.get('type_piece'),
                    date_debut=form.cleaned_data.get('date_debut'),
                    date_fin=form.cleaned_data.get('date_fin'),
                    auteur=self.request.user
                )

        messages.success(self.request, "Les pièces ont été ajoutées avec succès.")
        return redirect(self.get_success_url())

    def Apres_form_valid(self, form=None, instance=None):
        # Mémorisation du renseignement
        PortailRenseignement.objects.create(famille=self.request.user.famille, individu=instance.individu,
                                            categorie="famille_pieces", code="Nouvelle pièce", validation_auto=True,
                                            nouvelle_valeur=json.dumps(instance.Get_nom(), cls=DjangoJSONEncoder), idobjet=instance.pk)
