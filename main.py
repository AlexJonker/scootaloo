from django.urls import re_path
from django.views.generic import TemplateView
import os
from dotenv import load_dotenv, find_dotenv


DEBUG = False
load_dotenv(dotenv_path=find_dotenv())
SECRET_KEY = os.getenv("SECRET_KEY")
ROOT_URLCONF = __name__
ALLOWED_HOSTS = ['*']


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates/'
        ],
        'APP_DIRS': True,
    },
]

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='homepage'),

    re_path(r'^about$', TemplateView.as_view(template_name='about.html', extra_context={
        'title': 'scootaloo',
        'author': 'Alex, Natas and Brent'
    }), name='aboutpage'),
    
]
