from botcity.core import DesktopBot
import pygetwindow as gw
import pyautogui as gui
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import numpy as np
import time



numero_primeiro_lote = 30180
mes = '05'
quantidade_notas = 3



def not_found(label):
    print(f"Element not found: {label}")



def mudar_janela(titulo_janela):
    janelas = gw.getWindowsWithTitle(titulo_janela) # Obtém todas as janelas com o título especificado
    # Verifica se foi encontrada alguma janela com o título especificado
    if janelas:
        janela = janelas[0] # Seleciona a primeira janela encontrada (você pode iterar sobre a lista para selecionar a janela desejada)
        janela.activate() # Foca na janela (torna-a ativa)
    else:
        print("Nenhuma janela encontrada com o título especificado.")
    time.sleep(1)
    gui.hotkey('alt', 'esc')



def ler_tela(bot):
    # x0,y0 = 70,250
    # x1, y1 = 425, 525
    quantidade_lotes = 0
    while quantidade_lotes == 0:
        screen_cut_temp = bot.screen_cut(x=70, y=250, width=(425-70), height=(350-250))
        screen_cut_temp.save('screen_temp.png')

        text = pytesseract.image_to_string(screen_cut_temp)
        padrao = r'\d{2}\/\d{2}\/\d{4}'
        
        numeros_lote = re.findall(padrao, text, re.MULTILINE)
        quantidade_lotes = len(numeros_lote)
        
    mes = numeros_lote[0].split('/')[1]

    return quantidade_lotes, mes



bot = DesktopBot()

mudar_janela('Lista de Programas')

for n in np.ones(quantidade_notas):
    if not bot.find("campo_numero_lote_inicial", matching=0.97, waiting_time=10000):
        not_found("campo_numero_lote_inicial")
    bot.click_relative(87, 35)
    bot.type_key(str(numero_primeiro_lote))
    bot.tab()
    bot.type_key(str(numero_primeiro_lote))

    if not bot.find("botao_ok", matching=0.97, waiting_time=10000):
        not_found("botao_ok")
    bot.click()
    bot.wait(1850)

    quantidade_lotes, mes_lote = ler_tela(bot)
    
    print(mes_lote)
    if mes == mes_lote:
        if quantidade_lotes == 1:
            print('Registro único')
            break

        if not bot.find("botao_janela_impressao", matching=0.97, waiting_time=10000):
            not_found("botao_janela_impressao")
        bot.click()

        if not bot.find("botao_ok_impressao.png", matching=0.97, waiting_time=10000):
            not_found("botao_ok_impressao")
        bot.click()
        
        if not bot.find("botao_fechar_lancamento", matching=0.97, waiting_time=10000):
            not_found("botao_fechar_lancamento")
        bot.click()
    else:
        print('Mês incompatível')
        break
    numero_primeiro_lote += int(n)

