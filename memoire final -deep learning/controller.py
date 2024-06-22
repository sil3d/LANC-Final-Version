import requests
import time

try:
    with open("ip.txt", "r") as f:
        ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
        print(ip)
except:
    print("erreur de lecture")
try:
    delay = 1  # Délai en secondes entre les requêtes
    led_1_on = requests.get(f'http://{ip}/?led1=on')
    time.sleep(delay)
    led_2_on = requests.get(f'http://{ip}/?led2=on')
    time.sleep(delay)
    led_1_off = requests.get(f'http://{ip}/?led1=off')
    time.sleep(delay)
    led_2_off = requests.get(f'http://{ip}/?led2=off')
    time.sleep(delay)
except requests.ConnectionError:
    print("Erreur de connexion")
    pass

def led(total):
    if total == 0:
        led_1_off
        led_2_off
    elif total == 1:
        led_1_on
        led_2_off
    elif total == 2:
        led_1_off
        led_2_on
