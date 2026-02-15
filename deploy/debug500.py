"""Run on server: /opt/todoapp/venv/bin/python /opt/todoapp/deploy/debug500.py"""
import os
import sys

os.environ["DEBUG"] = "False"
os.environ["DJANGO_SETTINGS_MODULE"] = "todoapp.settings"
sys.path.insert(0, "/opt/todoapp")

import django
django.setup()

from django.test import Client

c = Client()
try:
    r = c.get("/")
    print(f"Status: {r.status_code}")
    if r.status_code >= 400:
        print(r.content.decode()[:3000])
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()
