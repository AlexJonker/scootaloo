from django.urls import path
from django.views.generic import TemplateView
import os
from dotenv import load_dotenv

DEBUG = False
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ROOT_URLCONF = __name__
ALLOWED_HOSTS = ['*']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
    },
]

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='homepage'),
    path('about', TemplateView.as_view(template_name='about.html', extra_context={
        'title': 'scootaloo',
        'author': 'Alex, Natas and Brent'
    }), name='aboutpage'),
]
