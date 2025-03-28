from botcity.core import DesktopBot
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import numpy as np
from pyautogui import alert
from pathlib import Path
import cv2
                   


def not_found(label):
    msgAlerta = f'Deixe o domínio na janela inicial e rode o programa novamente a partir do último número de lote'
    alert(text=msgAlerta, title=f'Elemento não encontrado: {label}')


def preprocess_image(image_path):
    # Carrega a imagem
    image = cv2.imread(image_path)

    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica CLAHE para melhorar o contraste
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # Aplica um desfoque para reduzir ruído
    blurred = cv2.GaussianBlur(enhanced, (5,5), 0)

    # Aplica binarização Otsu
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Aumenta a resolução para melhorar a precisão do OCR
    scale_percent = 300  # Aumenta em 300%
    width = int(binary.shape[1] * scale_percent / 100)
    height = int(binary.shape[0] * scale_percent / 100)
    resized = cv2.resize(binary, (width, height), interpolation=cv2.INTER_CUBIC)

    return resized


def ler_tela(bot):
    # x0,y0 = 70,250
    # x1, y1 = 425, 525
    n_tentativas = 0
    quantidade_lotes = 0
    while (quantidade_lotes == 0) and (n_tentativas < 7):
        
        n_tentativas += 1
        bot.wait(1000)
        
        screen_cut_temp = bot.screen_cut(x=70, y=250, width=(425-70), height=(350-250))
        screen_cut_temp.save('screen_temp.png')

        processed_image = preprocess_image('screen_temp.png')
        bot.wait(1000)
        # Configuração do OCR
        custom_config = r'--oem 3 --psm 6'  # Ajusta a segmentação de texto para melhor precisão

        # Executa OCR na imagem processada
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        print(text)
        padrao = r'\d{1,2}\/\d{2}\/\d{4}'
        
        numeros_lote = re.findall(padrao, text, re.MULTILINE)
        quantidade_lotes = len(numeros_lote)

    mes = numeros_lote[0].split('/')[1]

    return quantidade_lotes, mes



def main(numero_primeiro_lote, mes, quantidade_notas = 150):
    
    bot = DesktopBot()
    bot.wait(4000)

    lotes_unicos = []

    for n in np.ones(quantidade_notas):
        if not bot.find("campo_numero_lote_inicial", matching=0.97, waiting_time=10000):
            not_found("campo_numero_lote_inicial")

        bot.click_relative(87, 35, clicks=2)
        bot.type_key(str(numero_primeiro_lote))
        bot.tab()
        bot.type_key(str(numero_primeiro_lote))

        if not bot.find("botao_ok", matching=0.97, waiting_time=10000):
            not_found("botao_ok")
        bot.click()

        try:
            quantidade_lotes, mes_lote = ler_tela(bot)
        except:
            if not bot.find("janela_fim", matching=0.97, waiting_time=10000):
                not_found("janela_fim")
            alert('Sem mais lotes para emitir')
            raise

        if mes == mes_lote:
            if quantidade_lotes == 1:
                # alert(title='Registro único', text='Digite manualmente o intervalo de lotes únicos')
                lotes_unicos.append(numero_primeiro_lote)

                if not bot.find("botao_fechar_lancamento", matching=0.97, waiting_time=10000):
                    not_found("botao_fechar_lancamento")
                bot.click()

                numero_primeiro_lote += int(n)
                continue

            if not bot.find("botao_janela_impressao", matching=0.97, waiting_time=10000):
                not_found("botao_janela_impressao")
            bot.click()

            if not bot.find("botao_ok_impressao", matching=0.97, waiting_time=10000):
                not_found("botao_ok_impressao")
            bot.click()

            # if not bot.find("botao_cancelar(teste)", matching=0.97, waiting_time=10000):
            #     not_found("botao_cancelar(teste)")
            # bot.click()
            bot.wait(500)

            if not bot.find("botao_fechar_lancamento", matching=0.97, waiting_time=10000):
                not_found("botao_fechar_lancamento")
            bot.click()

            count = 0
            while (bot.find("botao_fechar_lancamento", matching=0.97, waiting_time=1000)) and (count < 10):
                bot.click()
                bot.wait(500)
        else:
            alert('Mês incompatível')
            break
        numero_primeiro_lote += int(n)

    arquivoLotesUnicos = Path.home()/'OneDrive/Área de Trabalho/lotes_unicos.txt'
    with open(arquivoLotesUnicos, 'w') as f:
        f.write(f'Lotes com apenas 1 lançamento: {lotes_unicos}')

    Path('screen_temp.png').unlink()



if __name__ == '__main__':
    main(32405, '11')
