# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import logging
logger = logging.getLogger(__name__)
from core.models import Historique
from core.models import Individu


def Ajouter(titre="", detail="", utilisateur=None, famille=None, individu=None, collaborateur=None, objet=None, idobjet=None, classe=None, old=None, portail=False, activite=None):
    try:
        if individu and not Individu.objects.filter(idindividu=individu).exists():  # Vérifie si l'individu existe toujours
            individu = None

        Historique.objects.create(titre=titre, detail=detail, utilisateur=utilisateur, famille_id=famille, individu_id=individu,
                                  collaborateur_id=collaborateur, objet=objet, idobjet=idobjet, classe=classe, old=old, portail=portail, activite_id=activite)
    except Exception as err:
        logger.error('Erreur dans ajout historique : %s - titre="%s" detail="%s"', err, titre, detail, exc_info=True)


def Ajouter_plusieurs(actions=[]):
    liste_ajouts = [Historique(**action) for action in actions]
    Historique.objects.bulk_create(liste_ajouts)
