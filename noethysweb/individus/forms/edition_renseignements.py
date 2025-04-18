# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Fieldset, Hidden
from crispy_forms.bootstrap import Field
from core.forms.select2 import Select2MultipleWidget
from core.models import Rattachement
from core.utils.utils_commandes import Commandes
from core.forms.base import FormulaireBase


class Formulaire(FormulaireBase, forms.Form):
    tri = forms.ChoiceField(label="Tri", choices=[("nom", "Nom"), ("classe", "Classe")], initial="nom", required=False)
    afficher_signature = forms.BooleanField(label="Afficher la signature", required=False, initial=True, help_text="Une case signature est ajoutée à la fin du document afin de permettre la validation des données par la famille.")
    mode_condense = forms.BooleanField(label="Mode condensé", required=False, initial=False, help_text="Aucune ligne vierge n'est ajoutée aux rubriques.")
    rattachements = forms.MultipleChoiceField(label="Individus", widget=Select2MultipleWidget(), choices=[], required=False)

    def __init__(self, *args, **kwargs):
        idfamille = kwargs.pop("idfamille", None)
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form_parametres'
        self.helper.form_method = 'post'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        self.helper.layout = Layout(
            Commandes(annuler_url="{% url 'individus_toc' %}", enregistrer=False, ajouter=False,
                      commandes_principales=[HTML(
                          """<a type='button' class="btn btn-primary margin-r-5" onclick="generer_pdf()" title="Génération du PDF"><i class='fa fa-file-pdf-o margin-r-5'></i>Générer le PDF</a>"""),
                      ]),
            Fieldset("Options",
                Field("afficher_signature"),
                Field("mode_condense"),
            ),
            Fieldset("Sélection des individus"),
        )

        # Si impression depuis la fiche famille
        if idfamille:
            self.helper.layout.append(Hidden("idfamille", value=idfamille))
            self.helper.layout.append(Field("rattachements"))
            self.fields["rattachements"].choices = [(r.pk, r.individu.prenom) for r in Rattachement.objects.select_related("individu").filter(famille_id=idfamille).order_by("individu__prenom")]
