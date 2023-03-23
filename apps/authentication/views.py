import subprocess
from ast import Dict
from typing import Any
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from authentication.models import Team
from src.constants import LEAGUES_LINKS
from .services.crawler import collect_data
import threading


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        teams = Team.objects.all()
        context['teams'] = teams
        context['leagues'] = LEAGUES_LINKS
        return context
    
class DebutView(View):
    def get(self, request, *args, **kwargs):
        
        scrape_thread = threading.Thread(target=collect_data, args=())
        scrape_thread.name = "scrape-thread"
        scrape_thread.start()

        subprocess.run()
        teams = Team.objects.all()
        return render(request, 'debut.html', {'teams': teams})
