from django.urls import path

from .views import ping_view, scheduler_view

urlpatterns = [
    path('', ping_view, name='index'),
    path('ping/', ping_view, name='ping'),
    path('scheduler/', scheduler_view, name='scheduler'),
]
