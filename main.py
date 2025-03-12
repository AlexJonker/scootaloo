from django.urls import path
from django.conf.urls.static import static
from django.views.generic import TemplateView
import os
from scripts.login_system import *
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEBUG = True
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

    path('login', login_view, name='login'),

    path('signup', signup_view, name='signup'),

] + static('/static/', document_root=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

