from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from dotenv import load_dotenv
import os

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
    path('', TemplateView.as_view(template_name='index.html'), name='homepage'),
    path('about', TemplateView.as_view(template_name='about.html', extra_context={
        'title': 'scootaloo',
        'author': 'Alex, Natas and Brent'
    }), name='aboutpage'),
] + static(STATIC_URL, document_root=STATICFILES_DIRS[0])
