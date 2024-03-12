## RS-Projekt

# Pokretanje aplikacije
Aplikacija se pokreće pomoću uvicorn naredbi u terminalu. Potrebno je otvoriti tri terminala, jedan za svaku python datoteku. Te ih pokrenuti pomoću sjedećih naredbi, gdje se svaka naredba pokreće u posebnom terminalu: 
# Main.py - python -m uvicorn main:app --reload --port 8000
# Create.py - python -m uvicorn create:app --reload --port 8001
# Edit.py - python -m uvicorn edit:app --reload --port 8002
