from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('update_debut/', views.DebutView.as_view())
]