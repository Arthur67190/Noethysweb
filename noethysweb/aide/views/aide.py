# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import logging, json, importlib
logger = logging.getLogger(__name__)
from django.views.generic import TemplateView
from django.conf import settings
from core.views.base import CustomView
from outils.utils import utils_update
import requests
from django.shortcuts import render

class Aide(CustomView, TemplateView):
    template_name = "aide/aide.html"
    menu_code = "aide"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_titre'] = "Aide"
        context['videos'] = self.get_playlist_videos()
        return context

    def get_playlist_videos(self):
        api_key = 'AIzaSyAH4d8YfR35JZRDLVB-S80H64i32Q9naDc'
#TEST        playlist_id = 'PLNbT8-G8ACCkCMhfvKlxQtju4mn8NtJlz'
        playlist_id = 'PLX1Hj6AFyG5WzOavL7D0YT5csW9k'
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={api_key}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        'title': item['snippet']['title'],
                        'video_id': item['snippet']['resourceId']['videoId']
                    }
                    for item in data.get('items', [])
                ]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des vidéos : {e}")
        return []  # Retourne une liste vide en cas d'erreur