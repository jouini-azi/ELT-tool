import os
import subprocess
import time

# Chemin vers Laragon (adapte selon ton installation)
LARAGON_PATH = r"C:\laragon"

# Dossier du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# 1️⃣ Lancer Laragon (MySQL, MongoDB si configuré)
subprocess.Popen([os.path.join(LARAGON_PATH, "laragon.exe"), "start"])

# 2️⃣ Attendre que MySQL et MongoDB soient prêts
time.sleep(5)  # tu peux augmenter à 10 si nécessaire

# 3️⃣ Lancer ton app Streamlit
subprocess.run(["streamlit", "run", "Accueil.py"], shell=True)
