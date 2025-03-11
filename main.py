from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.conf.urls.static import static
from django.views.generic import TemplateView
import os
from scripts.login_system import *
from dotenv import load_dotenv


create_database()
create_user_table()

# Handle login requests
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()
        print(f"Login attempt: {username} {password}")
        if verify_login(username, password):
            return HttpResponse("Login successful!")
        else:
            return HttpResponse("Invalid login credentials!")
    return render(request, 'login-alex.html')

# Handle signup requests
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()
        register_user(username, password)
        return HttpResponseRedirect('/login')
    return render(request, 'signup-alex.html')

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

