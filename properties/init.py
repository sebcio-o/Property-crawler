import os
from requests_html import HTMLSession

os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")

session = HTMLSession()
r = session.get("http://1.1.1.1")
r.html.render(timeout=20)