import os
import sys
from selenium import webdriver
import pyautogui
import pyperclip
import keyboard
import threading
from time import sleep


path = os.path.join(sys.path[0], 'chromedriver.exe')
safe_exit = False
numbers = []

def clickAbrirWpp():
    sleep(1)
    pyautogui.click((550, 200))

def registrarError(num):
    with open('numeros salteados.txt', 'a+') as f:
        f.write(f"{num} fue salteado\n")

def enviarMensaje(num):
    global safe_exit
    found = None
    while found is None:
        found = pyautogui.locateCenterOnScreen('escribirmensaje.PNG')
        if safe_exit:
            safe_exit = False
            pyautogui.click((1900, 15))
            registrarError(num)
            return
    pyperclip.copy("Hola! Soy Gabriela profe de Diseño en UAI. Por favor unite al siguiente chat en telegram (bajar la app) donde explicaré cómo serán las clases en la Facu: https://t.me/joinchat/MYqkEhSA08pm903hwj5aKQ")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.keyDown('enter')
    pyautogui.click((1900, 15))

def formatNumber(num):
    if not num.startswith("+54"):
        num = "+54" + num
    num = num.rstrip('\n')
    return num


def process():
    with open('numeros.txt', "r") as f:
        numbers = list(map(formatNumber, f.readlines()))

    for num in numbers:
        driver = webdriver.Chrome(path)
        driver.get(f"https://api.whatsapp.com/send?phone={num}")
        clickAbrirWpp()
        driver.close()
        enviarMensaje(num)

if __name__ == "__main__":
    t1 = threading.Thread(target=process)
    t1.setDaemon(True)
    t1.start()
    while True:
        if not t1.isAlive():
            break
            
        if keyboard.is_pressed('esc'):
            sys.exit()
            break

        if keyboard.is_pressed('tab'):
            safe_exit = True