import PySimpleGUI as sg


def gui():

    meses = ['01','02','03','04','05','06','07','08','09','10','11','12']

    layout = [
        [sg.T('Insira o número do lote inicial:'), sg.I(key='-LOTE-', s=(8, 5))],
        [sg.T('Mês:'), sg.DropDown(meses, default_value='01', s=(3, 15), key='-MES-', readonly=True)],
        [sg.B('Rodar', enable_events=True, key='-RODAR-')]
    ]

    window = sg.Window('Imprimir Lançamentos', layout=layout, size=(300,100))
    event, values = window.read()

    lote = values['-LOTE-']
    if lote == '' and event == '-RODAR-':
        sg.popup_error('Insira um número válido')

    mes = values['-MES-']

    if event == '-RODAR-':
        window.minimize()

    return lote, mes, event
