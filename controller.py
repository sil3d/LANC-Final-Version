import requests
import tkinter as tk
from tkinter import messagebox

try:
    with open("ip.txt", "r") as f:
        ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
        print(ip)
except:
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("petit problème", "Impossible de se connecter à l'IP spécifiée. vérifier que votre ESP32 est bien allumé et configurer le fichier ip.txt")
    root.destroy()
    pass

try:
    delay = 10  # Délai en secondes entre les requêtes
    led_1_on = requests.get(f'http://{ip}/?LED0=OFF', timeout=delay)
    led_2_on = requests.get(f'http://{ip}/?LED1=OFF', timeout=delay)
    led_1_off = requests.get(f'http://{ip}/?LED0=ON', timeout=delay)
    led_2_off = requests.get(f'http://{ip}/?LED1=ON', timeout=delay)
except requests.ConnectionError:
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("j'ai ureur de connexion", "Impossible de se connecter à l'IP spécifiée.")
    root.destroy()
    pass

def led(total):
    try:
        if total == 0:
            requests.get(f'http://{ip}/?LED0=ON', timeout=delay)
            requests.get(f'http://{ip}/?LED1=ON', timeout=delay)
        elif total == 1:
            requests.get(f'http://{ip}/?LED0=OFF', timeout=delay)
            requests.get(f'http://{ip}/?LED1=ON', timeout=delay)
        elif total == 2:
            requests.get(f'http://{ip}/?LED0=ON', timeout=delay)
            requests.get(f'http://{ip}/?LED1=OFF', timeout=delay)
    except requests.ConnectionError:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Erreur de connexion", "Impossible de se connecter à l'IP spécifiée.")
        root.destroy()
