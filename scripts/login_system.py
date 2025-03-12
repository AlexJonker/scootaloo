import json
import pymysql
from dotenv import load_dotenv
import hashlib
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

load_dotenv()

with open('conf.json', 'r') as file:
        conf = json.load(file)

mysql = conf["mysql"]
HOST = mysql["HOST"]
PORT = 3306
USER = mysql["USER"]
PASSWORD = mysql["PASSWORD"]
DATABASE = 'scootaloo'

def get_db_connection():
    return pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        port=PORT
    )

def create_database():
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=PORT)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
    cursor.close()
    conn.close()

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


create_database()
create_user_table()

def verify_login(identifier, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s", (identifier, identifier, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None


def register_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return False

    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    
    cursor.close()
    conn.close()
    return True



def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()
        
        if verify_login(identifier, password):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s", (identifier, identifier, password))
            user = cursor.fetchone()
            return HttpResponse(f"Login successful! Welcome {user[1]} (Email: {user[2]}, UserID: {user[0]})")
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials!'})

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()
        password_retype = hashlib.md5(request.POST.get('password-retype').encode('utf-8')).hexdigest()

        if password != password_retype:
            return render(request, 'signup.html', {'error': 'Passwords do not match!'})

        success = register_user(username, email, password)
        if not success:
            return render(request, 'signup.html', {'error': 'Username or email is already in use!'})

        return HttpResponseRedirect('/login')

    return render(request, 'signup.html')
