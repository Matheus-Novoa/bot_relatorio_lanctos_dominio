from botcity.core import DesktopBot
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import numpy as np
                   


def not_found(label):
    print(f"Element not found: {label}")


def ler_tela(bot):
    # x0,y0 = 70,250
    # x1, y1 = 425, 525
    n_tentativas = 0
    quantidade_lotes = 0
    while (quantidade_lotes == 0) and (n_tentativas < 7):
        
        n_tentativas += 1
        bot.wait(500)
        
        screen_cut_temp = bot.screen_cut(x=70, y=250, width=(425-70), height=(350-250))
        screen_cut_temp.save('screen_temp.png')

        text = pytesseract.image_to_string(screen_cut_temp)
        padrao = r'\d{2}\/\d{2}\/\d{4}'
        
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
            print('Sem mais lotes para emitir')
            break

        if mes == mes_lote:
            if quantidade_lotes == 1:
                print('Registro único')
                lotes_unicos.append(numero_primeiro_lote)

                if not bot.find("botao_fechar_lancamento", matching=0.97, waiting_time=10000):
                    not_found("botao_fechar_lancamento")
                bot.click()

                numero_primeiro_lote += int(n)
                continue

            if not bot.find("botao_janela_impressao", matching=0.97, waiting_time=10000):
                not_found("botao_janela_impressao")
            bot.click()

            if not bot.find("botao_cancelar(teste)", matching=0.97, waiting_time=10000):
                not_found("botao_cancelar(teste)")
            bot.click()
            
            if not bot.find("botao_fechar_lancamento", matching=0.97, waiting_time=10000):
                not_found("botao_fechar_lancamento")
            bot.click()
        else:
            print('Mês incompatível')
            break
        numero_primeiro_lote += int(n)

    # print(f'Lotes com apenas 1 lançamento: {lotes_unicos}')
    return f'Lotes com apenas 1 lançamento: {lotes_unicos}'



if __name__ == '__main__':
  numero_primeiro_lote = 30500
  mes = '06'
  lotes = main(numero_primeiro_lote, mes, 3)
