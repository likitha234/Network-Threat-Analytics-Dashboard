import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_attack_prediction.settings')
django.setup()

from django.contrib.sessions.models import Session
Session.objects.all().delete()
print("All Django Sessions Wiped Successfully.")
